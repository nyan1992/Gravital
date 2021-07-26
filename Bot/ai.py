from aitextgen import aitextgen
import os
import random


class ChatAI:
    """ ChatAI class handles GPT2 responses and learning """

    def __init__(self) -> None:
        if not os.path.isdir("trained_model"):
            raise Exception(
                "You need to train the model first. Do this in colab or locally and make sure the finished model is in a folder called \"trained_model\".")
        self.ai = aitextgen(model_folder="trained_model")

    def get_bot_response(self, model_name: str, message: str) -> str:
        """ Get a response to a given message using GPT2 model """
        return self.ai.generate(
            model_name=model_name,
            max_length=30,
            prompt=message,
            temperature=0.9,
            return_as_list=True,
        )[0]
