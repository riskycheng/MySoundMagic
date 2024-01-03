import gradio as gr

import MyUtils

with gr.Blocks() as demo:
    error_box = gr.Textbox(label="Error", visible=False)

    name_box = gr.Textbox(label="Name")
    age_box = gr.Number(label="Age", minimum=0, maximum=100)
    symptoms_box = gr.CheckboxGroup(["Cough", "Fever", "Runny Nose"])
    submit_btn = gr.Button("Submit")

    textBoxes = []
    with gr.Column(visible=False) as output_col:
        diagnosis_box = gr.Textbox(label="Diagnosis")
        patient_summary_box = gr.Textbox(label="Patient Summary")

        for i in range(50):
            textbox = gr.Textbox(label=f'textBox @ {i}', visible=False)
            textBoxes.append(textbox)

    def submit(name):
        if len(name) == 0:
            return {error_box: gr.Textbox(value="Enter name", visible=True)}
        print('data ==> ', name)
        sentences = MyUtils.split_long_sentences(name)

        print(len(sentences))

        return {
            output_col: gr.Column(visible=True),
            textBoxes[0]: gr.Textbox(visible=True, value=sentences[0]),
            textBoxes[1]: gr.Textbox(visible=True, value=sentences[1]),
        }

    submit_btn.click(
        submit,
        [name_box],
        [diagnosis_box, patient_summary_box, output_col, textBoxes[0], textBoxes[1]],
    )

demo.launch()
