# enhanced_integration/core/enhanced_orchestrator.py
import sys
from pathlib import Path

# Mevcut orchestrator'u import et
sys.path.append('agents/jarvis')
from orchestrator_complete import JarvisOrchestrator

# Enhanced modülleri import et
sys.path.append('enhanced_integration')
from core.key_manager import enhanced_key_manager
from core.database_service import enhanced_db_service

class EnhancedJarvisOrchestrator(JarvisOrchestrator):
    """Mevcut orchestrator'u Enhanced özelliklerle güçlendiren sınıf"""
    
    def __init__(self):
        # Ana orchestrator'u başlat
        super().__init__()
        
        # Enhanced servisleri ekle
        self.enhanced_key_manager = enhanced_key_manager
        self.enhanced_db = enhanced_db_service
        
        # Enhanced veritabanını başlat
        self.enhanced_db.initialize()
        
        print("Enhanced Jarvis Orchestrator initialized!")
        print(f"Keys loaded: {len(self.enhanced_key_manager.keys)}")
        print(f"Missing keys: {self.enhanced_key_manager.get_missing_keys()}")
    
    async def enhanced_company_search(self, query: str, limit: int = 50):
        """Enhanced şirket arama - DB + Orchestrator"""
        # Önce veritabanından ara
        db_results = self.enhanced_db.search_companies(query, limit//2)
        
        # Sonra orchestrator ile ara (mevcut sistem)
        orchestrator_results = await self.process_request(
            f"pmba agent ile {query} sektöründe şirket ara"
        )
        
        # Sonuçları birleştir
        return {
            'database_results': db_results,
            'orchestrator_results': orchestrator_results,
            'total_found': len(db_results) + (len(orchestrator_results.get('results', [])) if isinstance(orchestrator_results, dict) else 0)
        }
    
    def get_enhanced_dashboard_data(self):
        """Enhanced dashboard verilerini getir"""
        # Mevcut sistem verilerini al
        base_data = self.get_system_status()
        
        # Enhanced verilerini ekle
        enhanced_data = self.enhanced_db.get_dashboard_data()
        
        return {
            'base_system': base_data,
            'enhanced_metrics': enhanced_data,
            'key_status': self.enhanced_key_manager.validate_keys(),
            'missing_keys': self.enhanced_key_manager.get_missing_keys()
        }
    
    def log_enhanced_metric(self, agent_name: str, metric_type: str, value: float):
        """Enhanced metrik kaydet"""
        self.enhanced_db.log_agent_metric(agent_name, metric_type, value)
        
        # Mevcut sisteme de kaydet
        self.log_system_event(f"{agent_name} metric: {metric_type} = {value}")
    
    async def process_enhanced_request(self, user_input: str):
        """Enhanced request processing"""
        # Metrik kaydet
        self.log_enhanced_metric("orchestrator", "requests_processed", 1)
        
        # Mevcut orchestrator'a gönder
        result = await self.process_request(user_input)
        
        return result

# Global enhanced orchestrator instance
enhanced_orchestrator = EnhancedJarvisOrchestrator()
