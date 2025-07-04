#!/usr/bin/env python3
"""
Lacework Compliance Reporter - Streamlit Web Interface
Beautiful web-based interface for generating and analyzing compliance reports
"""

import streamlit as st
import json
import os
import subprocess
from datetime import datetime, timedelta
import tempfile
import base64
import time
from lacework_compliance_reporter import LaceworkConfig, ComplianceFilter, ComplianceReporter
import re

# Page configuration
st.set_page_config(
    page_title="Lacework Compliance Reporter",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
    }
    .info-message {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #bee5eb;
    }
</style>
""", unsafe_allow_html=True)



def load_saved_config():
    """Load previously saved configuration from gui_config.json or config.json"""
    try:
        # First try to load from gui_config.json (Streamlit-specific config)
        if os.path.exists("gui_config.json"):
            with open("gui_config.json", "r") as f:
                return json.load(f)
        
        # If gui_config.json doesn't exist, try to load from config.json
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                config_data = json.load(f)
                # Convert config.json format to expected format
                return {
                    "keyId": config_data.get("keyId", ""),
                    "secret": config_data.get("secret", ""),
                    "account": config_data.get("account", ""),
                    "url": config_data.get("url", "")
                }
    except Exception as e:
        st.warning(f"Could not load configuration: {e}")
    return {}

def save_config(config):
    """Save configuration to file"""
    try:
        with open("gui_config.json", "w") as f:
            json.dump(config, f, indent=2)
        return True
    except:
        return False

def generate_report(config, options, progress_callback=None):
    """Generate compliance report with progress updates"""
    try:
        # Step 1: Initialize configuration
        if progress_callback:
            progress_callback("🔧 Initializing configuration...")
        
        lacework_config = LaceworkConfig(
            keyId=config["keyId"],
            secret=config["secret"],
            account=config["account"],
            url=config["url"]
        )
        
        # Step 2: Parse time range
        if progress_callback:
            progress_callback("⏰ Parsing time range...")
        
        from lacework_compliance_reporter import parse_time_range
        start_time, end_time = parse_time_range(options["timeRange"])
        
        # Step 3: Create filter configuration
        if progress_callback:
            progress_callback("🔍 Setting up compliance filters...")
        
        filter_config = ComplianceFilter(
            dataset=options["dataset"],
            start_time=start_time,
            end_time=end_time,
            status_filter=options["status"] if options["status"] != "All" else None,
            severity_levels=options.get("severity")
        )
        
        # Step 4: Initialize reporter
        if progress_callback:
            progress_callback("🔐 Authenticating with Lacework API...")
        
        reporter = ComplianceReporter(lacework_config)
        
        # Step 5: Generate report
        if progress_callback:
            progress_callback("📊 Fetching compliance data from API...")
        
        # --- BEGIN PATCH: capture API payload ---
        # Rebuild the payload as in ComplianceReporter.generate_compliance_report
        payload = {
            'dataset': filter_config.dataset,
            'returns': [
                'account', 'id', 'recommendation', 'severity', 'status', 
                'resource', 'region', 'section', 'evalType', 'reason', 'reportTime'
            ]
        }
        if filter_config.start_time or filter_config.end_time:
            payload['timeFilter'] = {}
            if filter_config.start_time:
                payload['timeFilter']['startTime'] = filter_config.start_time
            if filter_config.end_time:
                payload['timeFilter']['endTime'] = filter_config.end_time
        filters = []
        if filter_config.status_filter:
            filters.append({
                'field': 'status',
                'expression': 'eq',
                'value': filter_config.status_filter
            })
        if filter_config.account_ids:
            filters.append({
                'field': 'account.AccountId',
                'expression': 'in',
                'values': filter_config.account_ids
            })
        if filter_config.severity_levels:
            filters.append({
                'field': 'severity',
                'expression': 'in',
                'values': filter_config.severity_levels
            })
        if filters:
            payload['filters'] = filters
        # --- END PATCH ---
        
        report = reporter.generate_compliance_report(filter_config)
        
        # Step 6: Save report
        if progress_callback:
            progress_callback("💾 Saving report to file...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"compliance_report_{timestamp}_all.{options['format']}"
        reporter.save_report(report, output_file, options["format"])
        
        # Step 7: Apply resource group filtering if specified
        if options.get("resource_groups"):
            if progress_callback:
                progress_callback("🎯 Applying resource group filters...")
            
            filter_result = filter_report_by_resource_groups(output_file, options["resource_groups"])
            if not filter_result["success"]:
                if progress_callback:
                    progress_callback("⚠️ Resource group filtering failed, continuing with unfiltered report...")
                # Continue with unfiltered report
        
        # Step 8: Complete
        if progress_callback:
            progress_callback("✅ Report generation completed!")
        
        # Store report in session state for analysis
        st.session_state.report = report
        st.session_state.output_file = output_file
        st.session_state.file_list_needs_refresh = True
        
        return {
            "success": True,
            "report": report,
            "output_file": output_file,
            "api_payload": payload
        }
        
    except Exception as e:
        if progress_callback:
            progress_callback(f"❌ Error: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

def analyze_report(file_path=None, resource_groups=None):
    """Run analysis on a specific report file or the most recent one, with optional resource group filtering"""
    from collections import defaultdict
    
    try:
        if file_path is None:
            # Find the most recent compliance report JSON file
            import glob
            report_files = glob.glob("compliance_report_*.json")
            
            if not report_files:
                return {
                    "success": False,
                    "error": "No compliance report found. Please generate a report first."
                }
            
            # Get the most recent file
            file_path = max(report_files, key=os.path.getctime)
        
        # Load the report data
        with open(file_path, 'r') as f:
            report = json.load(f)
        
        # If resource groups are selected, filter the report
        if resource_groups:
            filtered_evaluations = []
            for evaluation in report.get('evaluations', []):
                eval_resource_groups = evaluation.get('resourceGroups', [])
                if eval_resource_groups:
                    for rg in eval_resource_groups:
                        if rg.get('resourceGuid') in resource_groups:
                            filtered_evaluations.append(evaluation)
                            break
            report['evaluations'] = filtered_evaluations
        
        # Add file information to the analysis output
        file_info = f"📊 Analyzing file: {file_path}"
        if resource_groups:
            # Try to get resource group names from session state
            resource_group_names = []
            if 'resource_groups' in st.session_state:
                for rg_guid in resource_groups:
                    for rg in st.session_state['resource_groups']:
                        if rg['resourceGuid'] == rg_guid:
                            resource_group_names.append(rg['resourceName'])
                            break
            
            if resource_group_names:
                file_info += f" (filtered to {len(resource_groups)} resource group(s): {', '.join(resource_group_names)})"
            else:
                file_info += f" (filtered to {len(resource_groups)} resource group(s))"
        file_info += f"\n{'='*50}\n\n"
        
        # Perform analysis
        total_evaluations = len(report.get('evaluations', []))
        evaluations_with_groups = 0
        evaluations_without_groups = 0
        resource_group_counts = defaultdict(int)
        resource_group_details = {}
        
        # Get metadata from the report
        metadata = report.get('metadata', {})
        generated_at = metadata.get('generated_at', 'Unknown')
        dataset = metadata.get('dataset', 'Unknown')
        time_range = metadata.get('time_range', {})
        filters_applied = metadata.get('filters_applied', {})
        status_filter = filters_applied.get('status', 'All')
        
        # Format time range for display
        time_range_str = 'Unknown'
        if time_range.get('start_time') or time_range.get('end_time'):
            start_time = time_range.get('start_time', 'N/A')
            end_time = time_range.get('end_time', 'N/A')
            time_range_str = f"{start_time} to {end_time}"
        
        # Build analysis output
        analysis_output = []
        analysis_output.append("=== COMPLIANCE REPORT SUMMARY ===")
        analysis_output.append(f"Total evaluations: {total_evaluations}")
        analysis_output.append(f"Report generated: {generated_at}")
        analysis_output.append(f"Time range: {time_range_str}")
        analysis_output.append(f"Dataset: {dataset}")
        analysis_output.append(f"Status filter: {status_filter}")
        
        analysis_output.append("\n=== RESOURCE GROUP ANALYSIS ===")
        
        # Analyze each evaluation
        for evaluation in report.get('evaluations', []):
            eval_resource_groups = evaluation.get('resourceGroups', [])
            
            if eval_resource_groups:
                evaluations_with_groups += 1
                for rg in eval_resource_groups:
                    rg_name = rg.get('resourceName', 'Unknown')
                    resource_group_counts[rg_name] += 1
                    # Store details for the first occurrence
                    if rg_name not in resource_group_details:
                        resource_group_details[rg_name] = {
                            'guid': rg.get('resourceGuid'),
                            'type': rg.get('resourceType'),
                            'enabled': rg.get('enabled'),
                            'isDefault': rg.get('isDefault')
                        }
            else:
                evaluations_without_groups += 1
        
        analysis_output.append(f"Evaluations with resource groups: {evaluations_with_groups}")
        analysis_output.append(f"Evaluations without resource groups: {evaluations_without_groups}")
        
        analysis_output.append("\n=== RESOURCE GROUP BREAKDOWN ===")
        if resource_group_counts:
            for rg_name, count in sorted(resource_group_counts.items(), key=lambda x: x[1], reverse=True):
                details = resource_group_details.get(rg_name, {})
                
                analysis_output.append(f"{rg_name}: {count} resources")
                analysis_output.append(f"  - Type: {details.get('type', 'Unknown')}")
                analysis_output.append(f"  - GUID: {details.get('guid', 'Unknown')}")
                analysis_output.append(f"  - Enabled: {details.get('enabled', 'Unknown')}")
                analysis_output.append(f"  - Default: {details.get('isDefault', 'Unknown')}")
                analysis_output.append("")
        else:
            analysis_output.append("No resource groups found in evaluations")
        
        analysis_output.append("=== SAMPLE RESOURCES ===")
        # Show a few sample resources with their groups
        samples = 0
        for evaluation in report.get('evaluations', []):
            if evaluation.get('resourceGroups') and samples < 3:
                analysis_output.append(f"Resource: {evaluation.get('resource', 'Unknown')}")
                analysis_output.append(f"Groups: {[rg.get('resourceName') for rg in evaluation.get('resourceGroups', [])]}")
                analysis_output.append(f"Region: {evaluation.get('region', 'Unknown')}")
                analysis_output.append(f"Account: {evaluation.get('account', {}).get('AccountId', 'Unknown')}")
                analysis_output.append("")
                samples += 1
        
        return {
            "success": True,
            "output": file_info + "\n".join(analysis_output)
        }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to run analysis: {str(e)}"
        }

def get_download_link(file_path, file_name):
    """Generate a download link for a file"""
    with open(file_path, "rb") as file:
        data = file.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/octet-stream;base64,{b64}" download="{file_name}">📥 Download {file_name}</a>'
    return href

def get_resource_groups_from_report(report_file=None):
    """Get resource groups that actually appear in the compliance report"""
    try:
        if report_file is None:
            # Find the most recent compliance report JSON file
            import glob
            report_files = glob.glob("compliance_report_*.json")
            
            if not report_files:
                return {
                    "success": False,
                    "error": "No compliance report found. Please generate a report first."
                }
            
            # Get the most recent file
            report_file = max(report_files, key=os.path.getctime)
        
        # Extract unique resource groups from the report
        result = subprocess.run([
            'jq', '-r', '''
            .evaluations | 
            map(select(.resourceGroups | length > 0)) | 
            .[].resourceGroups[] | 
            {resourceGuid, resourceName, resourceType} | 
            tojson
            ''', report_file
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            # Parse the JSON lines and get unique resource groups
            resource_groups = []
            seen_guids = set()
            
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    try:
                        rg = json.loads(line)
                        if rg['resourceGuid'] not in seen_guids:
                            resource_groups.append(rg)
                            seen_guids.add(rg['resourceGuid'])
                    except json.JSONDecodeError:
                        continue
            
            return {
                "success": True,
                "resource_groups": resource_groups
            }
        else:
            return {
                "success": False,
                "error": result.stderr if result.stderr else "Unknown error"
            }
            
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Timeout while fetching resource groups"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def filter_report_by_resource_groups(report_file, selected_resource_groups):
    """Filter the compliance report by selected resource groups using jq"""
    try:
        if not selected_resource_groups:
            return {"success": True, "message": "No filtering applied - all data included"}
        
        # Create jq filter to only include evaluations that match selected resource groups
        # We need to check if any of the resourceGroups in the evaluation match our selected GUIDs
        jq_filter = f'''
        .evaluations |= map(
            select(
                .resourceGroups and 
                (.resourceGroups | length > 0) and
                (.resourceGroups | any(.resourceGuid | IN({json.dumps(selected_resource_groups)})))
            )
        )
        '''
        
        # Apply the filter using jq
        result = subprocess.run([
            'jq', jq_filter, report_file
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            # Write the filtered data back to the file
            with open(report_file, 'w') as f:
                f.write(result.stdout)
            
            return {
                "success": True,
                "message": f"Report filtered to {len(selected_resource_groups)} resource group(s)"
            }
        else:
            return {
                "success": False,
                "error": f"jq filtering failed: {result.stderr}"
            }
            
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Timeout while filtering report"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def format_file_size(file_size):
    """Convert file size to human readable format"""
    if file_size < 1024:
        return f"{file_size} B"
    elif file_size < 1024 * 1024:
        return f"{file_size / 1024:.1f} KB"
    else:
        return f"{file_size / (1024 * 1024):.1f} MB"

def create_csv_from_json(json_file, csv_file):
    """Create CSV file from JSON compliance report"""
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        csv_rows = []
        for eval_item in data.get('evaluations', []):
            row = {
                'evaluationId': eval_item.get('id', ''),
                'status': eval_item.get('status', ''),
                'severity': eval_item.get('severity', ''),
                'resource': eval_item.get('resource', ''),
                'accountId': eval_item.get('account', {}).get('AccountId', ''),
                'accountAlias': eval_item.get('account', {}).get('Account_Alias', ''),
                'region': eval_item.get('region', ''),
                'section': eval_item.get('section', ''),
                'evalType': eval_item.get('evalType', ''),
                'reason': eval_item.get('reason', ''),
                'recommendation': eval_item.get('recommendation', ''),
                'reportTime': eval_item.get('reportTime', ''),
                'resourceGroups': ', '.join([rg.get('resourceName', '') for rg in eval_item.get('resourceGroups', [])])
            }
            csv_rows.append(row)
        
        import csv
        with open(csv_file, 'w', newline='') as f:
            if csv_rows:
                writer = csv.DictWriter(f, fieldnames=csv_rows[0].keys())
                writer.writeheader()
                writer.writerows(csv_rows)
        
        return True
    except Exception as e:
        st.error(f"Failed to create CSV: {e}")
        return False

def generate_filtered_filename(base_file, resource_groups=None):
    """Generate a descriptive filename based on selected resource groups"""
    if not resource_groups:
        return base_file.replace('.json', '_all.json')
    
    # Get resource group names from session state
    if 'resource_groups' in st.session_state:
        selected_names = []
        for rg_guid in resource_groups:
            for rg in st.session_state['resource_groups']:
                if rg['resourceGuid'] == rg_guid:
                    # Clean the name for filename use (remove special chars, limit length)
                    clean_name = re.sub(r'[^a-zA-Z0-9_-]', '_', rg['resourceName'])
                    clean_name = clean_name[:20]  # Limit length
                    selected_names.append(clean_name)
                    break
        
        if selected_names:
            # Create a descriptive suffix
            if len(selected_names) == 1:
                suffix = f"_{selected_names[0]}"
            else:
                # For multiple groups, use first few names
                suffix = f"_{'_'.join(selected_names[:3])}"
                if len(selected_names) > 3:
                    suffix += f"_and_{len(selected_names)-3}_more"
            
            return base_file.replace('.json', f'{suffix}.json')
    
    # Fallback to generic filtered name
    return base_file.replace('.json', '_filtered.json')

def main():
    # Header
    st.markdown('<h1 class="main-header">🔒 Lacework Compliance Reporter</h1>', unsafe_allow_html=True)
    
    # Load saved configuration
    saved_config = load_saved_config()
    
    # Show simple notification if credentials were loaded from config.json
    if saved_config and os.path.exists("config.json") and not os.path.exists("gui_config.json"):
        st.success("✅ **Credentials loaded automatically from config.json**")
        st.info("💡 Your API credentials have been automatically loaded from the config.json file. You can modify them in the sidebar if needed.")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("🔧 API Configuration")
        
        # API Configuration Form
        with st.form("api_config"):
            key_id = st.text_input(
                "Key ID", 
                value=saved_config.get("keyId", ""),
                help="Your Lacework API Key ID"
            )
            
            secret = st.text_input(
                "Secret", 
                value=saved_config.get("secret", ""),
                type="password",
                help="Your Lacework API Secret"
            )
            
            account = st.text_input(
                "Account", 
                value=saved_config.get("account", ""),
                help="Your Lacework account domain (e.g., company.lacework.net)"
            )
            
            url = st.text_input(
                "URL", 
                value=saved_config.get("url", ""),
                help="Your Lacework instance URL (e.g., https://company.lacework.net)"
            )
            
            # Save config button
            if st.form_submit_button("💾 Save Configuration"):
                config = {
                    "keyId": key_id,
                    "secret": secret,
                    "account": account,
                    "url": url
                }
                if save_config(config):
                    st.success("Configuration saved successfully!")
                else:
                    st.error("Failed to save configuration")
        
        st.markdown("---")
        
                # Resource Group Filter
        st.markdown("### 🔍 Resource Group Filter")
        st.markdown("Filter compliance evaluations by specific resource groups (optional)")
        
        # Check if API credentials are configured
        if not all([key_id, secret, account, url]):
            st.warning("⚠️ Please configure your API credentials above to load resource groups")
            resource_groups = []
            selected_resource_groups = []
        else:
            # Button to get resource groups
            if st.button("📋 Get Resource Groups from Report", key="get_resource_groups"):
                config = {
                    "keyId": key_id,
                    "secret": secret,
                    "account": account,
                    "url": url
                }
                
                with st.spinner("Fetching resource groups from latest report..."):
                    result = get_resource_groups_from_report()
                    
                    if result["success"]:
                        st.session_state.resource_groups = result["resource_groups"]
                        st.success(f"✅ Loaded {len(result['resource_groups'])} resource groups from report")
                    else:
                        st.error(f"Failed to load resource groups: {result['error']}")
            
            # Get resource groups from session state or initialize empty
            resource_groups = st.session_state.get("resource_groups", [])
            
            if resource_groups:
                # Create options for the multiselect
                resource_group_options = [rg['resourceGuid'] for rg in resource_groups]
                resource_group_labels = [f"{rg['resourceName']} ({rg['resourceType']})" for rg in resource_groups]
                
                # Create a mapping for display
                resource_group_mapping = dict(zip(resource_group_options, resource_group_labels))
                
                selected_resource_groups = st.multiselect(
                    "Select Resource Groups to Filter By:",
                    options=resource_group_options,
                    format_func=lambda x: resource_group_mapping.get(x, x),
                    help="Select one or more resource groups to filter the compliance report. Leave empty to include all data."
                )
                
                if selected_resource_groups:
                    st.info(f"📊 Report will be filtered to {len(selected_resource_groups)} selected resource group(s)")
                else:
                    st.info("💡 No resource groups selected - all compliance data will be included")
                    
                # Add clear selection button
                if st.button("🗑️ Clear Resource Group Selection", key="clear_resource_groups"):
                    selected_resource_groups = []
                    st.success("Resource group selection cleared")
                    st.rerun()
            else:
                selected_resource_groups = []
                st.info("💡 After you have generated your first report, Click 'Get Resource Groups from Report' to load available resource groups from the latest report")
       
        # Report Options
        st.header("📊 Report Options")
        
        dataset = st.selectbox(
            "Dataset",
            ["AwsCompliance", "AzureCompliance", "GcpCompliance", "K8sCompliance"],
            index=0
        )
        
        time_range = st.selectbox(
            "Time Range",
            ["24h", "7d", "30d"],
            index=0
        )
        
        # Hidden status filter - default to NonCompliant
        status = "NonCompliant"
        
        severity = st.multiselect(
            "Severity Filter",
            ["Critical", "High", "Medium", "Low", "Info"],
            default=["Critical", "High"],
            help="Select severity levels to include in the report. Leave empty to include all severities."
        )
        
        # Hidden output format - default to json
        output_format = "json"
        
        st.markdown("---")
        
 
        # Store options
        options = {
            "dataset": dataset,
            "timeRange": time_range,
            "status": status,
            "format": output_format,
            "severity": severity if severity else None,
            "resource_groups": selected_resource_groups if selected_resource_groups else None
        }
    
    # Main content area - Use containers to prevent layout shifts
    main_container = st.container()
    
    with main_container:
        # Create two columns for the main layout with fixed heights
        col1, col2 = st.columns([2, 1])
        
        # Left column (Main content) - positioned first
        with col1:
            # Create a container for the left column content to prevent movement
            left_column_container = st.container()
            
            with left_column_container:
                # Report Generation Section
                st.header("🚀 Generate Non-Compliant Resource Report")
                st.markdown("The Ui can lag, give it time, especially with large files")
                # Create a container for the report generation area
                report_container = st.container()
                
                with report_container:
                    # Generate Report Button
                    if st.button("📋 Generate Compliance Report", type="primary", use_container_width=True):
                        # Validate configuration
                        if not all([key_id, secret, account, url]):
                            st.error("Please fill in all API configuration fields")
                        else:
                            # Show progress with detailed steps
                            config = {
                                "keyId": key_id,
                                "secret": secret,
                                "account": account,
                                "url": url
                            }
                            
                            # Create progress container
                            progress_container = st.empty()
                            current_step = st.empty()
                            
                            def update_progress(message):
                                current_step.info(f"🔄 {message}")
                            
                            with st.spinner("Starting report generation..."):
                                result = generate_report(config, options, update_progress)
                            
                            # Clear progress display
                            progress_container.empty()
                            current_step.empty()
                            
                            # Show API Request Payload debug info
                            if result.get('api_payload'):
                                with st.expander("🔍 API Request Payload (Click to expand)", expanded=False):
                                    st.code(json.dumps(result['api_payload'], indent=2), language="json")
                            
                            if result["success"]:
                                report = result["report"]
                                output_file = result["output_file"]
                                
                                # Check if report has any data
                                total_evaluations = report['metadata']['total_evaluations']
                                
                                if total_evaluations == 0:
                                    st.markdown(f"""
                                    <div class="info-message">
                                        <h3>ℹ️ Report Generated (No Data Found)</h3>
                                        <p><strong>Generated at:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                                        <p><strong>Output file:</strong> {output_file}</p>
                                        <p><strong>Format:</strong> {output_format.upper()}</p>
                                        <p><strong>Status:</strong> No compliance evaluations found for the selected criteria.</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                else:
                                    # Success message
                                    st.markdown(f"""
                                    <div class="success-message">
                                        <h3>✅ Report Generated Successfully!</h3>
                                        <p><strong>Generated at:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                                        <p><strong>Output file:</strong> {output_file}</p>
                                        <p><strong>Format:</strong> {output_format.upper()}</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                # Report metrics
                                metric_col1, metric_col2, metric_col3 = st.columns(3)
                                
                                with metric_col1:
                                    st.metric(
                                        "Total Evaluations",
                                        report['metadata']['total_evaluations']
                                    )
                                
                                with metric_col2:
                                    st.metric(
                                        "Dataset",
                                        report['metadata']['dataset']
                                    )
                                
                                with metric_col3:
                                    st.metric(
                                        "Status Filter",
                                        report['metadata']['filters_applied']['status'] or "All"
                                    )
                                
                                # Show additional info if no data found
                                if total_evaluations == 0:
                                    st.info("💡 **Tip:** Try widening options to see more compliance data.")
                                
                                # Show resource group filter info if used
                                if options.get("resource_groups"):
                                    st.markdown("### 🔍 Resource Group Filter Applied")
                                    st.info(f"📊 Report filtered to {len(options['resource_groups'])} resource group(s)")
                                    
                                    # Show selected resource group names
                                    if 'resource_groups' in st.session_state:
                                        selected_names = []
                                        for rg_guid in options['resource_groups']:
                                            for rg in st.session_state['resource_groups']:
                                                if rg['resourceGuid'] == rg_guid:
                                                    selected_names.append(rg['resourceName'])
                                                    break
                                        
                                        if selected_names:
                                            st.markdown("**Selected Resource Groups:**")
                                            for name in selected_names:
                                                st.markdown(f"- {name}")
                                
                                # Download link
                                st.markdown("### 📥 Download Report")
                                download_link = get_download_link(output_file, output_file)
                                st.markdown(download_link, unsafe_allow_html=True)
                                
                                # Store report in session state for analysis
                                st.session_state.report = report
                                st.session_state.output_file = output_file
                                st.session_state.file_list_needs_refresh = True
                                
                                st.markdown("""
                                <div class="success-message">
                                    <h3>✅ Report Generated Successfully!</h3>
                                    <p>💡 Use the 'Analyse Selected File' button in the File Management section below to analyse this report.</p>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.error(f"Failed to generate report: {result['error']}")
                
                st.markdown("---")
                
                # File selection section - moved to col1
                st.markdown("### 📄 Select a Base Report File to Analyse")
                st.markdown("**Once a file is downloaded, you can analyse it to see the detailed metadata and apply resource group filtering to the report to get resource group specific data**")
                # Add analyse button above the file dropdown
                if st.button("🔍 Analyse Selected File", key="analyse_selected_file_above", type="primary", use_container_width=True):
                    if 'selected_file' in st.session_state and st.session_state.selected_file:
                        with st.spinner(f"Analysing {st.session_state.selected_file}..."):
                            analysis_result = analyze_report(st.session_state.selected_file, options["resource_groups"])
                            
                            # Store analysis result in session state with file-specific key
                            st.session_state[f"analysis_result_{st.session_state.selected_file}"] = analysis_result
                            
                            if not analysis_result["success"]:
                                st.error(f"Analysis failed: {analysis_result['error']}")
                    else:
                        st.warning("Please select a file first")
                
                if options.get("resource_groups"):
                    st.info("💡 Click 'Analyse Selected File' to generate filtered downloads")
                else:
                    st.info("💡 Click 'Analyse Selected File' to view detailed metadata, you can also apply resource group filtering to the report from the dropdown on the left")
                
                # Optimized file list caching with better performance
                cache_key = 'file_dropdown_cache'
                cache_timestamp_key = 'file_dropdown_cache_timestamp'
                current_time = time.time()
                
                # Check if cache is valid (refresh every 30 seconds)
                cache_valid = (
                    cache_key in st.session_state and 
                    cache_timestamp_key in st.session_state and
                    current_time - st.session_state[cache_timestamp_key] < 30 and
                    not st.session_state.get('file_list_needs_refresh', False)
                )
                
                if not cache_valid:
                    # Only refresh if cache is invalid
                    with st.spinner("🔄 Loading file list..."):
                        import glob
                        report_files = glob.glob("compliance_report_*.json")
                        
                        # Filter to only show "_all" files (base files without resource group filtering)
                        all_files = [f for f in report_files if "_all.json" in f]
                        
                        # Sort by creation time (newest first) and cache the result
                        all_files.sort(key=os.path.getctime, reverse=True)
                    
                    # Create display names efficiently
                    file_options = []
                    file_display_names = []
                    
                    for file in all_files[:10]:  # Show last 10 files
                        # Extract timestamp from filename for display (optimized)
                        display_name = f"📄 {file}"
                        if "_" in file and "." in file:
                            timestamp_part = file.split("_")[-1].split(".")[0]
                            if len(timestamp_part) == 15 and timestamp_part.replace("_", "").isdigit():
                                try:
                                    # Convert timestamp back to readable format
                                    timestamp_obj = datetime.strptime(timestamp_part, "%Y%m%d_%H%M%S")
                                    display_name = f"📄 {timestamp_obj.strftime('%Y-%m-%d %H:%M:%S')} (JSON)"
                                except:
                                    pass  # Keep default display name if parsing fails
                        
                        file_options.append(file)
                        file_display_names.append(display_name)
                    
                    # Cache the results
                    st.session_state[cache_key] = {
                        'file_options': file_options,
                        'file_display_names': file_display_names,
                        'all_files': all_files
                    }
                    st.session_state[cache_timestamp_key] = current_time
                    st.session_state.file_list_needs_refresh = False
                else:
                    # Use cached data
                    cache_data = st.session_state[cache_key]
                    file_options = cache_data['file_options']
                    file_display_names = cache_data['file_display_names']
                    all_files = cache_data['all_files']
                
                if all_files:
                    # Create selectbox for file selection
                    selected_file = st.selectbox(
                        "Choose a report file:",
                        options=file_options,
                        format_func=lambda x: file_display_names[file_options.index(x)],
                        index=0,  # Default to most recent file
                        key="file_selector"
                    )
                    
                    # Show selected file info and actions
                    if selected_file and os.path.exists(selected_file):
                        st.success(f"✅ Selected: {selected_file}")
                        
                        # Show basic file info (no JSON parsing)
                        file_size = os.path.getsize(selected_file)
                        size_str = format_file_size(file_size)
                        
                        # Get file creation time
                        file_created = datetime.fromtimestamp(os.path.getctime(selected_file))
                        
                        st.markdown(f"""
                        **Quick File Summary:**
                        - Created: {file_created.strftime('%Y-%m-%d %H:%M:%S')}
                        - File Size: {size_str}
                        - 💡 Click 'Analyse Selected File' above for detailed metadata
                        """)
                        
                        # Store selected file in session state
                        st.session_state.selected_file = selected_file
                        
                        # Show analysis results if available for this file
                        analysis_key = f"analysis_result_{selected_file}"
                        if analysis_key in st.session_state:
                            analysis_result = st.session_state[analysis_key]
                            
                            if analysis_result["success"]:
                                # Show detailed file metadata after analysis
                                try:
                                    with open(selected_file, 'r') as f:
                                        report_data = json.load(f)
                                    
                                    metadata = report_data.get('metadata', {})
                                    
                                    st.markdown("### 📊 Detailed File Metadata")
                                    st.markdown(f"""
                                    **Report Details:**
                                    - Generated: {metadata.get('generated_at', 'Unknown')}
                                    - Evaluations: {metadata.get('total_evaluations', 'Unknown')}
                                    - Dataset: {metadata.get('dataset', 'Unknown')}
                                    - Status Filter: {metadata.get('filters_applied', {}).get('status', 'All')}
                                    """)
                                except Exception as e:
                                    st.warning(f"Could not read detailed metadata: {e}")
                                
                                st.markdown("### 📈 Analysis Results")
                                st.text(analysis_result["output"])
                                
                                if options.get("resource_groups"):
                                    # Create descriptive label based on resource groups
                                    if 'resource_groups' in st.session_state:
                                        selected_names = []
                                        # Create descriptive label based on resource groups
                                        if 'resource_groups' in st.session_state:
                                            selected_names = []
                                            for rg_guid in options["resource_groups"]:
                                                for rg in st.session_state['resource_groups']:
                                                    if rg['resourceGuid'] == rg_guid:
                                                        selected_names.append(rg['resourceName'])
                                                        break
                                            if len(selected_names) == 1:
                                                label = f"**🔍 Filtered Data ({selected_names[0]}):**"
                                            else:
                                                label = f"**🔍 Filtered Data ({len(selected_names)} groups):**"
                                        else:
                                            label = f"**🔍 Filtered Data ({len(options['resource_groups'])} groups):**"
                                        
                                        st.markdown(label)
                                        
                                        # Create filtered JSON file
                                        filtered_json_filename = generate_filtered_filename(selected_file, options["resource_groups"])
                                        
                                        # Apply the same filtering that was used in analysis
                                        jq_conditions = ' or '.join(f'.resourceGuid == "{g}"' for g in options["resource_groups"])
                                        jq_filter = f'.evaluations |= map(select(.resourceGroups and (.resourceGroups | length > 0) and (.resourceGroups | any({jq_conditions}))))'
                                        
                                        result = subprocess.run(['jq', jq_filter, selected_file], capture_output=True, text=True, timeout=30)
                                        if result.returncode == 0:
                                            with open(filtered_json_filename, 'w') as f:
                                                f.write(result.stdout)
                                            
                                            # Create CSV version of the filtered data
                                            filtered_csv_filename = generate_filtered_filename(selected_file, options["resource_groups"]).replace('.json', '.csv')
                                            
                                            # Convert filtered JSON to CSV
                                            if create_csv_from_json(filtered_json_filename, filtered_csv_filename):
                                                # Show both download links
                                                st.markdown("**📄 Filtered JSON:**")
                                                st.markdown(get_download_link(filtered_json_filename, filtered_json_filename), unsafe_allow_html=True)
                                                
                                                st.markdown("**📊 Filtered CSV:**")
                                                st.markdown(get_download_link(filtered_csv_filename, filtered_csv_filename), unsafe_allow_html=True)
                                        else:
                                            st.error("Failed to create filtered JSON")
                                else:
                                    st.markdown("**📊 CSV Export:**")
                                    # Create CSV from original data
                                    csv_filename = selected_file.replace('.json', '.csv')
                                    if create_csv_from_json(selected_file, csv_filename):
                                        st.markdown(get_download_link(csv_filename, csv_filename), unsafe_allow_html=True)
                            else:
                                st.warning(f"Analysis had issues: {analysis_result['error']}")
                                if analysis_result["output"]:
                                    st.markdown("### 📊 Partial Results")
                                    st.text(analysis_result["output"])
                    elif selected_file:
                        st.warning(f"⚠️ Selected file '{selected_file}' no longer exists. Please refresh the file list or select another file.")
                        # Clear the invalid selection
                        if 'selected_file' in st.session_state:
                            del st.session_state.selected_file
                else:
                    st.warning("No base report files found. Only files with '_all' suffix (containing all data) are shown in this dropdown.")
                
                # Clear results button
                if st.button("🗑️ Clear Analysis Results", use_container_width=True):
                    # Clear all analysis results but keep configuration
                    keys_to_clear = [key for key in st.session_state.keys() if key.startswith('analysis_result_') or key.startswith('selected_file') or key.startswith('output_file')]
                    for key in keys_to_clear:
                        del st.session_state[key]
                    st.success("Analysis results cleared")
        
        # Right column (Information) - positioned after to stay fixed
        with col2:
            # Create a container for the sidebar content to prevent movement
            sidebar_container = st.container()
            
            with sidebar_container:
                # Information panel
                st.header("ℹ️ Information")
                
                # Version information
                st.markdown("**Version:** 2.0.20")
                st.markdown("**Last Updated:** 04/07/2025")
                st.markdown("---")
                st.markdown("**Community tool, not supported by Lacework**")
                st.markdown("---")

                # Make the "How to use" section expandable
                with st.expander("📖 How to use (Click to expand)", expanded=False):
                    st.markdown("### Quick Start Guide")
                    st.markdown("""
                    1. **Configure API Credentials**  
                       Enter your Lacework API Key ID, Secret, Account, and URL in the sidebar, then click "💾 Save Configuration"
                    
                    2. **Generate Non-Compliant Report**  
                       Select your dataset (AWS, Azure, GCP, or K8s), choose time range and severity filter, then click "📋 Generate Compliance Report"
                    
                    3. **Analyse and Filter Reports**  
                       Select a report file from the dropdown and click "🔍 Analyse Selected File" to view detailed metadata and generate filtered downloads
                    
                    4. **Resource Group Filtering (Optional)**  
                       Click "📋 Get Resource Groups from Report" to load available groups, then select specific resource groups to filter analysis results
                    
                    5. **Download Options**  
                       Use the Download Options section to get JSON and CSV versions of your reports
                    """)
                    
                    st.markdown("### Key Features")
                    st.markdown("""
                    - **Non-Compliant Focus:** Defaults to showing only non-compliant resources for better security insights
                    - **Manual Analysis:** Click "Analyse Selected File" to view detailed metadata and generate filtered downloads
                    - **Resource Group Filtering:** Filter results by specific resource groups for targeted analysis
                    - **Multiple Download Formats:** Get both JSON and CSV versions of your reports
                    - **File Management:** Browse, download, and manage recent reports with file size information
                    - **Performance Optimized:** Cached file lists and optimized loading for better performance
                    """)
                    
                    st.markdown("### Tips")
                    st.markdown("""
                    - **UI Performance:** The UI may lag with large files - give it time to process
                    - **Report Generation:** Generate a report first before loading resource groups
                    - **Analysis:** Use "Analyse Selected File" to get detailed insights and filtered downloads
                    - **Resource Groups:** Use resource group filtering to focus on specific environments or teams
                    - **Download Options:** Both JSON and CSV formats are available for all reports
                    - **File Management:** Use the File Management section to clean up old reports
                    """)
                
                st.markdown("---")
                
                # File Management Section - moved to col2
                st.header("📁 File Management")
                
                # File management buttons
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    if st.button("🗑️ Delete All Cached Reports", type="secondary", use_container_width=True):
                        st.session_state.show_delete_confirmation = True
                
                with col2:
                    if st.button("🔄 Refresh File List", use_container_width=True):
                        st.session_state.file_list_needs_refresh = True
                        st.rerun()
                
                # Show confirmation dialog if delete button was clicked
                if st.session_state.get('show_delete_confirmation', False):
                    st.warning("⚠️ **Are you sure you want to delete ALL cached report files?**")
                    st.markdown("This will permanently delete all files starting with 'compliance_report_' and cannot be undone.")
                    
                    confirm_col1, confirm_col2 = st.columns([1, 1])
                    
                    with confirm_col1:
                        if st.button("✅ Yes, Delete All Files", type="primary"):
                            import glob
                            
                            # Find all compliance report files
                            report_files = glob.glob("compliance_report_*")
                            
                            if report_files:
                                try:
                                    deleted_count = 0
                                    for file in report_files:
                                        try:
                                            os.remove(file)
                                            deleted_count += 1
                                        except Exception as e:
                                            st.error(f"Failed to delete {file}: {e}")
                                    
                                    if deleted_count > 0:
                                        st.success(f"✅ Successfully deleted {deleted_count} cached report file(s)")
                                        st.info("💡 The page will refresh to update the file list")
                                        # Clear the confirmation state and mark for refresh
                                        st.session_state.show_delete_confirmation = False
                                        st.session_state.file_list_needs_refresh = True
                                        # Force a rerun to update the UI
                                        st.rerun()
                                    else:
                                        st.warning("No files were deleted")
                                except Exception as e:
                                    st.error(f"Error deleting files: {e}")
                            else:
                                st.info("No cached report files found to delete")
                                st.session_state.show_delete_confirmation = False
                    
                    with confirm_col2:
                        if st.button("❌ Cancel", type="secondary"):
                            st.session_state.show_delete_confirmation = False
                            st.rerun()
                
                # Download Options Section
                st.markdown("---")
                st.header("📥 Download Options")
                
                # Check if a file is selected
                if 'selected_file' in st.session_state and st.session_state.selected_file and os.path.exists(st.session_state.selected_file):
                    selected_file = st.session_state.selected_file
                    
                    # Show base report download
                    file_size = os.path.getsize(selected_file)
                    size_str = format_file_size(file_size)
                    
                    st.markdown(f"**📄 Base Report JSON (All Data) - {size_str}:**")
                    st.markdown(get_download_link(selected_file, selected_file), unsafe_allow_html=True)
                    
                    # Show CSV export for base report
                    csv_filename = selected_file.replace('.json', '.csv')
                    if create_csv_from_json(selected_file, csv_filename):
                        # Get CSV file size
                        if os.path.exists(csv_filename):
                            csv_size = os.path.getsize(csv_filename)
                            csv_size_str = format_file_size(csv_size)
                        else:
                            csv_size_str = "N/A"
                        
                        st.markdown(f"**📊 Base Report CSV (All Data)  - {csv_size_str}:**")
                        st.markdown(get_download_link(csv_filename, csv_filename), unsafe_allow_html=True)
                    
                    # Show filtered downloads if resource groups are selected
                    if options.get("resource_groups"):
                        # Create descriptive label based on resource groups
                        if 'resource_groups' in st.session_state:
                            selected_names = []
                            for rg_guid in options["resource_groups"]:
                                for rg in st.session_state['resource_groups']:
                                    if rg['resourceGuid'] == rg_guid:
                                        selected_names.append(rg['resourceName'])
                                        break
                            if len(selected_names) == 1:
                                label = f"**🔍 Filtered Data ({selected_names[0]}):**"
                            else:
                                label = f"**🔍 Filtered Data ({len(selected_names)} groups):**"
                        else:
                            label = f"**🔍 Filtered Data ({len(options['resource_groups'])} groups):**"
                        
                        st.markdown(label)
                        
                        # Check if analysis has been performed for this file
                        analysis_key = f"analysis_result_{selected_file}"
                        if analysis_key in st.session_state:
                            analysis_result = st.session_state[analysis_key]
                            if analysis_result["success"]:
                                # Create filtered JSON file
                                filtered_json_filename = generate_filtered_filename(selected_file, options["resource_groups"])
                                
                                # Apply the same filtering that was used in analysis
                                jq_conditions = ' or '.join(f'.resourceGuid == "{g}"' for g in options["resource_groups"])
                                jq_filter = f'.evaluations |= map(select(.resourceGroups and (.resourceGroups | length > 0) and (.resourceGroups | any({jq_conditions}))))'
                                
                                result = subprocess.run(['jq', jq_filter, selected_file], capture_output=True, text=True, timeout=30)
                                if result.returncode == 0:
                                    with open(filtered_json_filename, 'w') as f:
                                        f.write(result.stdout)
                                    
                                    # Create CSV version of the filtered data
                                    filtered_csv_filename = generate_filtered_filename(selected_file, options["resource_groups"]).replace('.json', '.csv')
                                    
                                    # Convert filtered JSON to CSV
                                    if create_csv_from_json(filtered_json_filename, filtered_csv_filename):
                                        # Show both download links with file sizes
                                        # Get filtered JSON file size
                                        if os.path.exists(filtered_json_filename):
                                            json_size = os.path.getsize(filtered_json_filename)
                                            json_size_str = format_file_size(json_size)
                                        else:
                                            json_size_str = "N/A"
                                        
                                        # Get filtered CSV file size
                                        if os.path.exists(filtered_csv_filename):
                                            csv_size = os.path.getsize(filtered_csv_filename)
                                            csv_size_str = format_file_size(csv_size)
                                        else:
                                            csv_size_str = "N/A"
                                        
                                        st.markdown(f"**📄 Filtered JSON - {json_size_str}:**")
                                        st.markdown(get_download_link(filtered_json_filename, filtered_json_filename), unsafe_allow_html=True)
                                        
                                        st.markdown(f"**📊 Filtered CSV - {csv_size_str}:**")
                                        st.markdown(get_download_link(filtered_csv_filename, filtered_csv_filename), unsafe_allow_html=True)
                                else:
                                    st.error("Failed to create filtered JSON")
                        else:
                            st.info("💡 Click 'Analyse Selected File' to generate filtered downloads")
                else:
                    st.info("💡 Select a file from the dropdown to see download options")
                


    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #666;'>Lacework Compliance Reporter - Built with Streamlit</p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 