"""Hinglish Debug Adapter Protocol (DAP) package.

Provides zero-runtime-dependency Debug Adapter for VS Code and DAP clients.
"""

from .debugger import HinglishDebugger
from .protocol import (
    Breakpoint,
    DapMessageBuilder,
    Scope,
    Source,
    StackFrame,
    ThreadInfo,
    Variable,
    read_dap_message,
    write_dap_message,
)
from .server import HinglishDebugAdapterServer, main

__all__ = [
    "HinglishDebugger",
    "HinglishDebugAdapterServer",
    "Breakpoint",
    "Source",
    "StackFrame",
    "Scope",
    "Variable",
    "ThreadInfo",
    "DapMessageBuilder",
    "read_dap_message",
    "write_dap_message",
    "main",
]
