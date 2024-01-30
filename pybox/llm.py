import gradio as gr
import time

from typing import Callable


class GradioChatWebUI:
    """
    `GradioChatWebUI` allows you to create a chatbot WebUI with Gradio.
    """

    def __init__(
            self, bot_callback: Callable[[str],
                                         str],
            title: str, header: str, chatbox_height=400, input_placeholder="Type your message here...",
            send_button_text="Send", clear_button_text="🗑️", server_port=8000, share=True, colab_stay_awake=False):
        """
        Creates a WebUI for a chatbot.

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
            colab_stay_awake (bool, optional): This will keep Google Colab up. Defaults to False.

        Example:
            ```python
            from pybox.llm import ChatWebUI

            webui = ChatWebUI(
                bot_callback=test_bot,
                title="Test Bot",
                header="# This is a test"
            )

            webui.start()
            ```
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
        self.colab_stay_awake = colab_stay_awake

    def start(self):
        """
        Starts the WebUI.
        """

        with gr.Blocks(css="footer {visibility: hidden}") as app:
            app.title = self.title if self.title != "" else "WebUI"
            gr.Markdown(self.header)

            chatbot = gr.Chatbot(show_label=False) #.style(height=self.chatbox_height)

            with gr.Row():
                with gr.Column(scale=0.80):
                    msg = gr.Textbox(placeholder=self.input_placeholder, show_label=False).style(container=False)
                with gr.Column(scale=0.10):
                    submit = gr.Button(self.send_button_text)
                with gr.Column(scale=0.10):
                    clear = gr.Button(self.clear_button_text)

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
            app.launch(share=self.share, server_port=self.server_port)

            while self.colab_stay_awake:
                time.sleep(600)
                print("|---- Colab is still running ----|")


class Tester:
    """
    `Tester` allows you to test your chatbot by asking questions and saving the results to a CSV file. You can also use a CSV file to test your chatbot.
    """

    def __init__(self, bot_callback: Callable[[str], str], questions: list[str], questions_csv_path=""):
        """
        Creates a tester for a chatbot.

        Args:
            bot_callback (Callable[[str], str]): This is the function Tester calls for interacting with the chatbot.
            questions (list[str]): List of questions to ask the bot.
            questions_csv_path (str, optional): Path to a CSV file containing questions. First column is `Questions`, second column is `Expected Answers`, and the third column is `Bot Answers`. Defaults to "".

        Example:
            ```python
            from pybox.llm import Tester

            tester = Tester(
                bot_callback=test_bot,
                questions=["Hello", "How are you?", "What is your name?"]
            )

            tester.start()
            ```
        """

        self.bot_callback = bot_callback
        self.questions = questions
        self.questions_csv_path = questions_csv_path

    def start(self):
        """
        Starts the tester.
        """

        if self.questions_csv_path != "":
            import pandas as pd
            import csv

            df = pd.read_csv(self.questions_csv_path)
            self.questions = df["Questions"].tolist()
            self.expected_answers = df["Expected Answers"].tolist()

            with open("results.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Questions", "Expected Answers", "Bot Answers"])

            # Start the test
            for question in self.questions:
                answer = self.bot_callback(question)

                with open("results.csv", "a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([question, self.expected_answers[self.questions.index(question)], answer])

        else:
            import csv

            with open("results.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Questions", "Bot Answers"])

            # Start the test
            for question in self.questions:
                answer = self.bot_callback(question)

                with open("results.csv", "a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([question, answer])

        print("Testing complete.")
        print("You can find the results in the results.csv file.")
