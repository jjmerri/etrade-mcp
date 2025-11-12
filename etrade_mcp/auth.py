"""E*TRADE OAuth authentication"""
import os
from typing import Tuple
from rauth import OAuth1Service


class ETradeAuth:
    """Handles E*TRADE OAuth authentication"""
    
    def __init__(self, consumer_key: str, consumer_secret: str, environment: str = "sandbox"):
        """
        Initialize E*TRADE OAuth service
        
        Args:
            consumer_key: E*TRADE consumer key
            consumer_secret: E*TRADE consumer secret
            environment: 'sandbox' or 'production'
        """
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.environment = environment
        
        # Determine base URL
        if environment == "production":
            self.base_url = os.getenv("ETRADE_PROD_BASE_URL", "https://api.etrade.com")
        else:
            self.base_url = os.getenv("ETRADE_SANDBOX_BASE_URL", "https://apisb.etrade.com")
        
        # Initialize OAuth service
        self.oauth_service = OAuth1Service(
            name="etrade",
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            request_token_url="https://api.etrade.com/oauth/request_token",
            access_token_url="https://api.etrade.com/oauth/access_token",
            authorize_url="https://us.etrade.com/e/t/etws/authorize?key={}&token={}",
            base_url="https://api.etrade.com"
        )
        
        self.session = None
    
    def get_request_token(self) -> Tuple[str, str]:
        """
        Get OAuth request token
        
        Returns:
            Tuple of (request_token, request_token_secret)
        """
        request_token, request_token_secret = self.oauth_service.get_request_token(
            params={"oauth_callback": "oob", "format": "json"}
        )
        return request_token, request_token_secret
    
    def get_authorize_url(self, request_token: str) -> str:
        """
        Get authorization URL
        
        Args:
            request_token: OAuth request token
            
        Returns:
            Authorization URL
        """
        return self.oauth_service.authorize_url.format(
            self.oauth_service.consumer_key, 
            request_token
        )
    
    def get_session(self, request_token: str, request_token_secret: str, verifier: str):
        """
        Get authenticated session
        
        Args:
            request_token: OAuth request token
            request_token_secret: OAuth request token secret
            verifier: OAuth verifier code from user
            
        Returns:
            Authenticated OAuth session
        """
        self.session = self.oauth_service.get_auth_session(
            request_token,
            request_token_secret,
            params={"oauth_verifier": verifier}
        )
        return self.session
