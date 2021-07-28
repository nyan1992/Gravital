#!/usr/bin/env python3

import argparse
from Bot.bot import ChatBot
from Bot.ai import ChatAI


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="John's Epic Chatbot")
    parser.add_argument("--token", dest="token",
                        help="Your discord bot's token. Required for launching the bot in non-test mode!")
    parser.add_argument("--response_chance",
                        dest="response_chance",
                        default=0,
                        help="How likely the bot is to respond to a message in which it is not pinged. For example: give 0.25 for a 25%% chance, give 0 for no random responses. Defaults to 0.")
    parser.add_argument("--test", dest="test", action="store_true",
                        help="Test model by talking to the AI right in the terminal.")
    parser.add_argument("--maxlines", dest="maxlines", help="The maximum number of lines that the AI will try to generate per message. Will always generate random amount up to this value, which defaults to 1.",
                        default=1)
    parser.add_argument("--train", dest="train", action="store_true",
                        help="Trains the model on a file named dataset.txt. Only use this if you have a good NVIDIA GPU. Overwrites existing trained_model folder. Currently untested!")
    args = parser.parse_args()

    if args.test:
        ai = ChatAI(args.maxlines)  # see comment on line 33
        print("Type \"exit!!\" to exit.")
        while True:
            inp = input("> ")
            if(inp == "exit!!"):
                return
            print(ai.get_bot_response(message=inp))
    elif args.train:
        ai = ChatAI(togpu=True)
        ai.gpt2.train("dataset.txt",
                      line_by_line=False,
                      from_cache=False,
                      num_steps=5000, #Takes less than an hour on my RTX 3060. Increase if you want, but remember that training can pick up where it left off after this finishes.
                      generate_every=1000,
                      save_every=1000,
                      learning_rate=1e-3,
                      fp16=True, #this setting improves memory efficiency, disable if it causes issues
                      batch_size=2,
                      )
    else:
        # probably a cleaner way to do this than to pass the maxlines param all the way through? submit PR if you know
        client = ChatBot(args.maxlines)
        client.set_response_chance(args.response_chance)
        if args.token is None:
            raise Exception(
                "You are trying to launch the bot but have not included your discord bot's token with --token. Please include this and try again.")
        client.run(args.token)


if __name__ == "__main__":
    main()
