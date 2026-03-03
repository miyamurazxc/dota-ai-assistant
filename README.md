# Intelligent Decision Support System for Dota 2

## 1. Общая характеристика проекта

Данный проект представляет собой интеллектуальную систему поддержки принятия решений (Intelligent Decision Support System, IDSS), предназначенную для помощи игрокам в игре Dota 2 при выборе контр-пиков и предметных рекомендаций.

Проект выполнен в рамках курса по интеллектуальным системам и реализует итеративный подход (сквозной проект по неделям). Система не взаимодействует с игровыми серверами и не вмешивается в игровой процесс. Все рекомендации формируются на основе экспертных правил (rule-based) и базы знаний (JSON/CSV).

---

## 2. Цель проекта

Разработка MVP интеллектуальной системы, способной:

- анализировать состав противника;
- формировать рекомендации по контр-пикам;
- предлагать предметные рекомендации по угрозам;
- объяснять логику принятого решения (explainable output).

---

## 3. Тип интеллектуальной системы

**Rule-Based Intelligent Decision Support System**

Используемый подход:
- символьный ИИ (экспертные правила if–then);
- база знаний в формате JSON/CSV;
- NLP-модуль для разбора свободного текста;
- CV-модуль (OCR) для извлечения имени героя с изображения.

---

## 4. Архитектура системы

Система реализует цикл:

**Ввод → Анализ → Принятие решения → Объяснение**

### Архитектурная схема
    ```mermaid
    U[Пользователь] --> UI[CLI / Demo scripts]
    UI --> NLP[NLP модуль]
    UI --> CV[CV модуль OCR]
    NLP --> ANALYZE[Анализ состава и угроз]
    CV --> ANALYZE
    ANALYZE --> KB[База знаний]
    KB --> RULES[Rule-Based Engine]
    RULES --> REC[Recommender и объяснения]
    REC --> OUT[Рекомендации]
    OUT --> UI
    ```

## 5. Структура проекта (актуальная)

```text
dota-ai-assistant/
│
├── .gitignore
├── app.py
├── requirements.txt
├── README.md
│
├── docs/
│   └── architecture.md
│
├── data/
│   ├── heroes.json
│   ├── items.json
│   ├── counters.csv
│   │
│   ├── Axe/
│   │   └── axe.png
│   ├── Drow_Ranger/
│   │   └── drow ranger.png
│   ├── Ember Spirit/
│   │   └── ember spirit.png
│   ├── Invoker/
│   │   └── invoker.png
│   ├── Lion/
│   │   └── lion.png
│   ├── Mars/
│   │   └── mars.png
│   ├── Morphling/
│   │   └── morphling.png
│   ├── Phantom_Lancer/
│   │   └── phantom lancer.png
│   ├── Riki/
│   │   └── riki.png
│   ├── Shadow Fiend/
│   │   └── shadow fiend.png
│   ├── Storm Spirit/
│   │   └── storm spirit.png
│   └── Terrorblade/
│       └── terrorblade.png
│
└── src/
    ├── __init__.py
    ├── cli.py
    ├── demo_nlp.py
    ├── demo_cv.py
    ├── kb.py
    ├── nlp.py
    ├── rules.py
    ├── recommender.py
    └── cv_module.py
```

---

## 6. Реализованные модули (что именно сделано)

### 6.1 База знаний (`data/` + `src/kb.py`)

Содержит:
- список героев и их атрибуты (roles, tags, provides, weak_to, strong_against) — `data/heroes.json`;
- таблицу контр-пиков (counter vs against + score + reason) — `data/counters.csv`;
- словарь “угроза → предметы” — `data/items.json`;
- дополнительный набор изображений героев (для Week 7) — папки внутри `data/`.

Как используется:
- при запуске система загружает JSON/CSV;
- на основе `heroes.json` и `counters.csv` считает скоринг героев;
- на основе `items.json` подсказывает предметы по распознанным угрозам.

---

### 6.2 Rule-Based Engine (`src/rules.py`)

Реализует экспертные правила вида IF–THEN и explainable output.

Примеры логики:
- IF у противника много контроля → THEN рекомендовать предметы типа BKB / Linken (через threats → items)
- IF против Phantom Assassin → THEN повышать кандидатов, которые хорошо контрят PA (через counters.csv + rule logic)
- IF команде не хватает disable/frontline/save → THEN повышать героев, которые закрывают потребности

Выход модуля: не просто “герой”, а **герой + причины**, почему он выбран.

---

### 6.3 Recommender (`src/recommender.py`)

Объединяет:
- результаты rule-based оценки кандидатов;
- бонусы контр-пиков из `counters.csv`;
- итоговый скоринг и ранжирование Top-K.

Результат:
- список `Recommendation` (hero, score, reasons, counter_bonus, counter_reason).

