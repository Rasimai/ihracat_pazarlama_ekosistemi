"""Intent Detection"""
def detect_intent(text):
    text_lower = text.lower()
    if "görsel" in text_lower or "resim" in text_lower:
        return {"intent": "image.open", "params": {}}
    elif "excel" in text_lower:
        return {"intent": "excel.create", "params": {}}
    elif "dosya" in text_lower:
        return {"intent": "file.list", "params": {}}
    return {"intent": "general", "params": {"text": text}}
