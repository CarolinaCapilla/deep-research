import gradio as gr
from dotenv import load_dotenv
from gradio.themes.default import Default
from app.research_manager import ResearchManager

load_dotenv(override=True)


async def run(query: str):
    async for chunk in ResearchManager().run(query):
        yield chunk


def build_ui() -> gr.Blocks:
    with gr.Blocks(theme=Default(primary_hue="sky")) as demo:
        gr.Markdown("# Deep Research")
        query_textbox = gr.Textbox(label="What topic would you like to research?")
        run_button = gr.Button("Run", variant="primary")
        report = gr.Markdown(label="Report")

        run_button.click(fn=run, inputs=query_textbox, outputs=report)
        query_textbox.submit(fn=run, inputs=query_textbox, outputs=report)
    return demo


# Expose a top-level Gradio app object for Spaces
demo = build_ui()


if __name__ == "__main__":
    demo.launch()


