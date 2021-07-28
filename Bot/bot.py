import random
import datetime
import discord
from .ai import ChatAI


class ChatBot(discord.Client):
    """ChatBot handles discord communication. This class runs its own thread that
    persistently watches for new messages, then acts on them when the bots username
    is mentioned. It will use the ChatAI class to generate messages then send them
    back to the configured server channel.

    ChatBot inherits the discord.Client class from discord.py
    """

    def __init__(self, maxlines) -> None:
        self.model_name = "355M"  # Overwrite with set_model_name()
        super().__init__()
        self.maxlines = maxlines  #see comment on main.py line 33

    async def on_ready(self) -> None:
        """ Initializes the GPT2 AI on bot startup """
        print("Logged on as", self.user)
        self.chat_ai = ChatAI(self.maxlines)  # Ready the GPT2 AI generator

    async def on_message(self, message: discord.Message) -> None:
        """ Handle new messages sent to the server channels this bot is watching """

        if message.author == self.user:
            # Skip any messages sent by ourselves so that we don't get stuck in any loops
            return

        # Check to see if bot has been mentioned
        has_mentioned = False
        for mention in message.mentions:
            if str(mention) == self.user.name+"#"+self.user.discriminator:
                has_mentioned = True
                break

        # Only respond randomly (or when mentioned), not to every message
        if random.random() > float(self.response_chance) and has_mentioned == False:
            return

        # Get last n messages, save them to a string to be used as prefix
        context = ""
        # TODO: make limit parameter # configurable through command line args
        history = await message.channel.history(limit=9).flatten()
        history.reverse()  # put in right order
        for msg in history:
            # "context" now becomes a big string containing the content only of the last n messages, line-by-line
            context += msg.content + "\n"
        # probably-stupid way of making every line but the last have a newline after it
        context = context.rstrip(context[-1])
        
        # Print status to console
        print("----------Bot Triggered at {0:%Y-%m-%d %H:%M:%S}----------".format(datetime.datetime.now()))
        print("-----Context for message:")
        print(context)
        print("-----")

        # Process input and generate output
        processed_input = self.process_input(context)
        response = ""
        with message.channel.typing():
            response = self.chat_ai.get_bot_response(processed_input)
        print("----Response Given:")
        print(response)
        print("----")

        await message.channel.send(response)# sends the response

    def process_input(self, message: str) -> str:
        """ Process the input message """
        processed_input = message
        # Convert user ids to just nick names
        processed_input.replace(
            "@"+self.user.name+"#"+self.user.discriminator, "")
        processed_input.replace("@"+self.user.name, "")
        return processed_input

    def set_response_chance(self, response_chance: float) -> None:
        """ Set the response rate """
        self.response_chance = response_chance

    def set_model_name(self, model_name: str = "355M") -> None:
        """ Set the GPT2 model name """
        self.model_name = model_name
