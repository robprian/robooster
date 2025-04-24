from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from typing import Optional
import json
import os

class GoogleIndexingAPI:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.SCOPES = ['https://www.googleapis.com/auth/indexing']
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.credentials = None
        self._load_credentials()
    
    def _load_credentials(self):
        """Load or refresh credentials"""
        if os.path.exists('token.json'):
            self.credentials = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(
                    {
                        'installed': {
                            'client_id': self.client_id,
                            'client_secret': self.client_secret,
                            'redirect_uris': [self.redirect_uri],
                            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                            'token_uri': 'https://oauth2.googleapis.com/token'
                        }
                    },
                    self.SCOPES
                )
                self.credentials = flow.run_local_server(port=0)
            
            with open('token.json', 'w') as token:
                token.write(self.credentials.to_json())
    
    async def submit_url(self, url: str, action: str = 'URL_UPDATED') -> dict:
        """Submit URL to Google Indexing API
        
        Args:
            url: The URL to submit
            action: Either 'URL_UPDATED' or 'URL_DELETED'
            
        Returns:
            Response from Google Indexing API
        """
        try:
            service = build('indexing', 'v3', credentials=self.credentials)
            
            body = {
                'url': url,
                'type': action
            }
            
            response = service.urlNotifications().publish(body=body).execute()
            return {
                'success': True,
                'message': f'URL successfully submitted with action: {action}',
                'response': response
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error submitting URL: {str(e)}'
            }
    
    async def get_url_status(self, url: str) -> dict:
        """Get indexing status for a URL
        
        Args:
            url: The URL to check status for
            
        Returns:
            Indexing status from Google API
        """
        try:
            service = build('indexing', 'v3', credentials=self.credentials)
            response = service.urlNotifications().getMetadata(url=url).execute()
            
            return {
                'success': True,
                'status': response
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error getting URL status: {str(e)}'
            }