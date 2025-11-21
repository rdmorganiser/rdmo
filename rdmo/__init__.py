try:
    from importlib.metadata import PackageNotFoundError
    from importlib.metadata import version as _dist_version
except ImportError:  # pragma: no cover - for older Pythons if you ever care
    from importlib_metadata import PackageNotFoundError  # type: ignore[assignment]
    from importlib_metadata import version as _dist_version


def _get_version() -> str:
    try:
        return _dist_version("rdmo")
    except PackageNotFoundError:
        return "0+unknown"

__version__: str = _get_version()
version: str = __version__

def _version_to_tuple(v: str) -> tuple[int, ...]:
    parts: list[int] = []
    for part in v.split("."):
        if part.isdigit():
            parts.append(int(part))
        else:
            # stop on non-numeric pieces like "0.dev3+gXXXX"
            break
    return tuple(parts)


__version_tuple__ = _version_to_tuple(__version__)
version_tuple = __version_tuple__
