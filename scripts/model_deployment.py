#!/usr/bin/env python3
"""
Model Deployment Helper Script

This script can be used independently or as part of GitHub Actions workflow
to register or update models via API calls.
"""

import json
import requests
import os
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, Optional


class ModelDeploymentClient:
    """Client for interacting with model deployment APIs"""
    
    def __init__(self, api_url: str, api_token: str):
        self.api_url = api_url.rstrip('/')
        self.api_token = api_token
        self.headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }
    
    def register_model(self, config: Dict[str, Any]) -> bool:
        """Register a new model"""
        register_url = f"{self.api_url}/v1/models/register"
        
        print(f"🚀 Registering model: {config['model_name']} (variant: {config['variant']})")
        print(f"📡 API URL: {register_url}")
        
        try:
            response = requests.post(register_url, json=config, headers=self.headers)
            
            if response.status_code in [200, 201]:
                print("✅ Model registered successfully!")
                if response.content:
                    try:
                        response_data = response.json()
                        print(f"📄 Response: {json.dumps(response_data, indent=2)}")
                    except json.JSONDecodeError:
                        print(f"📄 Response: {response.text}")
                return True
            else:
                print(f"❌ Failed to register model. Status: {response.status_code}")
                print(f"📄 Response: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            return False
    
    def update_model(self, config: Dict[str, Any], model_id: Optional[str] = None) -> bool:
        """Update an existing model"""
        if not model_id:
            # Construct model identifier from config
            model_id = f"CD:{config['owner_team']}:{config['model_name']}:{config['variant']}"
        
        # Create update payload (only serving_configuration)
        update_payload = {
            "model": {
                "serving_configuration": config.get("serving_configuration", {})
            }
        }
        
        update_url = f"{self.api_url}/v1/models/update/{model_id}"
        
        print(f"🔄 Updating model: {model_id}")
        print(f"📡 API URL: {update_url}")
        
        try:
            response = requests.put(update_url, json=update_payload, headers=self.headers)
            
            if response.status_code in [200, 201]:
                print("✅ Model updated successfully!")
                if response.content:
                    try:
                        response_data = response.json()
                        print(f"📄 Response: {json.dumps(response_data, indent=2)}")
                    except json.JSONDecodeError:
                        print(f"📄 Response: {response.text}")
                return True
            else:
                print(f"❌ Failed to update model. Status: {response.status_code}")
                print(f"📄 Response: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            return False


def load_model_config(config_path: str) -> Dict[str, Any]:
    """Load model configuration from JSON file"""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Configuration file not found: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in configuration file: {e}")
        sys.exit(1)


def create_default_config(model_name: str, variant: str) -> Dict[str, Any]:
    """Create a default model configuration"""
    return {
        "model_name": model_name,
        "variant": variant,
        "owner_team": "personalization",
        "omd_business_service": "content-discovery",
        "related_features": {},
        "inference_configuration": {
            "response_item_limit": -1
        },
        "serving_configuration": {
            "autoscaling": True,
            "autoscale_conditions": {
                "rps": 20
            },
            "min_instance": 1,
            "max_instance": 5,
            "machine_type": "ml.c5.xlarge",
            "processor": "cpu",
            "framework": {
                "framework_name": "tensorflow",
                "framework_version": "2.9.2"
            },
            "shadow_config": {}
        },
        "serving_regions": ["us-east-1"]
    }


def main():
    parser = argparse.ArgumentParser(description='Deploy models via API')
    parser.add_argument('action', choices=['register', 'update'], 
                       help='Action to perform: register or update')
    parser.add_argument('--config', required=True,
                       help='Path to model configuration file')
    parser.add_argument('--api-url', 
                       default=os.environ.get('MODEL_API_URL'),
                       help='API base URL (can also use MODEL_API_URL env var)')
    parser.add_argument('--api-token', 
                       default=os.environ.get('API_TOKEN'),
                       help='API authentication token (can also use API_TOKEN env var)')
    parser.add_argument('--model-id',
                       help='Model ID for update operations (optional)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making API calls')
    
    args = parser.parse_args()
    
    # Validate required parameters
    if not args.api_url:
        print("❌ API URL is required (use --api-url or MODEL_API_URL env var)")
        sys.exit(1)
    
    if not args.api_token:
        print("❌ API token is required (use --api-token or API_TOKEN env var)")
        sys.exit(1)
    
    # Load configuration
    config = load_model_config(args.config)
    
    if args.dry_run:
        print("🧪 DRY RUN MODE - No API calls will be made")
        print(f"📋 Action: {args.action}")
        print(f"📋 Config: {json.dumps(config, indent=2)}")
        return
    
    # Create client and perform action
    client = ModelDeploymentClient(args.api_url, args.api_token)
    
    if args.action == 'register':
        success = client.register_model(config)
    elif args.action == 'update':
        success = client.update_model(config, args.model_id)
    
    if not success:
        sys.exit(1)
    
    print("🎉 Deployment completed successfully!")


if __name__ == '__main__':
    main()
