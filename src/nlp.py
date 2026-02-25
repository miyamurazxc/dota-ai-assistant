import re
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ParsedQuery:
    role: Optional[str]
    allies: list[str]
    enemies: list[str]
    threats: list[str]


KNOWN_ROLES = {
    "mid": ["мид", "mid", "middle"],
    "carry": ["керри", "carry", "pos1"],
    "offlane": ["оффлейн", "offlane", "pos3"],
    "pos4": ["pos4", "4", "роум", "roam"],
    "pos5": ["pos5", "5", "саппорт", "support"],
}

THREAT_KEYWORDS = {
    "invis": ["инвиз", "невидим", "invis", "invisibility"],
    "heavy_magic": [
        "много магии",
        "много магического",
        "магии",
        "магия",
        "heavy magic",
        "magic damage",
        "magical damage",
    ],
    "many_stuns": ["много контроля", "много станов", "станы", "stuns", "disable"],
    "regen_heal": ["много хила", "хил", "healing", "regen"],
    "physical_burst": ["физ урон", "физический", "physical burst", "crit"],
    "silence": ["сайленс", "silence", "немота"],
}

# Частые сокращения в Dota 2 (можно расширять)
ALIASES = {
    "pa": "Phantom Assassin",
    "am": "Anti-Mage",
    "cm": "Crystal Maiden",
    "ss": "Shadow Shaman",
    "bs": "Bloodseeker",
}


def detect_role(text: str) -> Optional[str]:
    t = text.lower()
    for role, keys in KNOWN_ROLES.items():
        for k in keys:
            if k in t:
                return role
    return None


def detect_threats(text: str) -> list[str]:
    t = text.lower()
    threats: list[str] = []
    for threat, keys in THREAT_KEYWORDS.items():
        for k in keys:
            if k in t:
                threats.append(threat)
                break
    return threats


def normalize_alias(token: str) -> str:
    tl = token.lower().strip(" ,.!?()[]{}")
    if tl in ALIASES:
        return ALIASES[tl]
    return token.strip(" ,.!?()[]{}")


def extract_hero_tokens(text: str) -> list[str]:
    """
    Пытаемся вытащить:
    - полные имена: "Storm Spirit"
    - одиночные слова: "Axe"
    - сокращения: "PA", "AM", "CM"
    """
    t = text.strip()

    # 1) Сначала вытащим сокращения (PA, AM и т.п.)
    abbrev = re.findall(r"\b[A-Za-z]{2,4}\b", t)
    tokens = [normalize_alias(a) for a in abbrev]

    # 2) Вытащим потенциальные имена из 1-2 слов (Storm Spirit, Crystal Maiden, Axe)
    phrases = re.findall(r"\b[A-Za-z][A-Za-z\-']+(?:\s+[A-Za-z][A-Za-z\-']+)?\b", t)
    for p in phrases:
        tokens.append(normalize_alias(p))

    # Уберём мусорные слова
    stop = {
        "i", "im", "am", "we", "you", "me",
        "ya", "я", "саппорт", "support", "mid", "carry", "offlane", "pos4", "pos5",
        "against", "vs", "versus", "против", "что", "пикнуть", "собрать", "посоветуй"
    }
    out: list[str] = []
    for tok in tokens:
        tl = tok.lower()
        if tl in stop:
            continue
        if len(tok) < 2:
            continue
        out.append(tok)

    return _dedup(out)


def parse_query(text: str) -> ParsedQuery:
    role = detect_role(text)
    threats = detect_threats(text)

    tokens = extract_hero_tokens(text)
    t = text.lower()

    # reverse map: "phantom assassin" -> ["pa"]
    reverse_aliases: dict[str, list[str]] = {}
    for a, canon in ALIASES.items():
        reverse_aliases.setdefault(canon.lower(), []).append(a.lower())

    enemies: list[str] = []
    allies: list[str] = []

    enemy_markers = ["против", "vs", "against"]
    marker_pos = min([t.find(m) for m in enemy_markers if t.find(m) != -1], default=-1)

    if marker_pos != -1:
        after = t[marker_pos:]

        for tok in tokens:
            canon = tok.strip()
            canon_l = canon.lower()

            mentions = [canon_l]
            mentions += reverse_aliases.get(canon_l, [])

            is_enemy = any(re.search(rf"\b{re.escape(m)}\b", after) for m in mentions)

            if is_enemy:
                enemies.append(canon)
            else:
                allies.append(canon)
    else:
        allies = tokens

    return ParsedQuery(role=role, allies=_dedup(allies), enemies=_dedup(enemies), threats=_dedup(threats))


def _dedup(items: list[str]) -> list[str]:
    seen = set()
    out = []
    for x in items:
        xl = x.lower()
        if xl in seen:
            continue
        seen.add(xl)
        out.append(x)
    return out