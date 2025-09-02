# enhanced_integration/core/database_service.py - Mevcut sisteme uyumlu DB servisi
import sqlite3
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

class EnhancedDatabaseService:
    """Mevcut SQLite sistemi ile uyumlu Enhanced Database"""
    
    def __init__(self, db_path: str = "state/jarvis_enhanced.db"):
        self.db_path = Path(db_path)
        self.connection = None
        
        # state klasörü yoksa oluştur (mevcut sistemde var)
        self.db_path.parent.mkdir(exist_ok=True)
    
    def initialize(self):
        """Database'i başlat ve tabloları oluştur"""
        try:
            self.connection = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self.connection.row_factory = sqlite3.Row  # Dict-like access
            
            # Enhanced tablolarını oluştur
            self._create_enhanced_tables()
            
            print(f"Enhanced Database initialized: {self.db_path}")
            
        except Exception as e:
            print(f"Database initialization error: {e}")
            raise e
    
    def _create_enhanced_tables(self):
        """Enhanced sistem için gerekli tabloları oluştur"""
        cursor = self.connection.cursor()
        
        # Companies tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS enhanced_companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                domain TEXT UNIQUE,
                industry TEXT,
                location TEXT,
                employee_count INTEGER,
                description TEXT,
                website_analysis TEXT,  -- JSON
                social_media_links TEXT,  -- JSON
                found_via TEXT DEFAULT 'manual',
                confidence_score REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Contacts tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS enhanced_contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER,
                email TEXT,
                phone TEXT,
                first_name TEXT,
                last_name TEXT,
                position TEXT,
                linkedin_url TEXT,
                is_verified BOOLEAN DEFAULT 0,
                verification_status TEXT DEFAULT 'unknown',
                confidence_score REAL DEFAULT 0.0,
                found_via TEXT DEFAULT 'manual',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES enhanced_companies (id)
            )
        ''')
        
        # Agent metrics tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS enhanced_agent_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name TEXT NOT NULL,
                metric_type TEXT NOT NULL,
                metric_value REAL NOT NULL,
                metric_unit TEXT,
                metadata TEXT,  -- JSON
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # System logs tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS enhanced_system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level TEXT NOT NULL,
                module TEXT NOT NULL,
                message TEXT NOT NULL,
                error_details TEXT,  -- JSON
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.connection.commit()
        print("Enhanced tables created/verified")
    
    # Company operations
    def create_company(self, company_data: Dict) -> Optional[int]:
        """Yeni şirket oluştur"""
        cursor = self.connection.cursor()
        
        # JSON alanları string'e çevir
        if 'website_analysis' in company_data and isinstance(company_data['website_analysis'], dict):
            company_data['website_analysis'] = json.dumps(company_data['website_analysis'])
        
        if 'social_media_links' in company_data and isinstance(company_data['social_media_links'], dict):
            company_data['social_media_links'] = json.dumps(company_data['social_media_links'])
        
        # Insert query
        columns = ', '.join(company_data.keys())
        placeholders = ', '.join(['?' for _ in company_data])
        
        try:
            cursor.execute(f'''
                INSERT INTO enhanced_companies ({columns})
                VALUES ({placeholders})
            ''', list(company_data.values()))
            
            self.connection.commit()
            return cursor.lastrowid
            
        except sqlite3.IntegrityError:
            print(f"Company already exists: {company_data.get('domain', 'unknown')}")
            return None
        except Exception as e:
            print(f"Company creation error: {e}")
            return None
    
    def get_company_by_domain(self, domain: str) -> Optional[Dict]:
        """Domain ile şirket bul"""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT * FROM enhanced_companies WHERE domain = ?
        ''', (domain,))
        
        row = cursor.fetchone()
        if row:
            company = dict(row)
            # JSON alanları parse et
            if company.get('website_analysis'):
                try:
                    company['website_analysis'] = json.loads(company['website_analysis'])
                except:
                    pass
            return company
        return None
    
    def get_dashboard_data(self) -> Dict:
        """Dashboard için özet veriler"""
        cursor = self.connection.cursor()
        
        # Temel sayılar
        cursor.execute('SELECT COUNT(*) FROM enhanced_companies')
        total_companies = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM enhanced_contacts')
        total_contacts = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM enhanced_contacts WHERE is_verified = 1')
        verified_contacts = cursor.fetchone()[0]
        
        return {
            'total_companies': total_companies,
            'total_contacts': total_contacts,
            'verified_contacts': verified_contacts
        }
    
    def close(self):
        """Database bağlantısını kapat"""
        if self.connection:
            self.connection.close()

# Global instance
enhanced_db_service = EnhancedDatabaseService()
