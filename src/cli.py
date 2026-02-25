from pathlib import Path

from .recommender import Recommender


def _split_list(s: str) -> list[str]:
    s = s.strip()
    if not s:
        return []
    parts = [p.strip() for p in s.split(",")]
    return [p for p in parts if p]


def main() -> None:
    data_dir = Path(__file__).resolve().parent.parent / "data"
    rec = Recommender(data_dir)
    rec.load()

    print("Dota 2 Decision Support (MVP)")
    print("Вводи героев через запятую. Пример: Lion, Axe")
    allies = _split_list(input("Allies: "))
    enemies = _split_list(input("Enemies: "))
    role = input("Your role (support/pos5/pos4/mid/carry/offlane): ").strip()

    top = rec.recommend(allies=allies, enemies=enemies, role=role, top_k=5)

    print("\nРекомендации:")
    for i, r in enumerate(top, start=1):
        print(f"\n{i}) {r.hero} | score={r.score}")
        for reason in r.reasons:
            print(f"   - {reason}")
        if r.counter_bonus > 0 and r.counter_reason:
            print(f"   - counter bonus: {r.counter_bonus} ({r.counter_reason})")


if __name__ == "__main__":
    main()