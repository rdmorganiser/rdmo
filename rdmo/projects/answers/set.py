from __future__ import annotations

from dataclasses import dataclass

SET_DELIM = '|'
ROOT_PREFIX = ''

@dataclass(frozen=True, order=True)
class SetPrefix:
    segments: tuple[int, ...] = ()

    @classmethod
    def parse(cls, prefix: str | None) -> SetPrefix:
        if not prefix:
            return cls(())
        parts = tuple(int(p) for p in str(prefix).strip().split(SET_DELIM) if p != ROOT_PREFIX)
        return cls(parts)

    def to_str(self) -> str:
        return str(self)

    @property
    def level(self) -> int:
        return len(self.segments)

    @property
    def is_root(self) -> bool:
        return self.level == 0

    @property
    def parent_level(self) -> int:
        return self.level + 1

    def append(self, index: int) -> SetPrefix:
        return SetPrefix((*self.segments, int(index)))

    def child(self, index: int) -> SetPrefix:
        return self.append(index)

    def truncate(self, depth: int) -> SetPrefix:
        return SetPrefix(self.segments[: int(depth)])

    # ---- Relations -----------------------------------------------------------
    def is_ancestor_of(self, other: SetPrefix) -> bool:
        return other.segments[: self.level] == self.segments

    def is_strict_ancestor_of(self, other: SetPrefix) -> bool:
        return self.level < other.level and self.is_ancestor_of(other)

    def is_descendant_of(self, other: SetPrefix, include_self: bool = False) -> bool:
        if include_self:
            return other.is_ancestor_of(self)
        return other.is_strict_ancestor_of(self)

    # ---- Helpers that simplify AnswerTree ------------------------------------
    def split_at_level(self, level: int) -> SetPrefix | None:
        if level < self.level:
            return self.truncate(level)
        return None

    def index_at(self, level: int) -> int | None:
        if level < self.level:
            return self.segments[level]
        return None

    def __str__(self) -> str:
        return ROOT_PREFIX if not self.segments else SET_DELIM.join(map(str, self.segments))

    def __bool__(self) -> bool:
        return self.level > 0


@dataclass(frozen=True, order=True)
class SetAddr:
    prefix: SetPrefix
    index: int

    @property
    def set_prefix(self) -> str:
        return str(self.prefix)

    @property
    def set_index(self) -> int:
        return int(self.index)

    @classmethod
    def from_db(cls, prefix_str: str, index: int) -> SetAddr:
        return cls(SetPrefix.parse(prefix_str), int(index))

    @classmethod
    def root_addr(cls):
        return cls(SetPrefix(), 0)

    def to_tuple(self) -> tuple[str, int]:
        return self.set_prefix, self.index

    def as_child_prefix(self) -> SetPrefix:
        return self.prefix.append(self.index)

    def child_at_level(self, level: int) -> SetAddr | None:
        truncated = self.prefix.split_at_level(level)
        if truncated is None:
            return None
        next_index = self.prefix.index_at(level)
        # next_index is guaranteed not None when truncated is not None
        return SetAddr(truncated, int(next_index))

    @staticmethod
    def branch_under(parent: SetAddr | None) -> SetAddr:
        if parent is None:
            return SetAddr.root_addr()
        return SetAddr(parent.as_child_prefix(), 0)
