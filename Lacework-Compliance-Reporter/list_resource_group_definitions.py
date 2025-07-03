from lacework_compliance_reporter import LaceworkConfig, LaceworkAPI
import json
import os
import sys

def main():
    try:
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
            print("Error: config.example.json not found. Please create it with your API credentials.")
            print("Example format:")
            print('{"keyId": "YOUR_API_KEY_ID", "secret": "YOUR_API_SECRET", "account": "yourcompany.lacework.net", "url": "https://yourcompany.lacework.net"}')
            sys.exit(1)
        except KeyError as e:
            print(f"Error: Missing required field {e} in config.example.json")
            sys.exit(1)
        api = LaceworkAPI(config)
        rgs = api.get_resource_groups()
        
        if not rgs:
            print("No resource groups found.")
            return
        
        for rg in rgs:
            print(f"\nName: {rg.get('name')}")
            print(f"Type: {rg.get('resourceType')}")
            print(f"GUID: {rg.get('resourceGroupGuid')}")
            print("Filters:")
            print(json.dumps(rg.get('query', {}).get('filters', {}), indent=2))
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 