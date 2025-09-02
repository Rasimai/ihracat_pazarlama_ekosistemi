"""OpenAI Client - Minimal Kullanım"""
from config.settings import config
from typing import Optional, Dict, Any

class OpenAIClient:
    """
    LLM sadece şu durumlarda kullanılır:
    1. Belirsiz istekleri netleştirme
    2. Uzun metin üretimi (teklif, rapor)
    3. Karmaşık muhakeme gerektiren durumlar
    """
    
    def __init__(self):
        self.api_key = config.OPENAI_API_KEY
        self.enabled = bool(self.api_key)
        self.usage_count = 0
        self.usage_log = []
    
    async def complete(self, prompt: str, context: Optional[Dict] = None) -> str:
        """LLM completion - sadece gerektiğinde"""
        if not self.enabled:
            return self._local_fallback(prompt)
        
        # Log usage reason
        self.usage_count += 1
        self.usage_log.append({
            "prompt": prompt[:100],
            "reason": self._determine_usage_reason(prompt)
        })
        
        # Mock response for now
        return f"LLM Response (Usage #{self.usage_count}): İsteğiniz işleniyor..."
    
    def should_use_llm(self, intent_confidence: float, local_tools_available: bool) -> bool:
        """LLM kullanılmalı mı?"""
        # Sadece güven düşük VE yerel araç yoksa
        return intent_confidence < 0.5 and not local_tools_available
    
    def _determine_usage_reason(self, prompt: str) -> str:
        """LLM kullanım sebebini belirle"""
        if len(prompt) > 500:
            return "long_text_generation"
        elif "?" in prompt and prompt.count("?") > 2:
            return "complex_reasoning"
        elif any(word in prompt.lower() for word in ["belirsiz", "karmaşık", "detaylı"]):
            return "ambiguous_request"
        else:
            return "fallback"
    
    def _local_fallback(self, prompt: str) -> str:
        """LLM yoksa yerel yanıt"""
        return "LLM servisi aktif değil. Yerel araçlarla işleminizi gerçekleştiriyorum."
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """LLM kullanım istatistikleri"""
        return {
            "total_calls": self.usage_count,
            "enabled": self.enabled,
            "recent_logs": self.usage_log[-10:]
        }

# Global client instance
llm_client = OpenAIClient()
