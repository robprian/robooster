from bs4 import BeautifulSoup
import requests
from typing import Dict, List, Optional
from urllib.parse import urlparse

class SEOAnalyzer:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    async def analyze_url(self, url: str) -> Dict:
        """Analisis SEO dasar untuk URL yang diberikan"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            return {
                'title': self._analyze_title(soup),
                'meta_description': self._analyze_meta_description(soup),
                'headings': self._analyze_headings(soup),
                'images': self._analyze_images(soup),
                'links': self._analyze_links(soup),
                'url_structure': self._analyze_url_structure(url)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_title(self, soup: BeautifulSoup) -> Dict:
        """Analisis tag title"""
        title_tag = soup.find('title')
        title = title_tag.text.strip() if title_tag else ''
        
        return {
            'content': title,
            'length': len(title),
            'issues': self._check_title_issues(title)
        }
    
    def _analyze_meta_description(self, soup: BeautifulSoup) -> Dict:
        """Analisis meta description"""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        content = meta_desc.get('content', '').strip() if meta_desc else ''
        
        return {
            'content': content,
            'length': len(content),
            'issues': self._check_meta_description_issues(content)
        }
    
    def _analyze_headings(self, soup: BeautifulSoup) -> Dict:
        """Analisis struktur heading"""
        headings = {}
        for i in range(1, 7):
            tags = soup.find_all(f'h{i}')
            headings[f'h{i}'] = [tag.text.strip() for tag in tags]
        
        return {
            'structure': headings,
            'issues': self._check_heading_issues(headings)
        }
    
    def _analyze_images(self, soup: BeautifulSoup) -> Dict:
        """Analisis gambar dan alt text"""
        images = soup.find_all('img')
        image_data = [{
            'src': img.get('src', ''),
            'alt': img.get('alt', ''),
            'has_alt': bool(img.get('alt'))
        } for img in images]
        
        return {
            'total': len(images),
            'with_alt': sum(1 for img in image_data if img['has_alt']),
            'without_alt': sum(1 for img in image_data if not img['has_alt']),
            'images': image_data
        }
    
    def _analyze_links(self, soup: BeautifulSoup) -> Dict:
        """Analisis internal dan external links"""
        links = soup.find_all('a')
        internal = []
        external = []
        
        for link in links:
            href = link.get('href')
            if href:
                if href.startswith('http'):
                    external.append(href)
                else:
                    internal.append(href)
        
        return {
            'total': len(links),
            'internal': {
                'count': len(internal),
                'urls': internal
            },
            'external': {
                'count': len(external),
                'urls': external
            }
        }
    
    def _analyze_url_structure(self, url: str) -> Dict:
        """Analisis struktur URL"""
        parsed = urlparse(url)
        return {
            'scheme': parsed.scheme,
            'netloc': parsed.netloc,
            'path': parsed.path,
            'params': parsed.params,
            'query': parsed.query,
            'length': len(url),
            'issues': self._check_url_issues(url)
        }
    
    def _check_title_issues(self, title: str) -> List[str]:
        """Cek masalah pada title"""
        issues = []
        if not title:
            issues.append('Title tidak ditemukan')
        elif len(title) < 30:
            issues.append('Title terlalu pendek (minimal 30 karakter)')
        elif len(title) > 60:
            issues.append('Title terlalu panjang (maksimal 60 karakter)')
        return issues
    
    def _check_meta_description_issues(self, description: str) -> List[str]:
        """Cek masalah pada meta description"""
        issues = []
        if not description:
            issues.append('Meta description tidak ditemukan')
        elif len(description) < 120:
            issues.append('Meta description terlalu pendek (minimal 120 karakter)')
        elif len(description) > 160:
            issues.append('Meta description terlalu panjang (maksimal 160 karakter)')
        return issues
    
    def _check_heading_issues(self, headings: Dict) -> List[str]:
        """Cek masalah pada struktur heading"""
        issues = []
        if not headings.get('h1'):
            issues.append('H1 tidak ditemukan')
        elif len(headings['h1']) > 1:
            issues.append('Terdapat lebih dari satu H1')
        return issues
    
    def _check_url_issues(self, url: str) -> List[str]:
        """Cek masalah pada URL"""
        issues = []
        if len(url) > 100:
            issues.append('URL terlalu panjang (maksimal 100 karakter)')
        if not url.startswith('https'):
            issues.append('URL tidak menggunakan HTTPS')
        return issues

# Create global analyzer instance
seo_analyzer = SEOAnalyzer()