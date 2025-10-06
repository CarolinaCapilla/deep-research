import sys
from pathlib import Path
import importlib.util as _import_util
import pytest


# Load the research_manager module directly to avoid top-level app.py collision
_ROOT = Path(__file__).resolve().parents[1]
# Ensure the project root is importable so 'app' package resolves during module execution
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
_RM_PATH = _ROOT / "app" / "research_manager.py"
_spec = _import_util.spec_from_file_location("research_manager", str(_RM_PATH))
if _spec and _spec.loader:
    research_manager = _import_util.module_from_spec(_spec)  # type: ignore[assignment]
    _spec.loader.exec_module(research_manager)  # type: ignore[attr-defined]
else:
    raise ImportError(f"Failed to load research_manager.py from {_RM_PATH}")


@pytest.mark.asyncio
async def test_research_manager_happy_path_no_email(monkeypatch):
    # Ensure email is not configured so the manager emits the skip message
    monkeypatch.delenv("SENDGRID_API_KEY", raising=False)
    monkeypatch.delenv("SMTP_SERVER", raising=False)

    # Shortcuts to types used by ResearchManager
    WebSearchItem = research_manager.WebSearchItem
    WebSearchPlan = research_manager.WebSearchPlan
    ReportData = research_manager.ReportData

    async def fake_plan_searches(self, query):  # noqa: D401, ANN001
        return WebSearchPlan(searches=[WebSearchItem(query="q1", reason="r1")])

    async def fake_perform_searches(self, plan):  # noqa: D401, ANN001
        return ["summary: ..."]

    async def fake_write_report(self, query, results):  # noqa: D401, ANN001
        return ReportData(
            short_summary="ss",
            markdown_report="Final report",
            follow_up_questions=[],
        )

    # Patch the instance methods directly
    monkeypatch.setattr(
        research_manager.ResearchManager,
        "plan_searches",
        fake_plan_searches,
        raising=True,
    )
    monkeypatch.setattr(
        research_manager.ResearchManager,
        "perform_searches",
        fake_perform_searches,
        raising=True,
    )
    monkeypatch.setattr(
        research_manager.ResearchManager,
        "write_report",
        fake_write_report,
        raising=True,
    )

    mgr = research_manager.ResearchManager()
    events = []
    async for ev in mgr.run("test query"):
        events.append(ev)

    # We should have yielded a final report event
    assert any(ev.get("type") == "report" for ev in events)
    # And a status message indicating email is disabled (since no provider configured)
    assert any(
        ev.get("type") == "status" and "Email sending is disabled" in ev.get("text", "")
        for ev in events
    )
