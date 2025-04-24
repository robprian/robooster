from telegram import Update
from telegram.ext import ContextTypes
from .seo_analyzer import SEOAnalyzer
from ..services.google_indexing import GoogleIndexingAPI
from ..config import settings
from typing import Optional

class CommandHandlers:
    def __init__(self):
        self.seo_analyzer = SEOAnalyzer()
        self.indexing_api = GoogleIndexingAPI(
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            redirect_uri=settings.GOOGLE_REDIRECT_URI
        )
    
    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /analyze command"""
        if not context.args:
            await update.message.reply_text(
                'Silakan masukkan URL yang ingin dianalisis.\n'
                'Contoh: /analyze https://example.com'
            )
            return
        
        url = context.args[0]
        await update.message.reply_text(f'Menganalisis {url}...')
        
        result = await self.seo_analyzer.analyze_url(url)
        if 'error' in result:
            await update.message.reply_text(f'Error: {result["error"]}')
            return
        
        # Format hasil analisis
        analysis_text = (
            f'📊 Hasil Analisis SEO untuk {url}\n\n'
            f'📝 Title ({result["title"]["length"]} karakter):\n'
            f'{result["title"]["content"]}\n'
            f'Masalah: {"\n- ".join(result["title"]["issues"]) if result["title"]["issues"] else "Tidak ada"}\n\n'
            f'📋 Meta Description ({result["meta_description"]["length"]} karakter):\n'
            f'{result["meta_description"]["content"]}\n'
            f'Masalah: {"\n- ".join(result["meta_description"]["issues"]) if result["meta_description"]["issues"] else "Tidak ada"}\n\n'
            f'📌 Headings:\n{result["headings"]}\n\n'
            f'🖼 Gambar: {result["images"]["count"]} total\n'
            f'- Tanpa alt text: {result["images"]["missing_alt"]}\n\n'
            f'🔗 Links:\n'
            f'- Internal: {result["links"]["internal"]}\n'
            f'- External: {result["links"]["external"]}\n\n'
            f'🌐 Struktur URL:\n{result["url_structure"]["analysis"]}'
        )
        
        await update.message.reply_text(analysis_text)
    
    async def submit_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /submit command"""
        if not context.args:
            await update.message.reply_text(
                'Silakan masukkan URL yang ingin disubmit ke Google.\n'
                'Contoh: /submit https://example.com'
            )
            return
        
        url = context.args[0]
        await update.message.reply_text(f'Mensubmit {url} ke Google Indexing API...')
        
        result = await self.indexing_api.submit_url(url)
        if result['success']:
            await update.message.reply_text(
                f'✅ {result["message"]}\n\n'
                f'Detail Response:\n{result["response"]}'
            )
        else:
            await update.message.reply_text(f'❌ {result["message"]}')
    
    async def report_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /report command"""
        # TODO: Implement weekly SEO report generation
        await update.message.reply_text('Fitur laporan SEO mingguan akan segera hadir!')
    
    async def remindme_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /remindme command"""
        # TODO: Implement content update reminder
        await update.message.reply_text('Fitur pengingat update konten akan segera hadir!')