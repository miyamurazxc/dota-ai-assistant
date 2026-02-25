import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


@dataclass(frozen=True)
class Hero:
    name: str
    roles: tuple[str, ...]
    tags: tuple[str, ...]
    provides: tuple[str, ...]
    weak_to: tuple[str, ...]
    strong_against: tuple[str, ...]


class KnowledgeBase:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self._heroes: dict[str, Hero] = {}

    def load(self) -> None:
        heroes_path = self.data_dir / "heroes.json"
        heroes_raw = json.loads(heroes_path.read_text(encoding="utf-8"))

        heroes: dict[str, Hero] = {}
        for h in heroes_raw:
            hero = Hero(
                name=h["name"],
                roles=tuple(h.get("roles", [])),
                tags=tuple(h.get("tags", [])),
                provides=tuple(h.get("provides", [])),
                weak_to=tuple(h.get("weak_to", [])),
                strong_against=tuple(h.get("strong_against", [])),
            )
            heroes[hero.name.lower()] = hero

        self._heroes = heroes

    def get_hero(self, name: str) -> Optional[Hero]:
        return self._heroes.get(name.strip().lower())

    def all_heroes(self) -> Iterable[Hero]:
        return self._heroes.values()

    def hero_names(self) -> list[str]:
        return sorted([h.name for h in self._heroes.values()])