---

### 6.4 CLI интерфейс (Week 5) (`src/cli.py`)

Консольный MVP:
- пользователь вводит союзников / противников / роль;
- система выводит Top-K рекомендаций и объяснения.

---

### 6.5 NLP модуль (Week 6) (`src/nlp.py` + `src/demo_nlp.py`)

Функциональность:
- разбор свободного текста (RU/EN микс);
- распознавание роли (pos5/support/mid/carry/offlane/pos4);
- извлечение героев из текста, включая алиасы (PA → Phantom Assassin, CM → Crystal Maiden и т.д.);
- извлечение угроз (many_stuns, heavy_magic, invis и т.п.);
- выдача предметов по угрозам через `items.json` (в demo).

---

### 6.6 Computer Vision (Week 7) — OCR по изображениям (`src/cv_module.py` + `src/demo_cv.py`)

Что сделано на 7-й неделе:
- добавлен модуль обработки изображения через OpenCV + EasyOCR;
- система принимает путь к изображению;
- выполняет OCR и извлекает текст (например “Phantom Lancer”);
- найденные имена сопоставляются с базой знаний (`heroes.json`);
- далее запускается `Recommender` и выдаёт контр-пики.

Важно: в текущей реализации Week 7 — это **OCR (текст с изображения)**, а не “распознавание героя по лицу”. Поэтому изображение должно содержать **надпись с именем героя**, как на твоих карточках.

---

## 7. Установка и запуск (все режимы)

### 7.1 Клонирование

```bash
git clone https://github.com/your_username/dota-ai-assistant.git
cd dota-ai-assistant
```

### 7.2 Виртуальное окружение

```bash
python -m venv .venv
```

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux / Mac:**
```bash
source .venv/bin/activate
```

### 7.3 Установка зависимостей

```bash
pip install -r requirements.txt
```

### 7.4 Запуск режимов

#### A) Основной запуск (если `app.py` подключает CLI)
```bash
python app.py
```

#### B) CLI MVP (Week 5)
Запуск через модуль (из корня проекта):
```bash
python -m src.cli
```

#### C) NLP demo (Week 6)
```bash
python -m src.demo_nlp
```

Пример ввода:
```text
Я саппорт, против Storm Spirit и PA, у врагов много контроля и магии, что пикнуть и что собрать?
```

#### D) CV/OCR demo (Week 7)
```bash
python -m src.demo_cv
```

Дальше программа спросит путь к изображению. Пример:
```text
data/Phantom_Lancer/phantom lancer.png
```

---

## 8. Примеры работы (реальные)

### 8.1 Пример: NLP (Week 6)

Ввод:
```text
Я саппорт, против Storm Spirit и PA, у врагов много контроля и магии, что пикнуть и что собрать?
```

Ожидаемая логика:
- распознаются враги: Storm Spirit, Phantom Assassin;
- распознаются угрозы: heavy_magic, many_stuns;
- выводятся предметы из `items.json`;
- выдаются герои с объяснениями.

---

### 8.2 Пример: CV/OCR (Week 7)

Ввод:
```text
Введите путь к изображению: data/Phantom_Lancer/phantom lancer.png
```

Вывод (пример):
```text
Распознано на изображении:
['Phantom Lancer', '#75']

Определённые герои: ['Phantom Lancer']

Рекомендации:
1) Shadow Shaman | score=11
2) Lion | score=8
3) Dazzle | score=8
4) Oracle | score=8
5) Crystal Maiden | score=8
```

---

## 9. Этапы реализации (Недели 1–7)

| Неделя | Что сделано |
|--------|-------------|
| 1 | Инициализация проекта, структура репозитория, окружение, базовая идея ИС |
| 2 | Проектирование архитектуры, разделение на модули, подготовка документации |
| 3 | Реализация базы знаний (heroes.json, counters.csv, items.json) |
| 4 | Rule-Based Engine: правила, потребности команды, explainable output |
| 5 | CLI MVP: ввод союзников/врагов/роли → рекомендации |
| 6 | NLP: разбор текста, извлечение героев/роли/угроз, items по threats |
| 7 | CV (OCR): обработка изображений героев → извлечение имени → рекомендации |

---

## 10. Перспективы развития

- Web-интерфейс (Streamlit) для загрузки текста/изображений через UI;
- улучшение NLP (больше алиасов, устойчивость к ошибкам, более “умное” извлечение);
- расширение OCR: поддержка скриншотов драфта (где сразу 5 героев);
- переход к hybrid AI: добавить ML-модель для ранжирования кандидатов поверх rule-based логики.

---

## 11. Статус проекта

Реализован MVP и расширения до Week 7 (NLP + OCR).  
Проект готов к дальнейшему расширению и улучшению.











