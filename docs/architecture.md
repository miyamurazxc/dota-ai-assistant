# Architecture (MVP)

## Components
- UI: Console CLI (Week 5) / Text input
- NLP Parser (Week 6): transforms free text to structured query
- Rule Engine (Week 3): if-then rules + team needs
- Knowledge Base (Week 4): JSON/CSV data about heroes/counters/items
- Recommender: combines rules + counter scores and returns top suggestions

## Data flow
User text -> NLP -> (allies, enemies, role, threats) -> Rule Engine -> Candidates ranking -> Output (reasons)