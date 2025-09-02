"""Final Jarvis Orchestrator - Complete Architecture"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from datetime import datetime
from typing import Dict, Any, Optional

from config.settings import config
from agents.jarvis.registry import registry
from core.router.intent_detect import detect_intent
from core.router.dispatcher import Dispatcher
from core.policy.reply_style_enhanced import (
    explain_cannot_with_fix,
    success_with_details,
    thinking_response,
    need_more_info
)
from core.llm.openai_client import llm_client
from core.tools.updater import updater
from core.integrations.database_service import DatabaseService

class JarvisFinal:
    """
    Final Orchestrator - Hedef Mimariye Tam Uyumlu
    Öncelik: Yerel araçlar → Alt asistanlar → LLM (sadece gerektiğinde)
    """
    
    def __init__(self):
        # Core components
        self.registry = registry
        self.dispatcher = Dispatcher()
        self.database = DatabaseService()
        
        # State
        self.history = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Load configuration
        self.validation = config.validate()
        
        print(f"🤖 Jarvis Final initialized - Session: {self.session_id}")
        print(f"📊 Loaded agents: {list(self.registry.agents.keys())}")
        print(f"🔧 Services status: {self.validation}")
    
    async def process(self, message: str, context: Optional[Dict] = None) -> Any:
        """Ana işlem fonksiyonu - Tüm istekler buradan geçer"""
        start_time = datetime.now()
        
        # 1. Intent detection
        intent = detect_intent(message)
        confidence = intent.get("confidence", 0.8)
        
        print(f"📝 Intent: {intent['intent']} (confidence: {confidence})")
        
        # 2. Önce yerel araçları dene
        local_result = await self.dispatcher.try_local_tools(intent, message)
        if local_result:
            response = local_result
        
        # 3. Alt asistanlara yönlendir
        elif intent["intent"].split(".")[0] in self.registry.agents:
            agent_name = intent["intent"].split(".")[0]
            agent = self.registry.get_agent(agent_name)
            if agent:
                response = await agent.process(intent["intent"], message, context)
            else:
                response = explain_cannot_with_fix(
                    f"{agent_name} asistanı yüklenemedi",
                    "sistemi yeniden başlatın veya güncelleme kontrolü yapın"
                )
        
        # 4. Skill-based routing
        elif "." in intent["intent"]:
            skill = intent["intent"]
            agent_name = self.registry.find_agent_for_skill(skill)
            if agent_name:
                agent = self.registry.get_agent(agent_name)
                response = await agent.process(skill, message, context)
            else:
                response = await self._handle_unknown_skill(skill, message)
        
        # 5. Son çare: LLM (sadece belirsiz/karmaşık durumlar)
        elif llm_client.should_use_llm(confidence, local_result is not None):
            response = await llm_client.complete(message, context)
        
        # 6. Hiçbiri değilse varsayılan yanıt
        else:
            response = explain_cannot_with_fix(
                "bu komutu anlayamadım",
                "daha açık bir ifade kullanın veya 'yardım' yazın"
            )
        
        # Log to database
        duration = int((datetime.now() - start_time).total_seconds() * 1000)
        await self.database.save_command(message, response, duration)
        
        # Add to history
        self.history.append({
            "message": message,
            "intent": intent,
            "response": response,
            "duration_ms": duration,
            "timestamp": datetime.now().isoformat()
        })
        
        # Return structured result
        class Result:
            def __init__(self, msg, meta=None):
                self.success = True
                self.message = msg
                self.data = meta or {"duration_ms": duration, "intent": intent}
        
        return Result(response, {"session": self.session_id})
    
    async def _handle_unknown_skill(self, skill: str, message: str) -> str:
        """Bilinmeyen skill durumu"""
        available_skills = []
        for agent_skills in self.registry.skills.values():
            available_skills.extend(agent_skills)
        
        # Benzer skill öner
        similar = [s for s in available_skills if skill.split(".")[0] in s]
        
        if similar:
            return need_more_info(
                f"'{skill}' bulunamadı",
                f"Şunları deneyin: {', '.join(similar[:3])}"
            )
        else:
            return explain_cannot_with_fix(
                f"'{skill}' yeteneği sistemde yok",
                "mevcut yetenekleri görmek için 'yardım' yazın"
            )
    
    async def help(self) -> str:
        """Yardım mesajı"""
        help_text = """
🤖 JARVIS - Kullanılabilir Komutlar

📁 Dosya İşlemleri:
- Masaüstündeki dosyaları listele
- Son görseli aç
- Excel oluştur

📊 PMBA (Proje Yönetimi):
- Teklif hazırla
- Excel raporu oluştur
- Kontrol listesi oluştur
- Bütçe hesapla

👥 IKBA (İnsan Kaynakları):
- Personel listesi
- İzin durumu
- Görev ataması

📞 CIKTA (Müşteri İlişkileri):
- Müşteri durumu
- PDF/Word rapor
- Geri bildirim analizi

⚙️ Sistem:
- Sistem durumu
- Güncelleme kontrolü
- Komut geçmişi
        """
        return success_with_details("Yardım", help_text)
    
    def get_status(self) -> Dict[str, Any]:
        """Detaylı sistem durumu"""
        return {
            "session": self.session_id,
            "agents": list(self.registry.agents.keys()),
            "total_skills": sum(len(skills) for skills in self.registry.skills.values()),
            "history_count": len(self.history),
            "llm_usage": llm_client.get_usage_stats(),
            "validation": self.validation
        }

# Global orchestrator instance
orchestrator = JarvisFinal()
