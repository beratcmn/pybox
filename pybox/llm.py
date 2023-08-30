import gradio as gr
import time

from typing import Callable


class ChatWebUI:
    def __init__(
            self, bot_callback: Callable[[str],
                                         str],
            title: str, header: str, chatbox_height=400, input_placeholder="Type your message here...",
            send_button_text="Send", clear_button_text="🗑️", server_port=8000, share=True):
        """
        #### Creates a WebUI for a chatbot.

        Args:
            bot_callback (Callable[[str], str]): This is the function WebUI calls for interacting with the chatbot.
            title (str): Title of the webpage.
            header (str): Header of the webpage.
            chatbox_height (int, optional): Chatbox Height. Defaults to 400.
            input_placeholder (str, optional): Inputbox placeholder. Defaults to "Type your message here...".
            send_button_text (str, optional): Defaults to "Send".
            clear_button_text (str, optional): Defaults to "🗑️".
            server_port (int, optional): Defaults to 8000.
            share (bool, optional): Defaults to True.
        """

        self.bot_callback = bot_callback
        self.title = title
        self.header = header
        self.chatbox_height = chatbox_height
        self.input_placeholder = input_placeholder
        self.send_button_text = send_button_text
        self.clear_button_text = clear_button_text
        self.server_port = server_port
        self.share = share

    def start_webui(self):
        """
        #### Starts the WebUI.
        """

        with gr.Blocks(css="footer {visibility: hidden}") as app:
            app.title = self.title if self.title != "" else "WebUI"
            gr.Markdown(self.header)

            chatbot = gr.Chatbot(show_label=False).style(height=self.chatbox_height)

            with gr.Row():
                with gr.Column(scale=0.90):
                    msg = gr.Textbox(placeholder=self.input_placeholder, show_label=False).style(container=False)
                with gr.Column(scale=0.05):
                    submit = gr.Button(self.send_button_text)
                with gr.Column(scale=0.05):
                    clear = gr.Button(self.clear_button_text)

            userMessage = ""

            def user(user_message, history):
                global userMessage
                userMessage = user_message
                return "", history + [[user_message, None]]

            def bot(history):
                bot_message = self.bot_callback(userMessage)
                history[-1][1] = ""
                for character in bot_message:
                    history[-1][1] += character
                    time.sleep(0.05)
                    yield history

            msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
                bot, chatbot, chatbot
            )

            submit.click(user, [msg, chatbot], [msg, chatbot], queue=False).then(
                bot, chatbot, chatbot
            )

            clear.click(lambda: None, None, chatbot, queue=False)

            gr.close_all()
            app.queue(concurrency_count=4)
            app.launch(share=self.share, port=self.server_port)
