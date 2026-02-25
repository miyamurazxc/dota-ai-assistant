import json
from pathlib import Path

from src.nlp import parse_query
from src.recommender import Recommender


def main() -> None:
    data_dir = Path(__file__).resolve().parent.parent / "data"
    rec = Recommender(data_dir)
    rec.load()

    text = input("Введите запрос (пример: 'Я саппорт, против Storm Spirit и PA, что пикнуть?'): ")
    parsed = parse_query(text)

    role = parsed.role or "support"
    if role == "pos5":
        role = "support"

    allies = parsed.allies
    enemies = parsed.enemies

    print("\nРаспознано:")
    print(f"role: {role}")
    print(f"allies: {allies}")
    print(f"enemies: {enemies}")
    print(f"threats: {parsed.threats}")

    # Items suggestion by threats (Week 6)
    items_path = data_dir / "items.json"
    items_data = json.loads(items_path.read_text(encoding="utf-8"))
    threat_to_items = items_data.get("threat_to_items", {})

    if parsed.threats:
        print("\nРекомендации по предметам (по распознанным угрозам):")
        for th in parsed.threats:
            rec_items = threat_to_items.get(th, [])
            if rec_items:
                print(f"- {th}: {', '.join(rec_items)}")

    top = rec.recommend(allies=allies, enemies=enemies, role=role, top_k=5)

    print("\nРекомендации по героям:")
    for i, r in enumerate(top, start=1):
        print(f"\n{i}) {r.hero} | score={r.score}")
        for reason in r.reasons:
            print(f"   - {reason}")
        if r.counter_bonus > 0 and r.counter_reason:
            print(f"   - counter bonus: {r.counter_bonus} ({r.counter_reason})")


if __name__ == "__main__":
    main()