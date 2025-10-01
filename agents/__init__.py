"""Local package shim to avoid shadowing and re-export symbols from the real library.

This package re-exports Agent/Runner/tools from the installed `openai-agents` library so
imports like `from agents import Agent, Runner, ...` work both locally and on Hosts like HF.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Generator
import uuid

try:
    # Primary: openai-agents package installs as `openai_agents`
    from openai_agents import (  # type: ignore
        Agent,
        Runner,
        WebSearchTool,
        ModelSettings,
        function_tool,
        trace,  # some versions export trace/gen_trace_id at top-level
        gen_trace_id,
    )
except Exception:  # pragma: no cover - provide graceful fallbacks for optional exports
    try:
        # Try importing core symbols; trace helpers may live under a submodule
        from openai_agents import (  # type: ignore
            Agent,
            Runner,
            WebSearchTool,
            ModelSettings,
            function_tool,
        )
        try:
            from openai_agents.tracing import trace, gen_trace_id  # type: ignore
        except Exception:
            # Minimal no-op trace and a simple UUID trace id as a safe fallback
            @contextmanager
            def trace(_: str, trace_id: str | None = None) -> Generator[None, None, None]:
                yield None

            def gen_trace_id() -> str:
                return str(uuid.uuid4())
    except Exception as e:  # Raise a clear error explaining the requirement
        raise ImportError(
            "The local 'agents' package re-exports from the 'openai-agents' library, but it "
            "could not be imported. Ensure 'openai-agents' is listed in requirements and "
            "installed in your environment. Original error: " + str(e)
        )

__all__ = [
    "Agent",
    "Runner",
    "WebSearchTool",
    "ModelSettings",
    "function_tool",
    "trace",
    "gen_trace_id",
]

