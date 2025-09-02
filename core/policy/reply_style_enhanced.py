"""Enhanced Reply Style Policy - Jarvis Standard Format"""

def explain_cannot_with_fix(reason: str, solution: str) -> str:
    """
    Standart 'yapamıyorum' formatı
    Format: "Ben yapamıyorum çünkü [reason]. Eğer benim yapmamı istiyorsan [solution]."
    """
    return f"Ben yapamıyorum çünkü {reason}. Eğer benim yapmamı istiyorsan {solution}."

def success_with_details(action: str, details: str = "") -> str:
    """Başarılı işlem yanıtı"""
    result = f"✅ {action}"
    if details:
        result += f"\n\n{details}"
    return result

def thinking_response(task: str) -> str:
    """İşlem sırasında düşünme yanıtı"""
    return f"🔄 {task} üzerinde çalışıyorum..."

def need_more_info(missing: str, example: str = "") -> str:
    """Eksik bilgi durumu"""
    result = f"ℹ️ {missing} bilgisine ihtiyacım var."
    if example:
        result += f" Örnek: {example}"
    return result

def confirm_action(action: str, consequences: str = "") -> str:
    """Onay gerektiren işlemler"""
    result = f"⚠️ {action} işlemini yapmak üzeresin."
    if consequences:
        result += f"\n{consequences}"
    result += "\nOnaylıyor musun? (Evet/Hayır)"
    return result

def error_with_recovery(error: str, recovery: str) -> str:
    """Hata durumu ve kurtarma önerisi"""
    return f"❌ Hata: {error}\n💡 Önerim: {recovery}"

def multi_option_response(question: str, options: list) -> str:
    """Çoklu seçenek sunma"""
    result = f"❓ {question}\n\n"
    for i, option in enumerate(options, 1):
        result += f"{i}. {option}\n"
    return result

def progress_update(current: int, total: int, task: str) -> str:
    """İlerleme durumu"""
    percentage = (current / total) * 100 if total > 0 else 0
    return f"📊 İlerleme: {current}/{total} ({percentage:.1f}%) - {task}"

# Politika kuralları
POLICY_RULES = {
    "no_delete_without_confirm": "Silme işlemleri için onay gerekli",
    "no_sensitive_data_to_llm": "Hassas veriler LLM'e gönderilmez",
    "local_first": "Önce yerel araçlar, sonra bulut servisleri",
    "explain_failures": "Her hata kullanıcıya anlaşılır dille açıklanmalı",
    "provide_alternatives": "Yapılamayan her işlem için alternatif sunulmalı"
}
