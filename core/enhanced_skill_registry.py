#!/usr/bin/env python3
"""Enhanced Skill Registry - 21 Skills + Enhanced Database Integration"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional

class EnhancedSkillRegistry:
    """21 Skill + Enhanced Database entegrasyonu"""
    
    def __init__(self):
        self.skills_db_path = "data/enhanced_skills.db"
        self.connection = None
        self.skills = self.load_default_skills()
        self.initialize_skills_db()
    
    def initialize_skills_db(self):
        """Skills için enhanced database tablosu oluştur"""
        try:
            self.connection = sqlite3.connect(self.skills_db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            
            cursor = self.connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS enhanced_skills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    skill_name TEXT UNIQUE NOT NULL,
                    skill_type TEXT NOT NULL,
                    agent_owner TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    last_used TIMESTAMP,
                    usage_count INTEGER DEFAULT 0,
                    performance_score REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS skill_executions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    skill_name TEXT,
                    execution_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT,
                    duration_ms INTEGER,
                    input_data TEXT,
                    output_data TEXT,
                    error_message TEXT
                )
            ''')
            
            self.connection.commit()
            print("✅ Enhanced Skills Database initialized")
            
            # Load existing skills into database
            self.sync_skills_to_database()
            
        except Exception as e:
            print(f"❌ Skills database init failed: {e}")
    
    def load_default_skills(self) -> Dict:
        """21 temel skill'i yükle"""
        return {
            # PMBA Agent Skills
            "company_finder": {
                "type": "PMBA",
                "description": "Google Maps ile şirket bulma",
                "agent": "pmba_agent",
                "active": True
            },
            "industry_analyzer": {
                "type": "PMBA", 
                "description": "Sektör analizi ve kategorileme",
                "agent": "pmba_agent",
                "active": True
            },
            "company_validator": {
                "type": "PMBA",
                "description": "Şirket bilgilerini doğrulama",
                "agent": "pmba_agent", 
                "active": True
            },
            
            # İKBA Agent Skills
            "email_finder": {
                "type": "IKBA",
                "description": "Hunter.io ile email bulma",
                "agent": "ikba_agent",
                "active": True
            },
            "linkedin_scraper": {
                "type": "IKBA",
                "description": "LinkedIn veri toplama",
                "agent": "ikba_agent",
                "active": True
            },
            "phone_extractor": {
                "type": "IKBA",
                "description": "Telefon numarası çıkarma",
                "agent": "ikba_agent",
                "active": True
            },
            "website_analyzer": {
                "type": "IKBA",
                "description": "Website iletişim bilgileri",
                "agent": "ikba_agent",
                "active": True
            },
            
            # İKA Agent Skills
            "content_personalizer": {
                "type": "IKA",
                "description": "AI ile içerik kişiselleştirme",
                "agent": "ika_agent",
                "active": True
            },
            "email_sender": {
                "type": "IKA",
                "description": "Otomatik email gönderimi",
                "agent": "ika_agent",
                "active": True
            },
            "campaign_manager": {
                "type": "IKA",
                "description": "Kampanya yönetimi",
                "agent": "ika_agent",
                "active": True
            },
            "response_tracker": {
                "type": "IKA",
                "description": "Yanıt takip sistemi",
                "agent": "ika_agent",
                "active": True
            },
            
            # RA Agent Skills
            "report_generator": {
                "type": "RA",
                "description": "Otomatik rapor oluşturma",
                "agent": "ra_agent",
                "active": True
            },
            "analytics_processor": {
                "type": "RA",
                "description": "Veri analizi ve metrikler",
                "agent": "ra_agent",
                "active": True
            },
            "dashboard_updater": {
                "type": "RA",
                "description": "Dashboard güncelleyici",
                "agent": "ra_agent",
                "active": True
            },
            
            # CIKTA Agent Skills
            "multi_channel_detector": {
                "type": "CIKTA",
                "description": "Çoklu kanal tespit",
                "agent": "cikta_agent",
                "active": True
            },
            "crm_integrator": {
                "type": "CIKTA",
                "description": "CRM entegrasyonu",
                "agent": "cikta_agent",
                "active": True
            },
            
            # Cross-Agent Skills
            "data_validator": {
                "type": "CROSS",
                "description": "Veri doğrulama",
                "agent": "all_agents",
                "active": True
            },
            "api_connector": {
                "type": "CROSS",
                "description": "API bağlantı yöneticisi",
                "agent": "all_agents", 
                "active": True
            },
            "error_handler": {
                "type": "CROSS",
                "description": "Hata yönetimi",
                "agent": "all_agents",
                "active": True
            },
            "performance_monitor": {
                "type": "CROSS",
                "description": "Performans izleme",
                "agent": "all_agents",
                "active": True
            },
            "backup_manager": {
                "type": "CROSS",
                "description": "Yedekleme yöneticisi",
                "agent": "all_agents",
                "active": True
            },
            "security_validator": {
                "type": "CROSS", 
                "description": "Güvenlik doğrulama",
                "agent": "all_agents",
                "active": True
            }
        }
    
    def sync_skills_to_database(self):
        """Skills'i database'e senkronize et"""
        if not self.connection:
            return
            
        cursor = self.connection.cursor()
        
        for skill_name, skill_data in self.skills.items():
            cursor.execute('''
                INSERT OR REPLACE INTO enhanced_skills 
                (skill_name, skill_type, agent_owner, is_active, metadata)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                skill_name,
                skill_data['type'],
                skill_data['agent'],
                skill_data['active'],
                json.dumps(skill_data)
            ))
        
        self.connection.commit()
        print(f"✅ {len(self.skills)} skills synced to database")
    
    def get_active_skills(self) -> Dict:
        """Aktif skills'leri getir"""
        if not self.connection:
            return self.skills
            
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM enhanced_skills WHERE is_active = 1')
        
        active_skills = {}
        for row in cursor.fetchall():
            active_skills[row['skill_name']] = {
                'type': row['skill_type'],
                'agent': row['agent_owner'],
                'usage_count': row['usage_count'],
                'performance_score': row['performance_score'],
                'last_used': row['last_used']
            }
        
        return active_skills
    
    def get_skills_by_agent(self, agent_name: str) -> List[str]:
        """Belirli agent'ın skills'lerini getir"""
        agent_skills = []
        for skill_name, skill_data in self.skills.items():
            if skill_data['agent'] == agent_name or skill_data['agent'] == 'all_agents':
                agent_skills.append(skill_name)
        return agent_skills
    
    def record_skill_execution(self, skill_name: str, status: str, duration_ms: int = 0, error_msg: str = None):
        """Skill execution'ı kaydet"""
        if not self.connection:
            return
            
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO skill_executions 
            (skill_name, status, duration_ms, error_message)
            VALUES (?, ?, ?, ?)
        ''', (skill_name, status, duration_ms, error_msg))
        
        # Usage count'u güncelle
        cursor.execute('''
            UPDATE enhanced_skills 
            SET usage_count = usage_count + 1, last_used = CURRENT_TIMESTAMP
            WHERE skill_name = ?
        ''', (skill_name,))
        
        self.connection.commit()

# Global enhanced skill registry instance
enhanced_skill_registry = EnhancedSkillRegistry()

if __name__ == "__main__":
    print("🎯 Enhanced Skill Registry Status:")
    active_skills = enhanced_skill_registry.get_active_skills()
    print(f"📊 Total Active Skills: {len(active_skills)}")
    
    skill_types = {}
    for skill_name, skill_data in active_skills.items():
        skill_type = skill_data['type']
        if skill_type not in skill_types:
            skill_types[skill_type] = []
        skill_types[skill_type].append(skill_name)
    
    for skill_type, skills in skill_types.items():
        print(f"  {skill_type}: {len(skills)} skills")
