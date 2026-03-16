from similarity import find_similar
from heroes_vectors import heroes


def analyze_text(text):

    text = text.lower()

    # если пользователь написал героя
    for hero in heroes:
        if hero in text:
            return hero

    # роли
    if "carry" in text or "damage" in text:
        return "carry"

    if "support" in text or "stun" in text:
        return "support"

    return "unknown"


def rule_engine(result):

    if result in heroes:
        return result

    if result == "carry":
        return "juggernaut"

    if result == "support":
        return "lion"

    return "juggernaut"


def recommendation(text):

    detected = analyze_text(text)

    base_hero = rule_engine(detected)

    similar = find_similar(base_hero, heroes)

    return base_hero, similar