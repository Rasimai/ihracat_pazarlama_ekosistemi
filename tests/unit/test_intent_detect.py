from core.router.intent_detect import detect_intent


def test_maps_radius_triggers():
    intent, score = detect_intent("Berlin’de 2 km yatak ara")
    assert intent == "maps.search.radius"
    assert 0 <= score <= 1


def test_default_intent():
    intent, score = detect_intent("müşteri araştırması yap")
    assert intent in {"market.customer.search", "maps.search.radius"}
