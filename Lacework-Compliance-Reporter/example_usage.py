#!/usr/bin/env python3
"""
Lacework Compliance Reporter v2.0.6 - Example Usage

This script demonstrates how to use the Lacework Compliance Reporter both programmatically
and through the web interface. The current implementation focuses on a Streamlit-based
web application with enhanced resource group filtering and analysis capabilities.

For the best user experience, use the web interface:
    streamlit run streamlit_app.py
"""

import json
import logging
import os
from datetime import datetime, timedelta
from lacework_compliance_reporter import LaceworkConfig, ComplianceFilter, ComplianceReporter

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def example_web_interface_usage():
    """Example: How to use the web interface (Recommended)"""
    print("=== Web Interface Usage (Recommended) ===")
    print("1. Launch the web application:")
    print("   # Standard launch")
    print("   streamlit run streamlit_app.py")
    print()
    print("   # For large files (recommended for production)")
    print("   streamlit run streamlit_app.py --server.maxMessageSize 500")
    print()
    print("2. Configure API credentials in the sidebar:")
    print("   - Enter your Lacework API Key ID, Secret, Account, and URL")
    print("   - Click '💾 Save Configuration'")
    print()
    print("3. Generate a Non-Compliant Report:")
    print("   - Select dataset (AWS, Azure, GCP, or K8s)")
    print("   - Choose time range (24h, 7d, 30d)")
    print("   - Select severity levels (defaults to Critical and High)")
    print("   - Click '📋 Generate Compliance Report'")
    print()
    print("4. Analyse and Filter Reports:")
    print("   - Select a report file from the dropdown")
    print("   - Click '🔍 Analyse Selected File' for detailed metadata")
    print("   - Use resource group filtering for targeted analysis")
    print()
    print("5. Download Options:")
    print("   - Base Report JSON and CSV formats")
    print("   - Filtered reports by resource groups")
    print("   - File size information for all downloads")
    print()

def example_basic_programmatic_usage():
    """Example: Basic programmatic usage for automation"""
    print("=== Example 1: Basic Programmatic Usage ===")
    
    # Configuration
    config = LaceworkConfig(
        keyId="your-api-key-id-here",
        secret="your-api-secret-here",
        account="your-account-id-here",
        url="https://your-instance.lacework.net"
    )
    
    # Filter configuration - matches current UI defaults
    filter_config = ComplianceFilter(
        dataset="AwsCompliance",
        start_time=(datetime.utcnow() - timedelta(days=7)).isoformat() + 'Z',
        end_time=datetime.utcnow().isoformat() + 'Z',
        status_filter="NonCompliant",  # Current UI default
        severity_levels=["Critical", "High"]  # Current UI default
    )
    
    try:
        # Generate report
        reporter = ComplianceReporter(config)
        report = reporter.generate_compliance_report(filter_config)
        
        # Save report with timestamp (matches web interface format)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"compliance_report_{timestamp}_all.json"
        reporter.save_report(report, filename, "json")
        
        print(f"✅ Report generated successfully!")
        print(f"📄 File: {filename}")
        print(f"📊 Evaluations: {report['metadata']['total_evaluations']}")
        print(f"🔍 Dataset: {report['metadata']['dataset']}")
        print(f"⏰ Time Range: {report['metadata']['filters_applied']['time_range']}")
        
    except Exception as e:
        print(f"❌ Error generating report: {e}")

