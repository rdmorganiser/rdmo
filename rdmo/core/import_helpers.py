from dataclasses import dataclass, field
from inspect import signature
from typing import Callable, Iterable, Optional, Sequence, Union

from django.db import models

ELEMENT_COMMON_FIELDS = (
    'uri_prefix',
    'uri_path',
    'comment',
)

@dataclass(frozen=True)
class ThroughInstanceMapper:
    field_name: str
    source_name: str
    target_name: str
    through_name: str


@dataclass(frozen=True)
class ExtraFieldDefaultHelper:
    field_name: str
    value: Optional[Union[str, bool, int]] = None
    callback: Optional[Callable] = None

    def get_default(self, **kwargs):
        if self.callback is None:
            return self.value

        sig = signature(self.callback)
        _kwargs = {k:val for k,val in kwargs.items() if k in sig.parameters}
        _value = self.callback(**_kwargs)
        return _value


@dataclass(frozen=True)
class ElementImportHelper:
    model: Optional[models.Model] = field(default=None)
    model_path: Optional[str] = field(default=None)
    validators: Iterable[Callable] = field(default_factory=list)
    common_fields: Sequence[str] = field(default=ELEMENT_COMMON_FIELDS)
    lang_fields: Sequence[str] = field(default_factory=list)
    foreign_fields: Sequence[str] = field(default_factory=list)
    extra_fields: Sequence[ExtraFieldDefaultHelper] = field(default_factory=list)
    m2m_instance_fields: Sequence[str] = field(default_factory=list)
    m2m_through_instance_fields: Sequence[ThroughInstanceMapper] = field(default_factory=list)
    reverse_m2m_through_instance_fields: Sequence[ThroughInstanceMapper] = field(default_factory=list)
    add_current_site_editors: bool = field(default=True)
    add_current_site_sites: bool = field(default=False)
