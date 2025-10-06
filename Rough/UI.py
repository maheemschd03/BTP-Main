import gradio as gr
from AI import AI


def echo_prompt(prompt):
    complete_command = f'''

            you are an expert Database enggineer and proficient in SQL queries. You know to solve  any type of problem.
            now you will get some instrutions from the user. you goal is to understand what user wants done and do the same, It will generally involve using your skills only.

            <user instructions start>  {prompt} <user instructions ends>

            Remember, you can use always use sql queries to know the schema if unsure, like you can always use desc table_name etc. do not ask silly questions if there is somehting that you can know
            youself by using a query go for it.
            Try to solve the problems yourself first, you have all the neccsary tools. Do not anounce you plan to user just execute it.
            Always Give the final response in a credible manner with proper details and all the data that was asked for.
            Always return text as the final response.

            respond according to the user instructions. Also be friendly and a good conversation.
            also do not return the quesries execute them . You are an engg not a consultant.
            
            Also at last always verify if this user needs were met or not correctly, verify own your own.


            '''

    return AI(complete_command)


with gr.Blocks(theme=gr.themes.Default()) as demo:
    gr.Markdown(
        """
        # 🧑‍💻 HumanDB - AI-powered Database Assistant
        Enter your request below and let our AI Database Engineer handle it for you!
        """
    )

    with gr.Row():
        prompt_input = gr.Textbox(
            label="What do you want to be done?",
            placeholder="Describe your database query or issue here...",
            lines=4,
            show_copy_button=True
        )

    with gr.Row():
        output_box = gr.Textbox(
            label="Final Output",
            placeholder="The AI's response will appear here...",
            lines=10,
            interactive=False
        )

    submit_button = gr.Button("Run Query 🚀")

    submit_button.click(fn=echo_prompt, inputs=prompt_input, outputs=output_box)

demo.launch(share=True)