def example_multi_cloud_automation():
    """Example: Automated multi-cloud compliance reporting"""
    print("\n=== Example 2: Multi-Cloud Automation ===")
    
    # Configuration
    config = LaceworkConfig(
        keyId="your-api-key-id-here",
        secret="your-api-secret-here",
        account="your-account-id-here",
        url="https://your-instance.lacework.net"
    )
    
    # Cloud providers to check
    cloud_providers = ["AwsCompliance", "AzureCompliance", "GcpCompliance", "K8sCompliance"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for provider in cloud_providers:
        print(f"🔍 Generating {provider} report...")
        
        try:
            filter_config = ComplianceFilter(
                dataset=provider,
                start_time=(datetime.utcnow() - timedelta(days=7)).isoformat() + 'Z',
                end_time=datetime.utcnow().isoformat() + 'Z',
                status_filter="NonCompliant",
                severity_levels=["Critical", "High"]
            )
            
            reporter = ComplianceReporter(config)
            report = reporter.generate_compliance_report(filter_config)
            
            # Save with provider-specific naming
            filename = f"compliance_report_{timestamp}_{provider.lower()}_all.json"
            reporter.save_report(report, filename, "json")
            
            print(f"  ✅ {provider}: {report['metadata']['total_evaluations']} evaluations")
            print(f"  📄 Saved: {filename}")
            
        except Exception as e:
            print(f"  ❌ {provider}: Error - {e}")

def example_resource_group_analysis():
    """Example: Analyze resource group data from existing reports"""
    print("\n=== Example 3: Resource Group Analysis ===")
    
    # This example shows how to analyze resource group data from existing reports
    # This matches the functionality available in the web interface
    
    def analyze_resource_groups_from_file(filename):
        """Analyze resource groups from a compliance report file"""
        try:
            with open(filename, 'r') as f:
                report = json.load(f)
            
            evaluations = report.get('evaluations', [])
            
            # Count evaluations with and without resource groups
            with_groups = 0
            without_groups = 0
            resource_group_counts = {}
            
            for evaluation in evaluations:
                resource_groups = evaluation.get('resourceGroups', [])
                if resource_groups:
                    with_groups += 1
                    for rg in resource_groups:
                        rg_name = rg.get('resourceName', 'Unknown')
                        resource_group_counts[rg_name] = resource_group_counts.get(rg_name, 0) + 1
                else:
                    without_groups += 1
            
            print(f"📊 Analysis of {filename}:")
            print(f"  Total evaluations: {len(evaluations)}")
            print(f"  With resource groups: {with_groups}")
            print(f"  Without resource groups: {without_groups}")
            
            if resource_group_counts:
                print(f"  Resource group breakdown:")
                for rg_name, count in sorted(resource_group_counts.items(), key=lambda x: x[1], reverse=True):
                    print(f"    {rg_name}: {count} evaluations")
            
            return resource_group_counts
            
        except FileNotFoundError:
            print(f"❌ File not found: {filename}")
            return {}
        except Exception as e:
            print(f"❌ Error analyzing {filename}: {e}")
            return {}
    
    # Look for existing compliance reports
    import glob
    report_files = glob.glob("compliance_report_*.json")
    
    if report_files:
        # Analyze the most recent report
        latest_report = max(report_files, key=os.path.getctime)
        analyze_resource_groups_from_file(latest_report)
    else:
        print("📝 No compliance reports found. Generate a report first using the web interface.")

def example_csv_export_automation():
    """Example: Automated CSV export for reporting"""
    print("\n=== Example 4: CSV Export Automation ===")
    
    # Configuration
    config = LaceworkConfig(
        keyId="your-api-key-id-here",
        secret="your-api-secret-here",
        account="your-account-id-here",
        url="https://your-instance.lacework.net"
    )
    
    try:
        # Generate report for CSV export
        filter_config = ComplianceFilter(
            dataset="AwsCompliance",
            start_time=(datetime.utcnow() - timedelta(days=7)).isoformat() + 'Z',
            end_time=datetime.utcnow().isoformat() + 'Z',
            status_filter="NonCompliant",
            severity_levels=["Critical", "High"]
        )
        
        reporter = ComplianceReporter(config)
        report = reporter.generate_compliance_report(filter_config)
        
        # Save both JSON and CSV formats
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_filename = f"compliance_report_{timestamp}_all.json"
        csv_filename = f"compliance_report_{timestamp}_all.csv"
        
        reporter.save_report(report, json_filename, "json")
        reporter.save_report(report, csv_filename, "csv")
        
        print(f"✅ Reports exported successfully!")
        print(f"📄 JSON: {json_filename}")
        print(f"📊 CSV: {csv_filename}")
        print(f"📈 Evaluations: {report['metadata']['total_evaluations']}")
        
    except Exception as e:
        print(f"❌ Error exporting reports: {e}")

def example_configuration_management():
    """Example: Configuration management and validation"""
    print("\n=== Example 5: Configuration Management ===")
    
    def load_config_from_file(filename):
        """Load configuration from file (matches web interface functionality)"""
        try:
            with open(filename, 'r') as f:
                config_data = json.load(f)
            
            # Validate required fields
            required_fields = ['keyId', 'secret', 'account', 'url']
            missing_fields = [field for field in required_fields if not config_data.get(field)]
            
            if missing_fields:
                raise ValueError(f"Missing required fields: {missing_fields}")
            
            return LaceworkConfig(
                keyId=config_data['keyId'],
                secret=config_data['secret'],
                account=config_data['account'],
                url=config_data['url']
            )
            
        except FileNotFoundError:
            print(f"❌ Configuration file not found: {filename}")
            return None
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in configuration file: {filename}")
            return None
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            return None
    
    def save_config_to_file(config, filename):
        """Save configuration to file (matches web interface functionality)"""
        try:
            config_data = {
                'keyId': config.keyId,
                'secret': config.secret,
                'account': config.account,
                'url': config.url
            }
            
            with open(filename, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            print(f"✅ Configuration saved to {filename}")
            
        except Exception as e:
            print(f"❌ Error saving configuration: {e}")
    
    # Example: Load configuration from file
    config = load_config_from_file("config.json")
    
    if config:
        print("✅ Configuration loaded successfully")
        print(f"   Account: {config.account}")
        print(f"   URL: {config.url}")
        
        # Example: Save configuration to a different file
        save_config_to_file(config, "config_backup.json")
    else:
        print("📝 Create a config.json file with your Lacework credentials:")
        print("""
        {
          "keyId": "your-api-key-id",
          "secret": "your-api-secret",
          "account": "yourcompany.lacework.net",
          "url": "https://yourcompany.lacework.net"
        }
        """)

def example_error_handling():
    """Example: Error handling and validation"""
    print("\n=== Example 6: Error Handling ===")
    
    def safe_report_generation(config, filter_config, filename):
        """Safely generate a compliance report with error handling"""
        try:
            reporter = ComplianceReporter(config)
            report = reporter.generate_compliance_report(filter_config)
            
            # Check if report has data
            total_evaluations = report['metadata']['total_evaluations']
            
            if total_evaluations == 0:
                print(f"⚠️  Report generated but contains no evaluations")
                print(f"   This is normal if no resources match your filter criteria")
            else:
                print(f"✅ Report generated successfully with {total_evaluations} evaluations")
            
            reporter.save_report(report, filename, "json")
            return True
            
        except Exception as e:
            print(f"❌ Error generating report: {e}")
            return False
    
    # Example configuration (you would use real credentials)
    config = LaceworkConfig(
        keyId="invalid-key",
        secret="invalid-secret",
        account="invalid-account",
        url="https://invalid-url.com"
    )
    
    filter_config = ComplianceFilter(
        dataset="AwsCompliance",
        start_time=(datetime.utcnow() - timedelta(days=7)).isoformat() + 'Z',
        end_time=datetime.utcnow().isoformat() + 'Z',
        status_filter="NonCompliant"
    )
    
    # This will fail due to invalid credentials, demonstrating error handling
    success = safe_report_generation(config, filter_config, "test_report.json")
    
    if not success:
        print("💡 To fix this error, use valid Lacework API credentials")

def main():
    """Main function to demonstrate usage"""
    print("🔒 Lacework Compliance Reporter v2.0.6 - Example Usage")
    print("=" * 60)
    print("Community tool, not supported by Lacework")
    print()
    
    # Show web interface usage (recommended)
    example_web_interface_usage()
    
    # Show programmatic examples
    print("=== Programmatic Usage Examples ===")
    print("The following examples demonstrate programmatic usage for automation.")
    print("For most users, the web interface is recommended for better UX.")
    print()
    
    # Note: These examples require valid Lacework credentials
    # Uncomment the examples you want to run and update the configuration
    
    # example_basic_programmatic_usage()
    # example_multi_cloud_automation()
    # example_resource_group_analysis()
    # example_csv_export_automation()
    # example_configuration_management()
    # example_error_handling()
    
    print("📋 To run these examples:")
    print("1. Update the configuration with your Lacework API credentials")
    print("2. Create a config.json file (see config.example.json)")
    print("3. Uncomment the example functions you want to run")
    print("4. Run: python example_usage.py")
    print()
    print("🔑 Required credentials:")
    print("   - keyId: Your Lacework API key ID")
    print("   - secret: Your Lacework API secret")
    print("   - account: Your Lacework account domain")
    print("   - url: Your Lacework instance URL")
    print()
    print("🌐 For the best experience, use the web interface:")
    print("   # Standard launch")
    print("   streamlit run streamlit_app.py")
    print("   # For large files")
    print("   streamlit run streamlit_app.py --server.maxMessageSize 500")

if __name__ == '__main__':
    main() 