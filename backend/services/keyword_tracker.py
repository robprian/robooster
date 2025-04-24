from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models.models import URL, Keyword
import openai
import requests

class KeywordTracker:
    def __init__(self, google_api_key: str, openai_api_key: str):
        self.google_api_key = google_api_key
        self.openai_api_key = openai_api_key
        openai.api_key = openai_api_key
    
    async def track_keyword_ranking(self, keyword: str, domain: str) -> Dict:
        """Track peringkat keyword menggunakan Google Search API"""
        try:
            url = 'https://www.googleapis.com/customsearch/v1'
            params = {
                'key': self.google_api_key,
                'cx': 'YOUR_SEARCH_ENGINE_ID',  # Custom Search Engine ID
                'q': keyword,
                'num': 100  # Maksimum hasil pencarian
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Cari posisi domain dalam hasil pencarian
            position = None
            for i, item in enumerate(data.get('items', []), 1):
                if domain in item['link']:
                    position = i
                    break
            
            return {
                'keyword': keyword,
                'position': position,
                'total_results': data.get('searchInformation', {}).get('totalResults'),
                'checked_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'keyword': keyword
            }
    
    async def generate_meta_tags(self, url: str, content: str) -> Dict:
        """Generate meta tags menggunakan OpenAI"""
        try:
            prompt = f"""Analyze this content and generate SEO-optimized meta tags.
            Content: {content[:500]}...  # Limit content length
            
            Please provide:
            1. Title tag (max 60 chars)
            2. Meta description (max 160 chars)
            3. Primary keywords (max 5)
            
            Format the response as JSON."""
            
            response = await openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": "You are an SEO expert assistant."
                }, {
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Parse response and format meta tags
            ai_suggestion = response.choices[0].message.content
            
            return {
                'success': True,
                'meta_tags': ai_suggestion,
                'url': url,
                'generated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'url': url
            }
    
    async def update_keyword_tracking(self, db: Session, url_id: int) -> Dict:
        """Update tracking untuk semua keyword terkait URL"""
        try:
            url = db.query(URL).filter(URL.id == url_id).first()
            if not url:
                return {'error': 'URL not found'}
            
            results = []
            domain = url.url.split('/')[2]  # Get domain from URL
            
            for keyword in url.keywords:
                ranking = await self.track_keyword_ranking(keyword.keyword, domain)
                results.append(ranking)
            
            return {
                'success': True,
                'url': url.url,
                'tracking_results': results
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }