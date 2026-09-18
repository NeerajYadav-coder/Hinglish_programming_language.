"""Default globals and built-in runtime bindings for Hinglish execution."""

from typing import Any, Dict


def dikhao(*args: Any, **kwargs: Any) -> None:
    """Default built-in print function for Hinglish."""
    print(*args, **kwargs)


def get_default_globals() -> Dict[str, Any]:
    """Returns the default global execution context for Hinglish programs."""
    return {
        "__name__": "__main__",
        "__doc__": None,
        "__package__": None,
        "dikhao": dikhao,
        "chapo": dikhao,
        "batao": dikhao,
        "sahi": True,
        "galat": False,
        "kuch_nahi": None,
        "shunya": None,
        "khol": open,
    }


__all__ = ["dikhao", "get_default_globals"]
