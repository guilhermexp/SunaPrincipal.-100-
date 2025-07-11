#!/usr/bin/env python3
"""
Script to test Pipedream connection and configuration
"""
import os
import sys
import asyncio
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

async def test_pipedream():
    print("=== Testing Pipedream Configuration ===\n")
    
    # Check environment variables
    print("1. Checking environment variables...")
    required_vars = [
        "PIPEDREAM_PROJECT_ID",
        "PIPEDREAM_CLIENT_ID", 
        "PIPEDREAM_CLIENT_SECRET",
        "PIPEDREAM_X_PD_ENVIRONMENT"
    ]
    
    all_vars_present = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✓ {var}: {value[:20]}..." if len(value) > 20 else f"✓ {var}: {value}")
        else:
            print(f"✗ {var}: NOT SET")
            all_vars_present = False
    
    if not all_vars_present:
        print("\n❌ Missing required environment variables!")
        return
    
    print("\n✅ All environment variables are set")
    
    # Test MCP availability
    print("\n2. Checking MCP availability...")
    try:
        from mcp import ClientSession
        from mcp.client.streamable_http import streamablehttp_client
        print("✓ MCP modules imported successfully")
    except ImportError as e:
        print(f"✗ MCP not available: {e}")
        print("\nTo install MCP, run:")
        print("pip install mcp")
        return
    
    # Test Pipedream client
    print("\n3. Testing Pipedream client...")
    try:
        from pipedream.client import get_pipedream_client
        client = get_pipedream_client()
        print(f"✓ Pipedream client created: {client}")
        
        # Test access token
        print("\n4. Testing OAuth access token...")
        access_token = await client._obtain_access_token()
        print(f"✓ Access token obtained: {access_token[:20]}...")
        
        # Test rate limit token
        print("\n5. Testing rate limit token...")
        rate_limit_token = await client._obtain_rate_limit_token()
        print(f"✓ Rate limit token obtained: {rate_limit_token[:20]}...")
        
        # Test API connection
        print("\n6. Testing API connection...")
        test_user_id = "test_user_123"
        
        try:
            # Try to get connections for test user
            connections = await client.get_connections(test_user_id)
            print(f"✓ API connection successful")
            print(f"  Connections for test user: {len(connections)}")
        except Exception as e:
            if "404" in str(e) or "not found" in str(e).lower():
                print("✓ API connection successful (user not found is expected)")
            else:
                print(f"✗ API connection failed: {e}")
        
        print("\n✅ Pipedream configuration is working correctly!")
        
    except Exception as e:
        print(f"✗ Error testing Pipedream client: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Load environment variables from .env file
    from dotenv import load_dotenv
    env_file = Path(__file__).parent / "backend" / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        print(f"Loaded environment from: {env_file}\n")
    
    asyncio.run(test_pipedream())