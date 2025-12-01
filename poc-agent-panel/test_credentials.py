#!/usr/bin/env python3
"""
Test script to verify AWS credentials and Bedrock access
"""

import boto3
import sys
from botocore.exceptions import ClientError, NoCredentialsError, ProfileNotFound


def test_credentials():
    """Test AWS credentials and Bedrock access"""
    
    print("Testing AWS credentials and Bedrock access...\n")
    
    # Test 1: Check if profile exists
    print("1. Checking AWS profile 'chrismiller'...")
    try:
        session = boto3.Session(profile_name='chrismiller')
        print("   ✓ Profile 'chrismiller' found")
    except ProfileNotFound:
        print("   ✗ Profile 'chrismiller' not found")
        print("\n   Please configure your AWS profile:")
        print("   aws configure --profile chrismiller")
        return False
    
    # Test 2: Check credentials
    print("\n2. Checking credentials...")
    try:
        sts = session.client('sts')
        identity = sts.get_caller_identity()
        print(f"   ✓ Credentials valid")
        print(f"   Account: {identity['Account']}")
        print(f"   User/Role: {identity['Arn']}")
    except NoCredentialsError:
        print("   ✗ No credentials found")
        return False
    except ClientError as e:
        print(f"   ✗ Credential error: {e}")
        return False
    
    # Test 3: Check Bedrock access
    print("\n3. Checking Bedrock access in us-west-2...")
    try:
        bedrock = session.client('bedrock', region_name='us-west-2')
        models = bedrock.list_foundation_models()
        print(f"   ✓ Bedrock access confirmed")
        print(f"   Available models: {len(models.get('modelSummaries', []))}")
    except ClientError as e:
        if e.response['Error']['Code'] == 'AccessDeniedException':
            print("   ✗ Access denied to Bedrock")
            print("\n   Please ensure your IAM user/role has Bedrock permissions")
        else:
            print(f"   ✗ Bedrock error: {e}")
        return False
    
    # Test 4: Check for Claude Sonnet 4.5
    print("\n4. Checking for Claude Sonnet 4.5 model...")
    try:
        claude_models = [m for m in models['modelSummaries'] 
                        if 'claude-sonnet-4' in m['modelId'].lower()]
        if claude_models:
            print(f"   ✓ Claude Sonnet 4 models found:")
            for model in claude_models:
                print(f"     - {model['modelId']}")
        else:
            print("   ⚠ No Claude Sonnet 4 models found")
            print("   You may need to enable model access in the Bedrock console")
            return False
    except Exception as e:
        print(f"   ✗ Error checking models: {e}")
        return False
    
    # Test 5: Test Bedrock Runtime
    print("\n5. Testing Bedrock Runtime access...")
    try:
        bedrock_runtime = session.client('bedrock-runtime', region_name='us-west-2')
        print("   ✓ Bedrock Runtime client created successfully")
    except Exception as e:
        print(f"   ✗ Bedrock Runtime error: {e}")
        return False
    
    print("\n" + "="*60)
    print("✓ All tests passed! You're ready to run the panel discussion.")
    print("="*60)
    print("\nRun the panel discussion with:")
    print("  python panel_discussion.py '<your problem statement>'")
    return True


if __name__ == "__main__":
    try:
        success = test_credentials()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
