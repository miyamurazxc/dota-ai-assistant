from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class RuleResult:
    score: int
    reasons: tuple[str, ...]


def infer_team_needs(allies: list[str], enemies: list[str]) -> set[str]:
    allies_l = [a.lower() for a in allies]
    enemies_l = [e.lower() for e in enemies]

    needs: set[str] = set()

    disable_count = 0
    save_count = 0
    push_count = 0
    frontline_count = 0

    def has(hero: str, keywords: Iterable[str]) -> bool:
        hero = hero.lower()
        for k in keywords:
            if k.lower() in hero:
                return True
        return False

    for a in allies_l:
        if a in ["lion", "shadow shaman", "crystal maiden", "puck", "axe", "magnus"]:
            disable_count += 1
        if a in ["oracle", "dazzle"]:
            save_count += 1
        if a in ["shadow shaman", "drow ranger"]:
            push_count += 1
        if a in ["axe", "bristleback"]:
            frontline_count += 1

    if disable_count < 1:
        needs.add("disable")
    if save_count < 1:
        needs.add("save")
    if frontline_count < 1:
        needs.add("frontline")
    if push_count < 1:
        needs.add("push")

    if "storm spirit" in enemies_l and disable_count < 2:
        needs.add("instant_disable")
    if "phantom assassin" in enemies_l:
        needs.add("anti_pa")

    return needs


def score_candidate(hero_name: str, role: str, needs: set[str], allies: list[str], enemies: list[str]) -> RuleResult:
    score = 0
    reasons: list[str] = []

    role = role.strip().lower()
    hero_l = hero_name.lower()
    enemies_l = [e.lower() for e in enemies]

    if role in ["support", "pos5", "pos4"]:
        if hero_l in ["lion", "oracle", "dazzle", "shadow shaman", "crystal maiden", "silencer"]:
            score += 4
            reasons.append("подходит по роли саппорта")
        else:
            score -= 1
            reasons.append("по роли саппорта не самый очевидный выбор")

    if "disable" in needs and hero_l in ["lion", "shadow shaman", "crystal maiden", "puck", "axe", "magnus"]:
        score += 4
        reasons.append("закрывает нехватку контроля (disable)")

    if "instant_disable" in needs and hero_l in ["lion", "silencer"]:
        score += 4
        reasons.append("полезен против мобильного мида (нужен instant disable/silence)")

    if "save" in needs and hero_l in ["oracle", "dazzle"]:
        score += 4
        reasons.append("закрывает нехватку сейва (save)")

    if "frontline" in needs and hero_l in ["axe", "bristleback"]:
        score += 3
        reasons.append("даёт фронтлайн для команды")

    if "push" in needs and hero_l in ["shadow shaman", "drow ranger"]:
        score += 3
        reasons.append("усиливает пуш и давление на вышки")

    if "storm spirit" in enemies_l and hero_l in ["lion", "silencer"]:
        score += 3
        reasons.append("хорош против Storm Spirit (контроль/сайленс)")

    if "phantom assassin" in enemies_l and hero_l in ["axe"]:
        score += 4
        reasons.append("контрит Phantom Assassin (Call + tankiness)")

    if "anti_pa" in needs and hero_l in ["axe", "dazzle"]:
        score += 2
        reasons.append("полезен в матч-апе против PA")

    if hero_l in [a.lower() for a in allies]:
        score -= 10
        reasons.append("этот герой уже есть у союзников (дубликат)")

    if len(reasons) == 0:
        reasons.append("нейтральный выбор по текущим правилам")

    return RuleResult(score=score, reasons=tuple(reasons))