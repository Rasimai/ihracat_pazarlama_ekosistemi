"""PMBA - Project Management Business Assistant"""
from typing import Dict, Any
from core.tools.excel_pro import ExcelProcessor
from core.policy.reply_style import explain_cannot_with_fix, success_with_details

class PMBAAgent:
    """Proje yönetimi ve iş süreçleri asistanı"""
    
    def __init__(self):
        self.name = "PMBA"
        self.excel = ExcelProcessor()
    
    async def process(self, intent: str, text: str, context: Dict[str, Any] = None) -> str:
        """PMBA komutlarını işle"""
        text_lower = text.lower()
        
        if "teklif" in text_lower or "offer" in text_lower:
            return await self.generate_offer(text, context)
        elif "excel" in text_lower and "rapor" in text_lower:
            return await self.build_excel_report(text, context)
        elif "checklist" in text_lower or "kontrol listesi" in text_lower:
            return await self.create_checklist(text, context)
        elif "bütçe" in text_lower or "maliyet" in text_lower:
            return await self.calculate_budget(text, context)
        else:
            return await self.handle_general(text, context)
    
    async def generate_offer(self, text: str, context: Dict = None) -> str:
        """Teklif dokümanı oluştur"""
        template = """
📋 TEKLİF DOKÜMANI

Firma: [Firma Adı]
Tarih: {date}
Teklif No: TKL-2024-001

1. ÜRÜN/HİZMET DETAYLARI
- [Ürün/Hizmet açıklaması]

2. FİYATLANDIRMA
- Birim Fiyat: [Tutar]
- KDV: %20
- Toplam: [Tutar]

3. TESLİMAT
- Süre: [Gün]
- Koşullar: [Detaylar]

4. ÖDEME KOŞULLARI
- %30 Sipariş
- %70 Teslimat
        """
        
        from datetime import datetime
        return success_with_details(
            "Teklif dokümanı hazırlandı",
            template.format(date=datetime.now().strftime("%d.%m.%Y"))
        )
    
    async def build_excel_report(self, text: str, context: Dict = None) -> str:
        """Excel rapor oluştur"""
        result = await self.excel.create_excel({"type": "report"})
        return success_with_details("Excel raporu oluşturuldu", result)
    
    async def create_checklist(self, text: str, context: Dict = None) -> str:
        """İhracat kontrol listesi oluştur"""
        checklist = """
✅ İHRACAT SÜRECİ KONTROL LİSTESİ

□ Proforma fatura hazırlandı
□ Gümrük beyannamesi düzenlendi
□ Menşei belgesi alındı
□ EUR.1 dolaşım belgesi hazırlandı
□ Nakliye organizasyonu yapıldı
□ Sigorta poliçesi düzenlendi
□ Yükleme listesi (packing list) hazırlandı
□ Konşimento (B/L) alındı
□ Ödeme teyidi alındı
□ Sevkiyat tamamlandı
        """
        return success_with_details("Kontrol listesi hazır", checklist)
    
    async def calculate_budget(self, text: str, context: Dict = None) -> str:
        """Bütçe hesaplama"""
        return success_with_details(
            "Bütçe hesaplama modülü",
            "Detaylı bütçe için parametreleri belirtin: ürün, miktar, birim fiyat"
        )
    
    async def handle_general(self, text: str, context: Dict = None) -> str:
        """Genel PMBA işlemleri"""
        return f"PMBA: '{text}' için analiz yapıyorum..."
