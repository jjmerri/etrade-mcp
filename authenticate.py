#!/usr/bin/env python3
"""
E*TRADE Authentication Script

This script helps you authenticate with E*TRADE and saves the access tokens
to your .env file for use with the MCP server.

Usage:
    python authenticate.py
"""
import os
from dotenv import load_dotenv, set_key
from etrade_mcp.auth import ETradeAuth

def main():
    # Load environment variables
    load_dotenv()
    
    consumer_key = os.getenv("ETRADE_CONSUMER_KEY")
    consumer_secret = os.getenv("ETRADE_CONSUMER_SECRET")
    environment = os.getenv("ETRADE_ENVIRONMENT", "sandbox")
    
    if not consumer_key or not consumer_secret:
        print("Error: ETRADE_CONSUMER_KEY and ETRADE_CONSUMER_SECRET must be set in .env file")
        return
    
    print(f"\n🔐 E*TRADE Authentication ({environment} mode)")
    print("=" * 60)
    
    # Initialize auth
    auth = ETradeAuth(consumer_key, consumer_secret, environment)
    
    # Step 1: Get request token
    print("\nStep 1: Getting request token...")
    request_token, request_token_secret = auth.get_request_token()
    print("✓ Request token obtained")
    
    # Step 2: Get authorization URL
    authorize_url = auth.get_authorize_url(request_token)
    print(f"\nStep 2: Please visit this URL to authorize:\n")
    print(f"    {authorize_url}\n")
    
    # Step 3: Get verification code from user
    verifier = input("Enter the verification code from E*TRADE: ").strip()
    
    # Step 4: Get access token
    print("\nStep 3: Exchanging verification code for access token...")
    try:
        session = auth.get_session(request_token, request_token_secret, verifier)
        
        # Extract access token and secret from the session
        access_token = session.access_token
        access_token_secret = session.access_token_secret
        
        print("✓ Access token obtained")
        
        # Step 5: Save to .env file
        print("\nStep 4: Saving tokens to .env file...")
        env_file = ".env"
        set_key(env_file, "ETRADE_ACCESS_TOKEN", access_token)
        set_key(env_file, "ETRADE_ACCESS_TOKEN_SECRET", access_token_secret)
        
        print("✓ Tokens saved to .env")
        print("\n" + "=" * 60)
        print("🎉 Authentication successful!")
        print("\nYou can now use the MCP server without manual authentication.")
        print("Note: Access tokens expire at midnight US Eastern time.")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nAuthentication failed. Please try again.")

if __name__ == "__main__":
    main()
