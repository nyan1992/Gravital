from aitextgen import aitextgen
import os
import random


class ChatAI:
    """ ChatAI class handles the AI's responses """

    def __init__(self, max_response_lines=1, togpu=False) -> None:
        if not os.path.isdir("trained_model"):
            raise Exception(
                "You need to train the model first. Do this in colab or locally and make sure the finished model is in a folder called \"trained_model\".")
        self.gpt2 = aitextgen(model_folder="trained_model", to_gpu=togpu)
        self.maxlines = int(max_response_lines)

    def get_bot_response(self, message: str) -> str:
        """ Get a processed response to a given message using GPT model """
        text = self.gpt2.generate(
            # ahead: dumb and hacky way of setting the length right (taking maxlines into account) until "include_prompt=False" becomes a thing. will never be exact
            max_length=len(message.split()) + 70 + 5*self.maxlines,
            prompt=message + "\n",
            temperature=0.9,
            return_as_list=True,
        )[0]
        text = text.replace(message, "") # remove the input text from the output text
        output = ""
        for i in range(0, random.randint(1, self.maxlines)):  # include a random amount of lines up to maxlines in the response
            try:
                print(text.splitlines()[i + 1])
                output += text.splitlines()[i + 1] + "\n"
            except:
                continue
        return output.rstrip(output[-1]) # shaves off that last newline character like in bot.py, prob better way to do this