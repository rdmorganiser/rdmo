from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from django.utils.functional import cached_property

from rdmo.projects.answers.set import SetAddr


@dataclass
class ConditionEvaluator:
    conditions: Any
    values: Any
    resolved_conditions: dict = field(
        default_factory=lambda: defaultdict(lambda: defaultdict(dict))
    )

    @cached_property
    def conditions_map(self) -> dict:
        return {i.id: i for i in self.conditions}

    def resolve_for_element(self, element, parent_set: SetAddr | None) -> tuple[bool, list[dict]]:
        cached = self.resolved_conditions[element].get(parent_set)
        if cached:
            return cached['result'], cached['triggers']

        triggers: list[dict] = []

        # Evaluate each condition and collect minimal trigger info
        for condition in element.conditions.all():
            cond_obj = self.conditions_map[condition.id]
            if parent_set is not None:
                passed = cond_obj.resolve(self.values, parent_set.set_prefix, parent_set.set_index)
            else:
                passed = cond_obj.resolve(self.values)

            if passed:
                # Keep it lean but useful for debugging/UX in node metadata
                triggers.append({
                    'condition_id': condition.id,
                    'question_uri': getattr(condition.source, 'uri', None),
                })

        result = bool(triggers)
        self.resolved_conditions[element][parent_set] = {
            'result': result,
            'triggers': triggers,
        }
        return result, triggers
