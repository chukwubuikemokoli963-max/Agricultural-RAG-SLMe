
import inspect
import gradio as gr

CSS = """
:root {
    --farm-main: #F5F7F6;
    --farm-background: #0D1F17;
    --farm-text: #111815;
    --farm-highlight: #E2ECE7;
}

body, .gradio-container {
    background: #0D1F17 !important;
}

.gradio-container {
    max-width: 1000px !important;
    margin: auto !important;
    padding: 24px !important;
    font-family: Inter, system-ui, sans-serif !important;
}

#farm-header {
    background: #0D1F17 !important;
    border: none !important;
    padding: 10px 0 24px !important;
}

.farm-brand {
    display: flex;
    align-items: center;
    gap: 14px;
}

.farm-brand h1 {
    color: #F5F7F6 !important;
    font-size: 30px;
    font-weight: 750;
    letter-spacing: -1px;
    margin: 0;
}

.farm-brand p {
    color: #E2ECE7 !important;
    font-size: 12px;
    margin: 4px 0 0;
}

#farm-main, #farm-response {
    background: #F5F7F6 !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 26px !important;
}

#farm-main h1,
#farm-main h2,
#farm-main h3,
#farm-main p,
#farm-main label,
#farm-main span,
#farm-response h1,
#farm-response h2,
#farm-response h3,
#farm-response p,
#farm-response li,
#farm-response span {
    color: #111815 !important;
}

.farm-eyebrow {
    color: #111815;
    font-size: 11px;
    font-weight: 650;
    letter-spacing: 2px;
}

.farm-intro h2 {
    font-size: 36px;
    letter-spacing: -1.5px;
    line-height: 1.15;
    margin: 12px 0;
}

#farm-question,
#farm-question textarea {
    background: #E2ECE7 !important;
    color: #111815 !important;
    border-radius: 12px !important;
    border-color: #E2ECE7 !important;
}

#farm-question textarea {
    padding: 16px !important;
    font-size: 16px !important;
    min-height: 120px !important;
}

#farm-submit {
    background: #0D1F17 !important;
    color: #F5F7F6 !important;
    border: none !important;
    border-radius: 10px !important;
    min-height: 50px !important;
    font-weight: 650 !important;
}

#farm-clear {
    background: #E2ECE7 !important;
    color: #111815 !important;
    border: none !important;
    border-radius: 10px !important;
}

.topic-button {
    background: #E2ECE7 !important;
    color: #111815 !important;
    border: 1px solid #E2ECE7 !important;
    border-radius: 12px !important;
    min-height: 70px !important;
    text-align: left !important;
}

.topic-button:hover {
    border-color: #0D1F17 !important;
}

#farm-answer {
    background: #F5F7F6 !important;
    color: #111815 !important;
    padding: 12px !important;
    line-height: 1.8 !important;
}

#farm-sources {
    background: #E2ECE7 !important;
    color: #111815 !important;
    border-radius: 12px !important;
}

.edge-badge {
    display: inline-block;
    background: #E2ECE7;
    color: #0D1F17 !important;
    border-radius: 30px;
    padding: 7px 15px;
    font-size: 12px;
    font-weight: 650;
}

.farm-footer {
    color: #E2ECE7 !important;
    font-size: 12px;
    text-align: center;
    line-height: 1.7;
    padding: 20px 5px;
}

footer {
    display: none !important;
}

@media (max-width: 600px) {

    .gradio-container {
        padding: 12px !important;
    }

    #farm-main, #farm-response {
        padding: 18px !important;
        border-radius: 16px !important;
    }

    .farm-intro h2 {
        font-size: 28px;
    }

    .farm-brand h1 {
        font-size: 26px;
    }
}
"""

THEME = gr.themes.Soft(
    primary_hue="green",
    secondary_hue="green",
    neutral_hue="gray"
)

HEADER = """
<div class="farm-brand">

    <svg width="48" height="48"
         viewBox="0 0 48 48">

        <rect width="48" height="48"
              rx="13" fill="#E2ECE7"/>

        <path d="M24 37V17
                 M24 27C10 27 10 13 10 13
                 C24 13 24 27 24 27Z
                 M24 22C24 8 38 9 38 9
                 C38 22 24 22 24 22Z"
              stroke="#0D1F17"
              stroke-width="2.5"
              stroke-linecap="round"
              stroke-linejoin="round"
              fill="none"/>

    </svg>

    <div>
        <h1>FarmDoc</h1>
        <p>Powered by Agricultural RAG SLMe</p>
    </div>

</div>
"""

