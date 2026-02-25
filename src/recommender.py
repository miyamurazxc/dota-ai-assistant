from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd

from .kb import KnowledgeBase
from .rules import infer_team_needs, score_candidate


@dataclass(frozen=True)
class Recommendation:
    hero: str
    score: int
    reasons: tuple[str, ...]
    counter_bonus: int
    counter_reason: Optional[str]


class Recommender:
    def __init__(self, data_dir: Path):
        self.kb = KnowledgeBase(data_dir)
        self.data_dir = data_dir
        self.counters: pd.DataFrame | None = None

    def load(self) -> None:
        self.kb.load()
        self.counters = pd.read_csv(self.data_dir / "counters.csv")

    def _counter_bonus(self, candidate: str, enemies: list[str]) -> tuple[int, Optional[str]]:
        if self.counters is None:
            return 0, None

        c = candidate.strip().lower()
        enemies_l = [e.strip().lower() for e in enemies]

        df = self.counters.copy()
        df["counter_l"] = df["counter"].str.lower()
        df["against_l"] = df["against"].str.lower()

        hits = df[(df["counter_l"] == c) & (df["against_l"].isin(enemies_l))]
        if hits.empty:
            return 0, None

        best = hits.sort_values("score", ascending=False).iloc[0]
        return int(best["score"]), str(best["reason"])

    def recommend(self, allies: list[str], enemies: list[str], role: str, top_k: int = 5) -> list[Recommendation]:
        needs = infer_team_needs(allies, enemies)

        results: list[Recommendation] = []
        for h in self.kb.all_heroes():
            rule_res = score_candidate(h.name, role, needs, allies, enemies)
            bonus, reason = self._counter_bonus(h.name, enemies)
            total = rule_res.score + (bonus // 3)
            results.append(
                Recommendation(
                    hero=h.name,
                    score=total,
                    reasons=rule_res.reasons,
                    counter_bonus=bonus,
                    counter_reason=reason,
                )
            )

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:top_k]