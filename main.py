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
                        help="How likely should the bot respond. For example: give 0.25 for a 25%% chance, give 0 for no random responses.")
    parser.add_argument("--test", dest="test", action="store_true",
                        help="Test model by talking to the AI right in the CLI.")
    parser.add_argument("--maxlines", dest="maxlines", help="The maximum number of lines that the AI will try to generate per message. Will always generate random amount up to this value, which defaults to 1.",
                        default=1)
    args = parser.parse_args()

    if args.test:
        ai = ChatAI(args.maxlines)  # see comment on line 33
        print("Type \"exit!!\" to exit.")
        while True:
            inp = input("> ")
            if(inp == "exit!!"):
                return
            print(ai.get_bot_response(message=inp))

    else:
        client = ChatBot(args.maxlines)  # probably a cleaner way to do this than to pass the maxlines param all the way through? submit PR if you know
        client.set_response_chance(args.response_chance)
        if args.token is None:
            raise Exception(
                "You are trying to launch the bot but have not included your discord bot's token with --token. Please include this and try again.")
        client.run(args.token)


if __name__ == "__main__":
    main()
