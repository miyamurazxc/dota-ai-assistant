from src.cv_module import CVHeroExtractor
from src.recommender import Recommender
from pathlib import Path


def main():
    image_path = input("Введите путь к изображению: ")

    # Извлечение текста с изображения
    extractor = CVHeroExtractor()
    words = extractor.extract_text(image_path)

    print("\nРаспознано на изображении:")
    print(words)

    # Загрузка базы знаний и контр-пиков
    data_dir = Path(__file__).resolve().parent.parent / "data"
    rec = Recommender(data_dir)
    rec.load()

    # Фильтрация распознанных слов по героям
    enemies = []
    for w in words:
        if w.lower() in [hero.name.lower() for hero in rec.kb.all_heroes()]:  # Сравнение без учёта регистра
            enemies.append(w)

    print("\nОпределённые герои:", enemies)

    # Получение рекомендаций
    top = rec.recommend(allies=[], enemies=enemies, role="support", top_k=5)

    print("\nРекомендации:")
    for i, r in enumerate(top, start=1):
        print(f"{i}) {r.hero} | score={r.score}")


if __name__ == "__main__":
    main()