from agents import Runner, trace, gen_trace_id
from app.search_agent import search_agent
from app.planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from app.writer_agent import writer_agent, ReportData
from app.email_agent import email_agent
import asyncio
import os


class ResearchManager:

    async def run(self, query: str):
        """Run the deep research process, yielding structured events.

        Events are dicts with a 'type' key:
        - {"type": "status", "text": str}
        - {"type": "error", "text": str}
        - {"type": "report", "markdown": str}
        """
        trace_id = gen_trace_id()
        yield {"type": "status", "text": f"Trace: {trace_id}"}
        try:
            with trace("Research trace", trace_id=trace_id):
                print("Starting research...")
                yield {"type": "status", "text": "Planning searches..."}
                search_plan = await self.plan_searches(query)

                yield {
                    "type": "status",
                    "text": "Searches planned, starting to search...",
                }
                search_results = await self.perform_searches(search_plan)

                yield {"type": "status", "text": "Searches complete, writing report..."}
                report = await self.write_report(query, search_results)

                email_configured = bool(
                    os.environ.get("SENDGRID_API_KEY") or os.environ.get("SMTP_SERVER")
                )
                if email_configured:
                    yield {"type": "status", "text": "Report written, sending email..."}
                    send_result = await self.send_email(report)
                    # Surface tool outcome for visibility
                    if isinstance(send_result, dict):
                        status = send_result.get("status")
                        code_or_reason = send_result.get("code") or send_result.get(
                            "reason"
                        )
                        if status == "success":
                            yield {
                                "type": "status",
                                "text": f"Email sent (code: {code_or_reason})",
                            }
                        elif status == "skipped":
                            yield {
                                "type": "status",
                                "text": f"Email skipped: {code_or_reason}",
                            }
                        else:
                            yield {
                                "type": "status",
                                "text": f"Email status: {status} ({code_or_reason})",
                            }
                    else:
                        yield {
                            "type": "status",
                            "text": f"Email tool returned: {send_result}",
                        }
                else:
                    yield {
                        "type": "status",
                        "text": (
                            "Report written. Email sending is disabled in this deployment for security "
                            "(no email provider configured). To enable locally, set SENDGRID_API_KEY or "
                            "SMTP_SERVER in your .env."
                        ),
                    }

                yield {"type": "report", "markdown": report.markdown_report}
        except Exception as e:
            yield {"type": "error", "text": f"Unexpected error: {e}"}

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """Plan the searches to perform for the query"""
        print("Planning searches...")
        result = await Runner.run(
            planner_agent,
            f"Query: {query}",
        )
        print(f"Will perform {len(result.final_output.searches)} searches")
        return result.final_output_as(WebSearchPlan)

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """Perform the searches to perform for the query"""
        print("Searching...")
        num_completed = 0
        tasks = [
            asyncio.create_task(self.search(item)) for item in search_plan.searches
        ]
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1
            print(f"Searching... {num_completed}/{len(tasks)} completed")
        print("Finished searching")
        return results

    async def search(self, item: WebSearchItem) -> str | None:
        """Perform a search for the query"""
        input = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            result = await Runner.run(
                search_agent,
                input,
            )
            return str(result.final_output)
        except Exception:
            return None

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """Write the report for the query"""
        print("Thinking about report...")
        input = f"Original query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(
            writer_agent,
            input,
        )

        print("Finished writing report")
        return result.final_output_as(ReportData)

    async def send_email(self, report: ReportData) -> None:
        print("Writing email...")
        result = await Runner.run(
            email_agent,
            report.markdown_report,
        )
        # Log final tool output for debugging (success/skip/error details)
        try:
            out = result.final_output
        except Exception:
            out = None
        print(f"send_email result: {out}")
        return out
