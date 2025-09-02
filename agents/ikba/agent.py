"""IKBA - HR & People Management Assistant"""
from typing import Dict, Any
from core.policy.reply_style import success_with_details

class IKBAAgent:
    """İnsan kaynakları ve personel yönetimi asistanı"""
    
    def __init__(self):
        self.name = "IKBA"
    
    async def process(self, intent: str, text: str, context: Dict[str, Any] = None) -> str:
        """IKBA komutlarını işle"""
        text_lower = text.lower()
        
        if "izin" in text_lower or "leave" in text_lower:
            return await self.manage_leave(text, context)
        elif "personel" in text_lower or "çalışan" in text_lower:
            return await self.manage_employee(text, context)
        elif "görev" in text_lower or "task" in text_lower:
            return await self.assign_task(text, context)
        else:
            return f"IKBA: '{text}' için İK süreçlerini kontrol ediyorum..."
    
    async def manage_leave(self, text: str, context: Dict = None) -> str:
        """İzin yönetimi"""
        return success_with_details(
            "İzin durumu",
            "Yıllık izin hakları:\n- Ali: 14 gün\n- Ayşe: 10 gün\n- Mehmet: 21 gün"
        )
    
    async def manage_employee(self, text: str, context: Dict = None) -> str:
        """Personel yönetimi"""
        return success_with_details(
            "Personel listesi",
            "Aktif çalışan sayısı: 25\nBu ay işe başlayan: 2\nAçık pozisyonlar: 3"
        )
    
    async def assign_task(self, text: str, context: Dict = None) -> str:
        """Görev ataması"""
        return success_with_details(
            "Görev ataması yapıldı",
            "Proje X → Ali (Backend)\nProje Y → Ayşe (Frontend)"
        )
