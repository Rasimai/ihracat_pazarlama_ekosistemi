#!/usr/bin/env python3
"""Enhanced Orchestrator - Jarvis + Enhanced System Integration"""

import sys
import os
from pathlib import Path

# Path setup for both original and enhanced systems
sys.path.append(str(Path.cwd()))
sys.path.append(str(Path.cwd() / 'enhanced_integration'))

try:
    # Import enhanced components
    from enhanced_integration.core.key_manager import enhanced_key_manager
    from enhanced_integration.core.database_service import enhanced_db_service
    print("✅ Enhanced modules imported successfully")
except ImportError as e:
    print(f"⚠️ Enhanced modules not available: {e}")
    enhanced_key_manager = None
    enhanced_db_service = None

try:
    # Import original orchestrator
    from core.orchestrator import orchestrator
    print("✅ Original orchestrator imported")
except ImportError as e:
    print(f"❌ Original orchestrator import failed: {e}")
    orchestrator = None

class EnhancedOrchestrator:
    """Unified orchestrator combining original + enhanced features"""
    
    def __init__(self):
        self.original_orchestrator = orchestrator
        self.enhanced_key_manager = enhanced_key_manager
        self.enhanced_db = enhanced_db_service
        self.initialize_components()
    
    def initialize_components(self):
        """Initialize both original and enhanced components"""
        print("🚀 Initializing Enhanced Orchestrator...")
        
        # Initialize enhanced database if available
        if self.enhanced_db:
            try:
                self.enhanced_db.initialize()
                print("✅ Enhanced database initialized")
            except Exception as e:
                print(f"⚠️ Enhanced database init failed: {e}")
        
        # Validate API keys
        if self.enhanced_key_manager:
            if self.enhanced_key_manager.is_ready():
                print(f"✅ API Keys loaded: {len(self.enhanced_key_manager.keys)} keys")
            else:
                print("⚠️ API Keys missing - some features may be disabled")
    
    def get_system_status(self):
        """Get comprehensive system status"""
        status = {
            'enhanced_orchestrator': True,
            'original_orchestrator': bool(self.original_orchestrator),
            'enhanced_database': bool(self.enhanced_db),
            'enhanced_keys': bool(self.enhanced_key_manager),
            'api_keys_count': len(self.enhanced_key_manager.keys) if self.enhanced_key_manager else 0,
            'system_ready': self._is_system_ready()
        }
        return status
    
    def _is_system_ready(self):
        """Check if entire system is ready"""
        return (
            self.original_orchestrator is not None and
            self.enhanced_db is not None and
            self.enhanced_key_manager is not None
        )
    
    def start_enhanced_services(self):
        """Start all enhanced services"""
        print("🚀 Starting Enhanced Services...")
        
        services_status = {}
        
        # Start Enhanced API (port 8007)
        try:
            import subprocess
            api_process = subprocess.Popen([
                'python', '-m', 'enhanced_integration.api.enhanced_api'
            ])
            services_status['enhanced_api'] = 'started'
            print("✅ Enhanced API started on port 8007")
        except Exception as e:
            services_status['enhanced_api'] = f'failed: {e}'
            print(f"❌ Enhanced API start failed: {e}")
        
        return services_status

# Global enhanced orchestrator instance
enhanced_orchestrator = EnhancedOrchestrator()

if __name__ == "__main__":
    print("🎯 Enhanced Orchestrator Status:")
    status = enhanced_orchestrator.get_system_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    if status['system_ready']:
        print("🎉 Enhanced Orchestrator is READY!")
    else:
        print("⚠️ Enhanced Orchestrator has missing components")
