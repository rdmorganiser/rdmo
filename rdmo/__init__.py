try:
    from ._version import __version__, __version_tuple__, version, version_tuple
except ImportError:
    __version__ = __version_tuple__ = version = version_tuple = None
