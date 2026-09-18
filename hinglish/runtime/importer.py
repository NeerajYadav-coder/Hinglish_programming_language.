"""Import hook for loading .hin Hinglish modules directly using Python's import machinery."""

import importlib.abc
import importlib.machinery
import sys
from pathlib import Path
from typing import List, Optional, Sequence, Union

from ..compiler import HinglishCompiler
from ..parser import parse


class HinglishSourceLoader(importlib.abc.SourceLoader):
    """Loader that compiles Hinglish (.hin) source code into Python bytecode."""

    def __init__(self, fullname: str, path: str) -> None:
        self.fullname = fullname
        self.path = path

    def get_filename(self, fullname: str) -> str:
        return self.path

    def get_data(self, path: Union[str, bytes]) -> bytes:
        with open(path, "rb") as f:
            return f.read()

    def source_to_code(
        self,
        data: bytes,
        path: Union[str, bytes],
        _optimize: int = -1,
    ):
        source = data.decode("utf-8")
        tree = parse(source)
        compiler = HinglishCompiler()
        py_source, line_map = compiler.compile_with_map(tree)
        from .engine import register_source
        register_source(str(path), source, line_map)
        return compile(py_source, str(path), "exec")


class HinglishPathFinder(importlib.abc.MetaPathFinder):
    """MetaPathFinder that discovers .hin files on sys.path or package paths."""

    @classmethod
    def find_spec(
        cls,
        fullname: str,
        path: Optional[Sequence[str]] = None,
        target: Optional[object] = None,
    ) -> Optional[importlib.machinery.ModuleSpec]:
        search_dirs = path if path is not None else sys.path
        mod_parts = fullname.split(".")
        mod_name = mod_parts[-1]

        for entry in search_dirs:
            entry_path = Path(entry)
            # 1. Direct candidate: <entry>/<mod_name>.hin
            candidate = entry_path / f"{mod_name}.hin"
            if candidate.is_file():
                loader = HinglishSourceLoader(fullname, str(candidate))
                return importlib.machinery.ModuleSpec(fullname, loader, origin=str(candidate))

            # 2. Dotted candidate: <entry>/part1/part2.hin
            rel_candidate = entry_path.joinpath(*mod_parts).with_suffix(".hin")
            if rel_candidate.is_file():
                loader = HinglishSourceLoader(fullname, str(rel_candidate))
                return importlib.machinery.ModuleSpec(fullname, loader, origin=str(rel_candidate))

            # 3. Package candidate: <entry>/part1/part2/__init__.hin
            pkg_candidate = entry_path.joinpath(*mod_parts) / "__init__.hin"
            if pkg_candidate.is_file():
                loader = HinglishSourceLoader(fullname, str(pkg_candidate))
                spec = importlib.machinery.ModuleSpec(
                    fullname, loader, origin=str(pkg_candidate), is_package=True
                )
                spec.submodule_search_locations = [str(pkg_candidate.parent)]
                return spec

        return None


def install_import_hook() -> None:
    """Installs HinglishPathFinder into sys.meta_path if not already present."""
    for finder in sys.meta_path:
        if finder is HinglishPathFinder or (
            isinstance(finder, type) and issubclass(finder, HinglishPathFinder)
        ):
            return
    sys.meta_path.insert(0, HinglishPathFinder)


def uninstall_import_hook() -> None:
    """Removes HinglishPathFinder from sys.meta_path."""
    sys.meta_path = [
        f for f in sys.meta_path
        if f is not HinglishPathFinder and not (
            isinstance(f, type) and issubclass(f, HinglishPathFinder)
        )
    ]
