import gradio as gr
from dotenv import load_dotenv
from gradio.themes.default import Default
from app.research_manager import ResearchManager

load_dotenv(override=True)


async def run(query: str):
    """Stream status updates and final report.

    Returns a tuple (status_log, report_markdown) progressively.
    """
    status_lines: list[str] = []
    report_md: str = ""
    async for event in ResearchManager().run(query):
        if isinstance(event, dict):
            et = event.get("type")
            if et == "status":
                status_lines.append(str(event.get("text", "")))
            elif et == "error":
                status_lines.append(f"ERROR: {event.get('text', '')}")
            elif et == "report":
                report_md = str(event.get("markdown", ""))
        else:
            # Backward compat if any string yields remain
            status_lines.append(str(event))
        yield "\n".join(status_lines), report_md


def build_ui() -> gr.Blocks:
    with gr.Blocks(theme=Default(primary_hue="sky")) as demo:
        gr.Markdown("# Deep Research")
        query_textbox = gr.Textbox(label="What topic would you like to research?")
        run_button = gr.Button("Run", variant="primary")

        # Smaller status box stacked above the final report
        status = gr.Textbox(label="Status", lines=6)
        report = gr.Markdown(label="Report")

        run_button.click(fn=run, inputs=query_textbox, outputs=[status, report])
        query_textbox.submit(fn=run, inputs=query_textbox, outputs=[status, report])
    return demo


# Expose a top-level Gradio app object for Spaces
demo = build_ui()


if __name__ == "__main__":
    demo.launch()
