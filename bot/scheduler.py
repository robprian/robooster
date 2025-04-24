from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from typing import Dict, List

class SEOScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self._reminders: Dict[int, List[Dict]] = {}
        self._setup_jobs()
    
    def _setup_jobs(self):
        # Laporan mingguan setiap hari Senin jam 9 pagi
        self.scheduler.add_job(
            self._send_weekly_report,
            CronTrigger(day_of_week="mon", hour=9, minute=0),
            id="weekly_report"
        )
        
        # Cek URL setiap 6 jam
        self.scheduler.add_job(
            self._check_urls,
            CronTrigger(hour="*/6"),
            id="url_checker"
        )
    
    async def _send_weekly_report(self):
        """Kirim laporan SEO mingguan ke pengguna"""
        # TODO: Implementasi pengiriman laporan
        pass
    
    async def _check_urls(self):
        """Periksa status SEO URL yang dipantau"""
        # TODO: Implementasi pemeriksaan URL
        pass
    
    def add_reminder(self, user_id: int, url: str, timestamp: datetime):
        """Tambah pengingat untuk update konten"""
        if user_id not in self._reminders:
            self._reminders[user_id] = []
        
        reminder = {
            "url": url,
            "timestamp": timestamp
        }
        self._reminders[user_id].append(reminder)
        
        # Tambah job untuk pengingat
        self.scheduler.add_job(
            self._send_reminder,
            "date",
            run_date=timestamp,
            args=[user_id, url]
        )
    
    async def _send_reminder(self, user_id: int, url: str):
        """Kirim pengingat ke pengguna"""
        # TODO: Implementasi pengiriman pengingat
        pass
    
    def start(self):
        """Mulai scheduler"""
        self.scheduler.start()
    
    def shutdown(self):
        """Hentikan scheduler"""
        self.scheduler.shutdown()

# Create global scheduler instance
seo_scheduler = SEOScheduler()