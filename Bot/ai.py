from aitextgen import aitextgen
import os
import random


class ChatAI:
    """ ChatAI class handles the AI's responses """

    def __init__(self) -> None:
        if not os.path.isdir("trained_model"):
            raise Exception(
                "You need to train the model first. Do this in colab or locally and make sure the finished model is in a folder called \"trained_model\".")
        self.ai = aitextgen(model_folder="trained_model")

    def get_bot_response(self, model_name: str, message: str) -> str:
        """ Get a processed response to a given message using GPT model """
        text =  self.ai.generate(
            model_name=model_name,
            max_length=30,
            prompt=message + "\n",
            temperature=0.9,
            return_as_list=True,
        )[0]
        # print("--PRE TRUNCATION OUTPUT--")
        # print(text)
        # print("--------------------------")
        text = text.replace(message, "")#this is a hacky solution in place until aitextgen implements an "include prefix" parameter
        return text
