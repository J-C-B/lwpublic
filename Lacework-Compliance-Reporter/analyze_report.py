import json
from collections import defaultdict
from lacework_compliance_reporter import LaceworkConfig, LaceworkAPI

# Load configuration from config.example.json
try:
    with open('gui_config.json') as f:
        config_data = json.load(f)
    config = LaceworkConfig(
        key_id=config_data['keyId'],
        secret=config_data['secret'],
        account=config_data['account'],
        url=config_data['url']
    )
except FileNotFoundError:
    print("Warning: config.example.json not found. Please create it with your API credentials.")
    print("Example format:")
    print('{"keyId": "YOUR_API_KEY_ID", "secret": "YOUR_API_SECRET", "account": "yourcompany.lacework.net", "url": "https://yourcompany.lacework.net"}')
    exit(1)
except KeyError as e:
    print(f"Error: Missing required field {e} in config.example.json")
    exit(1)

# Change input file to the latest generated report
with open('compliance_report.json') as f:
    report = json.load(f)

# Load resource group definitions from API
api = LaceworkAPI(config)
resource_groups = api.get_resource_groups()

# Create a mapping of group names to their filter criteria
group_filters = {}
for rg in resource_groups:
    group_name = rg.get('name')
    filters = rg.get('query', {}).get('filters', {})
    filter_criteria = []
    
    for filter_name, filter_config in filters.items():
        field = filter_config.get('field')
        operation = filter_config.get('operation')
        values = filter_config.get('values', [])
        key = filter_config.get('key')
        
        if field and values:
            if field in ('Resource Tag', 'Machine Tag') and key:
                filter_criteria.append(f"{field} {key} {operation} {values}")
            else:
                filter_criteria.append(f"{field} {operation} {values}")
    
    group_filters[group_name] = filter_criteria

# Map old group names to new group names
group_name_mapping = {
    'script': 'APS 2',  # ap-southeast-2
    'test group1': 'APS 1'  # ap-southeast-1
}

# Initialize counters
total_evaluations = len(report.get('evaluations', []))
evaluations_with_groups = 0
evaluations_without_groups = 0
resource_group_counts = defaultdict(int)
resource_group_details = {}

# Get metadata from the correct location
metadata = report.get('metadata', {})
total_evaluations = len(report.get('evaluations', []))
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

print("=== COMPLIANCE REPORT SUMMARY ===")
print(f"Total evaluations: {total_evaluations}")
print(f"Report generated: {generated_at}")
print(f"Time range: {time_range_str}")
print(f"Dataset: {dataset}")
print(f"Status filter: {status_filter}")

print("\n=== RESOURCE GROUP ANALYSIS ===")

# Analyze each evaluation
for evaluation in report.get('evaluations', []):
    resource_groups = evaluation.get('resourceGroups', [])
    
    if resource_groups:
        evaluations_with_groups += 1
        for rg in resource_groups:
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

print(f"Evaluations with resource groups: {evaluations_with_groups}")
print(f"Evaluations without resource groups: {evaluations_without_groups}")

print("\n=== RESOURCE GROUP BREAKDOWN ===")
if resource_group_counts:
    for rg_name, count in sorted(resource_group_counts.items(), key=lambda x: x[1], reverse=True):
        details = resource_group_details.get(rg_name, {})
        
        # Map to new group name for filter lookup
        new_group_name = group_name_mapping.get(rg_name, rg_name)
        filters = group_filters.get(new_group_name, [])
        
        print(f"{rg_name} (now: {new_group_name}): {count} resources")
        print(f"  - Type: {details.get('type', 'Unknown')}")
        print(f"  - GUID: {details.get('guid', 'Unknown')}")
        print(f"  - Enabled: {details.get('enabled', 'Unknown')}")
        print(f"  - Default: {details.get('isDefault', 'Unknown')}")
        if filters:
            print(f"  - Filters:")
            for filter_criteria in filters:
                print(f"    * {filter_criteria}")
        else:
            print(f"  - Filters: None (default group)")
        print()
else:
    print("No resource groups found in evaluations")

print("=== SAMPLE RESOURCES ===")
# Show a few sample resources with their groups
samples = 0
for evaluation in report.get('evaluations', []):
    if evaluation.get('resourceGroups') and samples < 3:
        print(f"Resource: {evaluation.get('resource', 'Unknown')}")
        print(f"Groups: {[rg.get('resourceName') for rg in evaluation.get('resourceGroups', [])]}")
        print(f"Region: {evaluation.get('region', 'Unknown')}")
        print(f"Account: {evaluation.get('account', {}).get('AccountId', 'Unknown')}")
        print()
        samples += 1 