INTENTS = {
    "maps.search.radius": [],
    "manual.maps.search.radius": [],
    "manual.lens.inspect": [],
    "manual.outlook.send": [],
    "market.customer.search": [],
    "contact.info.find": [],
    "email.compose.personalized": [],
}


def detect_intent(text: str) -> tuple[str, float]:
    t = text.lower()
    if "km" in t and ("ara" in t or "search" in t):
        return "maps.search.radius", 0.62
    return "market.customer.search", 0.51