def build_farmdoc(
    response_handler,
    api_handler=None,
    initial_edge=False
):

    block_options = {
        "title": "FarmDoc",
        "analytics_enabled": False
    }

    block_parameters = inspect.signature(
        gr.Blocks
    ).parameters

    if "css" in block_parameters:
        block_options["css"] = CSS

    if "theme" in block_parameters:
        block_options["theme"] = THEME

    with gr.Blocks(**block_options) as app:

        # ==================================
        # HEADER
        # ==================================

        with gr.Row(elem_id="farm-header"):

            with gr.Column(scale=5):

                gr.HTML(HEADER)

            with gr.Column(scale=1, min_width=80):

                edge_indicator = gr.HTML(
                    value=(
                        '<span class="edge-badge">'
                        '● Edge</span>'
                        if initial_edge else ""
                    )
                )

        # ==================================
        # MAIN INTERFACE
        # ==================================

        with gr.Column(elem_id="farm-main"):

            gr.HTML("""
            <div class="farm-intro">

                <div class="farm-eyebrow">
                    YOUR AGRICULTURAL ASSISTANT
                </div>

                <h2>
                    How can we help your farm today?
                </h2>

                <p>
                    Ask a farming question in English
                    or Nigerian Pidgin.
                </p>

            </div>
            """)

            question = gr.Textbox(
                placeholder=(
                    "Describe what is happening "
                    "on your farm..."
                ),
                lines=4,
                max_lines=8,
                show_label=False,
                elem_id="farm-question"
            )

            with gr.Row():

                clear = gr.Button(
                    "Clear",
                    elem_id="farm-clear",
                    scale=1
                )

                submit = gr.Button(
                    "Ask FarmDoc ↗",
                    variant="primary",
                    elem_id="farm-submit",
                    scale=3
                )

            gr.Markdown("### Explore farming topics")

            with gr.Row():

                crop = gr.Button(
                    "🌿 Crop health",
                    elem_classes=["topic-button"]
                )

                water = gr.Button(
                    "💧 Water & rainfall",
                    elem_classes=["topic-button"]
                )

            with gr.Row():

                soil = gr.Button(
                    "🌱 Soil & nutrients",
                    elem_classes=["topic-button"]
                )

                pest = gr.Button(
                    "🐛 Pest management",
                    elem_classes=["topic-button"]
                )

            crop.click(
                lambda: (
                    "Wetin dey cause my cassava "
                    "leaf to turn yellow?"
                ),
                outputs=question,
                queue=False
            )

            water.click(
                lambda: (
                    "Rain no dey fall, wetin I go do?"
                ),
                outputs=question,
                queue=False
            )

            soil.click(
                lambda: (
                    "Which manure go make my yam "
                    "grow well?"
                ),
                outputs=question,
                queue=False
            )

            pest.click(
                lambda: (
                    "Wetin dey chop my tomato leaf?"
                ),
                outputs=question,
                queue=False
            )

        # ==================================
        # RESPONSE
        # ==================================

        with gr.Column(elem_id="farm-response"):

            gr.Markdown("## FarmDoc response")

            answer = gr.Markdown(
                "Your agricultural information "
                "will appear here.",
                elem_id="farm-answer"
            )

            with gr.Accordion(
                "Supporting evidence",
                open=False,
                elem_id="farm-sources"
            ):

                sources = gr.Markdown(
                    "No supporting documents yet."
                )

        # ==================================
        # RESEARCH DISCLOSURE
        # ==================================

        gr.HTML("""
        <div class="farm-footer">

            <strong>FarmDoc</strong><br>

            Powered by Agricultural RAG SLMe

            <p>
                Research prototype using agricultural
                benchmark documents, including synthetic
                evidence. Not a confirmed crop diagnosis.
                Consult an agricultural extension officer
                before applying treatments.
            </p>

        </div>
        """)

        outputs = [
            answer,
            sources,
            edge_indicator
        ]

        submit.click(
            response_handler,
            inputs=question,
            outputs=outputs,
            concurrency_limit=1
        )

        question.submit(
            response_handler,
            inputs=question,
            outputs=outputs,
            concurrency_limit=1
        )

        clear.click(
            lambda: (
                "",
                "Your agricultural information "
                "will appear here.",
                "No supporting documents yet."
            ),
            outputs=[
                question,
                answer,
                sources
            ],
            queue=False
        )

        # ==================================
        # MACHINE-READABLE REMOTE ENDPOINT
        # ==================================

        if api_handler is not None:

            with gr.Column(visible=False):

                api_question = gr.Textbox()
                api_result = gr.JSON()
                api_button = gr.Button()

            api_button.click(
                api_handler,
                inputs=api_question,
                outputs=api_result,
                api_name="farmdoc_api",
                concurrency_limit=1
            )

    return app


def launch_farmdoc(app, **kwargs):

    parameters = inspect.signature(
        app.launch
    ).parameters

    if "css" in parameters:
        kwargs["css"] = CSS

    if "theme" in parameters:
        kwargs["theme"] = THEME

    return app.queue(
        default_concurrency_limit=1,
        max_size=10
    ).launch(**kwargs)
