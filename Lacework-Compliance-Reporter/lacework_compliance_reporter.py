#!/usr/bin/env python3
"""
Lacework Compliance Report Downloader

This script downloads compliance violation reports from the Lacework API with filtering
capabilities for resources and policies. It authenticates using keyId and secret.

Usage:
    python lacework_compliance_reporter.py --config config.json
    python lacework_compliance_reporter.py --url https://your-instance.lacework.net --token YOUR_TOKEN
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import requests
from dataclasses import dataclass, asdict
import csv


@dataclass
class LaceworkConfig:
    """Configuration for Lacework API access"""
    keyId: str
    secret: str
    account: str
    url: str
    account_name: Optional[str] = None
    org_access: bool = False


@dataclass
class ComplianceFilter:
    """Filter configuration for compliance reports"""
    dataset: str  # AwsCompliance, AzureCompliance, GcpCompliance, K8sCompliance
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    status_filter: Optional[str] = None  # All, Compliant, NonCompliant (None = All)
    account_ids: Optional[List[str]] = None
    resource_groups: Optional[List[str]] = None
    policy_ids: Optional[List[str]] = None
    severity_levels: Optional[List[str]] = None  # Critical, High, Medium, Low, Info


class LaceworkAPI:
    """Lacework API client with rate limiting and pagination support"""
    
    def __init__(self, config: LaceworkConfig):
        self.config = config
        self.base_url = config.url.rstrip('/')
        self.session = requests.Session()
        self.token = None
        self.token_expiry = None
        self._authenticate()
        if config.account_name:
            self.session.headers['Account-Name'] = config.account_name
        if config.org_access:
            self.session.headers['Org-Access'] = 'true'
        
        # Rate limiting: 480 requests per hour
        self.rate_limit = 480
        self.request_count = 0
        self.last_reset = time.time()
    
    def _authenticate(self):
        logging.info("Authenticating with Lacework API using keyId/secret...")
        logging.debug(f"keyId being used for X-LW-UAKS: {self.config.keyId!r}")
        url = f"{self.base_url}/api/v2/access/tokens"
        payload = {
            "keyId": self.config.keyId,
            "expiryTime": 3600
        }
        headers = {
            "X-LW-UAKS": self.config.secret,
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 201:
            logging.error(f"Failed to authenticate: {response.status_code} {response.text}")
            raise Exception(f"Authentication failed: {response.text}")
        data = response.json()
        self.token = data["token"]
        self.token_expiry = data["expiresAt"]
        self.session.headers.update({
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        })
        logging.info("Authentication successful.")
    
    def _check_token(self):
        # If token is expired or about to expire, re-authenticate
        if not self.token or not self.token_expiry:
            self._authenticate()
            return
        expiry = datetime.strptime(self.token_expiry, "%Y-%m-%dT%H:%M:%S.%fZ")
        if (expiry - datetime.utcnow()).total_seconds() < 60:
            self._authenticate()
    
    def _check_rate_limit(self):
        """Check and handle rate limiting"""
        current_time = time.time()
        if current_time - self.last_reset >= 3600:  # Reset every hour
            self.request_count = 0
            self.last_reset = current_time
        
        if self.request_count >= self.rate_limit:
            sleep_time = 3600 - (current_time - self.last_reset)
            logging.warning(f"Rate limit reached. Sleeping for {sleep_time:.0f} seconds")
            time.sleep(sleep_time)
            self.request_count = 0
            self.last_reset = time.time()
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API request with rate limiting and error handling"""
        self._check_token()
        self._check_rate_limit()
        
        url = f"{self.base_url}{endpoint}"
        logging.debug(f"Making {method} request to: {url}")
        if 'json' in kwargs:
            logging.debug(f"Request payload: {json.dumps(kwargs['json'], indent=2)}")
        
        try:
            response = self.session.request(method, url, **kwargs)
            self.request_count += 1
            
            logging.debug(f"Response status: {response.status_code}")
            logging.debug(f"Response headers: {dict(response.headers)}")
            
            # Handle rate limiting headers
            if 'RateLimit-Remaining' in response.headers:
                remaining = int(response.headers['RateLimit-Remaining'])
                logging.debug(f"Rate limit remaining: {remaining}")
            
            response.raise_for_status()
            
            # Handle empty responses gracefully
            if not response.text.strip():
                logging.warning(f"Empty response received from {endpoint}")
                logging.debug(f"Empty response details - Status: {response.status_code}, Headers: {dict(response.headers)}")
                return {'data': []}
            
            try:
                return response.json()
            except json.JSONDecodeError as json_error:
                logging.error(f"Failed to parse JSON response from {endpoint}: {json_error}")
                logging.error(f"Response text: {response.text[:500]}...")  # Log first 500 chars
                logging.debug(f"Full response text: {response.text}")
                # Return empty data structure instead of raising
                return {'data': []}
        
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logging.error(f"Response status: {e.response.status_code}")
                logging.error(f"Response body: {e.response.text}")
            raise
    
    def get_resource_groups(self) -> List[Dict[str, Any]]:
        """Get all resource groups"""
        logging.info("Fetching resource groups...")
        response = self._make_request('GET', '/api/v2/ResourceGroups')
        return response.get('data', [])
    
    def get_resource_group_details(self, resource_guid: str) -> Dict[str, Any]:
        """Get details for a specific resource group"""
        logging.info(f"Fetching resource group details for {resource_guid}...")
        response = self._make_request('GET', f'/api/v2/ResourceGroups/{resource_guid}')
        return response.get('data', {})
    
    def get_policies(self) -> List[Dict[str, Any]]:
        """Get all policies"""
        logging.info("Fetching policies...")
        response = self._make_request('GET', '/api/v2/Policies')
        return response.get('data', [])
    
    def search_policies(self, filters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Search policies with filters"""
        logging.info("Searching policies with filters...")
        payload = {'filters': filters}
        response = self._make_request('POST', '/api/v2/Policies/search', json=payload)
        return response.get('data', [])
    
    def search_compliance_evaluations(self, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search compliance evaluations with pagination support"""
        logging.info("Searching compliance evaluations...")
        logging.debug(f"API Query Payload: {json.dumps(payload, indent=2)}")
        
        all_results = []
        next_page_url = None
        
        # Initial request
        response = self._make_request('POST', '/api/v2/Configs/ComplianceEvaluations/search', json=payload)
        data = response.get('data', [])
        logging.debug(f"API Response - Total results: {len(data)}, Response keys: {list(response.keys())}")
        
        if not data:
            logging.debug(f"Empty data response. Full response structure: {json.dumps(response, indent=2)}")
        
        all_results.extend(data)
        
        # Handle pagination
        paging = response.get('paging', {})
        if paging and 'urls' in paging and 'nextPage' in paging['urls']:
            next_page_url = paging['urls']['nextPage']
        
        # Fetch subsequent pages
        while next_page_url:
            logging.info(f"Fetching next page: {next_page_url}")
            try:
                # Extract the path from the full URL
                path = next_page_url.replace(self.base_url, '')
                response = self._make_request('GET', path)
                data = response.get('data', [])
                all_results.extend(data)
                
                paging = response.get('paging', {})
                if paging and 'urls' in paging and 'nextPage' in paging['urls']:
                    next_page_url = paging['urls']['nextPage']
                else:
                    next_page_url = None
                    
            except Exception as e:
                logging.error(f"Error fetching next page: {e}")
                break
        
        logging.info(f"Total compliance evaluations retrieved: {len(all_results)}")
        return all_results


class ComplianceReporter:
    """Main compliance reporting class"""
    
    def __init__(self, config: LaceworkConfig):
        self.config = config
        self.api = LaceworkAPI(config)
        self.resource_groups_cache = {}
        self.policies_cache = {}
    
    def _parse_aws_arn(self, arn: str) -> Dict[str, Any]:
        """Parse AWS ARN to extract components"""
        try:
            # Format: arn:partition:service:region:account-id:resource
            parts = arn.split(':')
            if len(parts) >= 6 and parts[0] == 'arn':
                return {
                    'partition': parts[1],
                    'service': parts[2],
                    'region': parts[3],
                    'accountId': parts[4],
                    'resource': ':'.join(parts[5:]),
                    'resourceType': parts[2].upper()  # e.g., 'iam' -> 'IAM'
                }
        except:
            pass
        return {}

    def _resource_matches_group_by_arn(self, resource_info: Dict[str, Any], resource_group: Dict[str, Any]) -> bool:
        """Check if a resource matches a resource group's criteria based on ARN parsing"""
        query = resource_group.get('query', {})
        filters = query.get('filters', {})
        
        # Track if we have any non-wildcard filters that we can evaluate
        has_evaluable_filters = False
        all_filters_wildcard = True
        
        # Check each filter in the resource group
        for filter_name, filter_config in filters.items():
            field = filter_config.get('field')
            operation = filter_config.get('operation')
            values = filter_config.get('values', [])
            key = filter_config.get('key')
            
            if not field or not values:
                continue
            
            # Skip wildcard filters for evaluation
            if '*' in values:
                continue
            
            all_filters_wildcard = False
            
            # Handle different field types based on what we can extract from ARN
            if field == 'Account':
                has_evaluable_filters = True
                resource_value = resource_info.get('accountId')
                if operation == 'EQUALS' and resource_value not in values:
                    return False
            elif field == 'Region':
                has_evaluable_filters = True
                resource_value = resource_info.get('region')
                if operation == 'EQUALS' and resource_value not in values:
                    return False
            elif field in ('Resource Tag', 'Machine Tag'):
                # Can't match tags from compliance report - need inventory API
                # For now, skip tag-based matching
                continue
            else:
                # Skip other fields we can't match from ARN
                continue
        
        # If all filters are wildcard, don't match by default
        # Only match if we have specific criteria that were met
        if all_filters_wildcard:
            return False
        
        # If we have evaluable filters and none failed, it's a match
        return has_evaluable_filters
    
    def _load_resource_groups_cache(self):
        """Load resource groups into cache"""
        if not self.resource_groups_cache:
            resource_groups = self.api.get_resource_groups()
            for rg in resource_groups:
                guid = rg.get('resourceGroupGuid')
                if guid:  # Only add if GUID is not None
                    self.resource_groups_cache[guid] = rg
            logging.info(f"Loaded {len(self.resource_groups_cache)} resource groups into cache")
    
    def _load_policies_cache(self):
        """Load policies into cache"""
        if not self.policies_cache:
            policies = self.api.get_policies()
            for policy in policies:
                self.policies_cache[policy.get('policyId')] = policy
    
    def _filter_by_resource_groups(self, evaluations: List[Dict[str, Any]], 
                                 resource_group_guids: List[str]) -> List[Dict[str, Any]]:
        """Filter compliance evaluations by resource groups"""
        if not resource_group_guids:
            return evaluations
        
        self._load_resource_groups_cache()
        
        # Get resource group details to understand what resources they contain
        filtered_evaluations = []
        
        for evaluation in evaluations:
            # Check if the evaluation's resources are in any of the specified resource groups
            evaluation_resources = evaluation.get('resources', [])
            
            for resource in evaluation_resources:
                resource_id = resource.get('resourceId')
                if not resource_id:
                    continue
                
                # Check if this resource belongs to any of the specified resource groups
                for rg_guid in resource_group_guids:
                    if rg_guid in self.resource_groups_cache:
                        rg_details = self.resource_groups_cache[rg_guid]
                        # This is a simplified check - in practice, you'd need to match
                        # based on the resource group's criteria (account IDs, tags, etc.)
                        if self._resource_matches_group(resource_id, rg_details):
                            filtered_evaluations.append(evaluation)
                            break
                else:
                    continue
                break
        
        logging.info(f"Filtered evaluations by resource groups: {len(filtered_evaluations)} out of {len(evaluations)}")
        return filtered_evaluations
    
    def _get_resource_groups_for_evaluation(self, evaluation: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get resource groups that contain the resources in this evaluation"""
        if not self.resource_groups_cache:
            self._load_resource_groups_cache()
        
        matching_resource_groups = []
        
        # Handle both 'resource' (singular) and 'resources' (array) fields
        if 'resource' in evaluation:
            # Single resource case - parse ARN and match based on account/region
            resource_arn = evaluation.get('resource', '')
            if resource_arn:
                resource_info = self._parse_aws_arn(resource_arn)
                if resource_info:
                    matching_resource_groups.extend(self._find_matching_resource_groups_by_arn(resource_info))
        elif 'resources' in evaluation:
            # Multiple resources case
            evaluation_resources = evaluation.get('resources', [])
            for resource in evaluation_resources:
                resource_id = resource.get('resourceId', '')
                if resource_id:
                    resource_info = self._parse_aws_arn(resource_id)
                    if resource_info:
                        matching_resource_groups.extend(self._find_matching_resource_groups_by_arn(resource_info))
        
        # Remove duplicates while preserving order
        seen = set()
        unique_resource_groups = []
        for rg in matching_resource_groups:
            rg_key = rg.get('resourceGuid')
            if rg_key not in seen:
                seen.add(rg_key)
                unique_resource_groups.append(rg)
        
        return unique_resource_groups

    def _find_matching_resource_groups_by_arn(self, resource_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find resource groups that match a given resource based on ARN parsing"""
        matching_resource_groups = []
        
        for rg_guid, rg_details in self.resource_groups_cache.items():
            if self._resource_matches_group_by_arn(resource_info, rg_details):
                rg_info = {
                    'resourceGuid': rg_guid,
                    'resourceName': rg_details.get('name'),
                    'resourceType': rg_details.get('resourceType'),
                    'enabled': rg_details.get('enabled'),
                    'isDefault': rg_details.get('isDefaultBoolean')
                }
                matching_resource_groups.append(rg_info)
        
        return matching_resource_groups
    
    def _filter_by_policies(self, evaluations: List[Dict[str, Any]], 
                          policy_ids: List[str]) -> List[Dict[str, Any]]:
        """Filter compliance evaluations by policies"""
        if not policy_ids:
            return evaluations
        
        self._load_policies_cache()
        
        filtered_evaluations = []
        for evaluation in evaluations:
            evaluation_policy_id = evaluation.get('policyId')
            if evaluation_policy_id in policy_ids:
                filtered_evaluations.append(evaluation)
        
        logging.info(f"Filtered evaluations by policies: {len(filtered_evaluations)} out of {len(evaluations)}")
        return filtered_evaluations
    
    def generate_compliance_report(self, filter_config: ComplianceFilter, 
                                 output_format: str = 'json') -> Dict[str, Any]:
        """Generate comprehensive compliance report"""
        logging.info("Generating compliance report...")
        
        # Build search payload
        payload = {
            'dataset': filter_config.dataset,
            'returns': [
                'account', 'id', 'recommendation', 'severity', 'status', 
                'resource', 'region', 'section', 'evalType', 'reason', 'reportTime'
            ]
        }
        
        # Add time filter
        if filter_config.start_time or filter_config.end_time:
            payload['timeFilter'] = {}
            if filter_config.start_time:
                payload['timeFilter']['startTime'] = filter_config.start_time
            if filter_config.end_time:
                payload['timeFilter']['endTime'] = filter_config.end_time
        
        # Add filters
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
        
        # Get compliance evaluations
        evaluations = self.api.search_compliance_evaluations(payload)
        
        # Apply resource group filtering
        if filter_config.resource_groups:
            evaluations = self._filter_by_resource_groups(evaluations, filter_config.resource_groups)
        
        # Apply policy filtering
        if filter_config.policy_ids:
            evaluations = self._filter_by_policies(evaluations, filter_config.policy_ids)
        
        # Add resource group information to each evaluation
        logging.info("Adding resource group information to evaluations...")
        for evaluation in evaluations:
            resource_groups = self._get_resource_groups_for_evaluation(evaluation)
            evaluation['resourceGroups'] = resource_groups
        
        # Build report
        report = {
            'metadata': {
                'generated_at': datetime.utcnow().isoformat() + 'Z',
                'total_evaluations': len(evaluations),
                'dataset': filter_config.dataset,
                'time_range': {
                    'start_time': filter_config.start_time,
                    'end_time': filter_config.end_time
                },
                'filters_applied': {
                    'status': filter_config.status_filter,
                    'account_ids': filter_config.account_ids,
                    'resource_groups': filter_config.resource_groups,
                    'policy_ids': filter_config.policy_ids,
                    'severity_levels': filter_config.severity_levels
                }
            },
            'evaluations': evaluations
        }
        
        return report
    
    def save_report(self, report: Dict[str, Any], output_file: str, 
                   output_format: str = 'json'):
        """Save report to file"""
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        
        if output_format.lower() == 'json':
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
        
        elif output_format.lower() == 'csv':
            self._save_csv_report(report, output_file)
        
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
        
        logging.info(f"Report saved to: {output_file}")
    
    def _save_csv_report(self, report: Dict[str, Any], output_file: str):
        """Save report as CSV"""
        evaluations = report.get('evaluations', [])
        
        if not evaluations:
            logging.warning("No evaluations to save to CSV")
            return
        
        # Determine CSV headers based on the first evaluation
        first_eval = evaluations[0]
        headers = self._flatten_dict_keys(first_eval)
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            
            for evaluation in evaluations:
                flattened = self._flatten_dict(evaluation)
                writer.writerow(flattened)
    
    def _flatten_dict_keys(self, d: Dict[str, Any], parent_key: str = '') -> List[str]:
        """Get flattened keys from a nested dictionary"""
        keys = []
        for k, v in d.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict):
                keys.extend(self._flatten_dict_keys(v, new_key))
            elif isinstance(v, list):
                keys.append(new_key)
            else:
                keys.append(new_key)
        return keys
    
    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = '') -> Dict[str, Any]:
        """Flatten a nested dictionary"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key).items())
            elif isinstance(v, list):
                items.append((new_key, json.dumps(v)))
            else:
                items.append((new_key, v))
        return dict(items)


def load_config_from_file(config_file: str) -> LaceworkConfig:
    """Load configuration from JSON file"""
    with open(config_file, 'r') as f:
        config_data = json.load(f)
    
    return LaceworkConfig(
        keyId=config_data['keyId'],
        secret=config_data['secret'],
        account=config_data['account'],
        url=config_data['url'],
        account_name=config_data.get('account_name'),
        org_access=config_data.get('org_access', False)
    )


def parse_time_range(time_range: str) -> tuple:
    """Parse time range string (e.g., '24h', '7d', '30d')"""
    if not time_range:
        return None, None
    
    now = datetime.utcnow()
    
    if time_range.endswith('h'):
        hours = int(time_range[:-1])
        start_time = now - timedelta(hours=hours)
    elif time_range.endswith('d'):
        days = int(time_range[:-1])
        start_time = now - timedelta(days=days)
    else:
        raise ValueError(f"Invalid time range format: {time_range}")
    
    return start_time.isoformat() + 'Z', now.isoformat() + 'Z'


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Lacework Compliance Report Downloader')
    parser.add_argument('--config', help='Configuration file (JSON)')
    parser.add_argument('--url', help='Lacework instance URL')
    parser.add_argument('--token', help='API access token')
    parser.add_argument('--account-name', help='Account name (for sub-accounts)')
    parser.add_argument('--org-access', action='store_true', help='Use organization-level access')
    
    parser.add_argument('--dataset', required=True, 
                       choices=['AwsCompliance', 'AzureCompliance', 'GcpCompliance', 'K8sCompliance'],
                       help='Compliance dataset to query')
    parser.add_argument('--time-range', help='Time range (e.g., 24h, 7d, 30d)')
    parser.add_argument('--start-time', help='Start time (ISO format)')
    parser.add_argument('--end-time', help='End time (ISO format)')
    parser.add_argument('--status', choices=['All', 'Compliant', 'NonCompliant'], help='Filter by status (All shows all evaluations)')
    parser.add_argument('--account-ids', nargs='+', help='Filter by account IDs')
    parser.add_argument('--resource-groups', nargs='+', help='Filter by resource group GUIDs')
    parser.add_argument('--policy-ids', nargs='+', help='Filter by policy IDs')
    parser.add_argument('--severity', nargs='+', 
                       choices=['Critical', 'High', 'Medium', 'Low', 'Info'],
                       help='Filter by severity levels')
    
    parser.add_argument('--output', default='compliance_report.json', help='Output file path')
    parser.add_argument('--format', choices=['json', 'csv'], default='json', help='Output format')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Load configuration
    if args.config:
        config = load_config_from_file(args.config)
    elif args.url and args.token:
        config = LaceworkConfig(
            keyId=args.token,
            secret=args.token,
            account=args.token,
            url=args.url,
            account_name=args.account_name,
            org_access=args.org_access
        )
    else:
        logging.error("Either --config or both --url and --token must be provided")
        sys.exit(1)
    
    # Parse time range
    start_time = args.start_time
    end_time = args.end_time
    if args.time_range and not (start_time or end_time):
        start_time, end_time = parse_time_range(args.time_range)
    
    # Create filter configuration
    filter_config = ComplianceFilter(
        dataset=args.dataset,
        start_time=start_time,
        end_time=end_time,
        status_filter=args.status if args.status != "All" else None,
        account_ids=args.account_ids,
        resource_groups=args.resource_groups,
        policy_ids=args.policy_ids,
        severity_levels=args.severity
    )
    
    try:
        # Create reporter and generate report
        reporter = ComplianceReporter(config)
        report = reporter.generate_compliance_report(filter_config, args.format)
        
        # Save report
        reporter.save_report(report, args.output, args.format)
        
        logging.info("Compliance report generation completed successfully")
        
    except Exception as e:
        logging.error(f"Error generating compliance report: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 