#!/usr/bin/env python3

import argparse
from Bot.bot import ChatBot
from Bot.ai import ChatAI
#Change what model you're using here
MODEL_NAME = "124M" #Acceptable values are 124M/355M/774M for OpenAI's GPT2, and "EleutherAI/gpt-neo-125M" for GPT-Neo's model (analogous to openAI 124m)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="John's Epic Chatbot")
    parser.add_argument("--token", dest="token", help="Input")
    parser.add_argument("--response_chance", 
                        dest="response_chance", 
                        help="How likely should the bot respond. For example: give 0.25 for a 25% chance, give 0 for no random responses.")
    parser.add_argument("-t", dest="test", action="store_true", help="Test responses in CLI.")
    args = parser.parse_args()

    if args.test:
        ai = ChatAI()
        ai.load_model()
        print("Type \"exit!!\" to exit.")
        while True:
            inp = input("> ")
            if(inp == "exit!!"):
                return
            print(ai.get_bot_response(MODEL_NAME, author="h!", message=inp))

        return

    else:
        client = ChatBot()
        client.set_response_chance(args.response_chance)
        client.set_model_name(MODEL_NAME)
        client.run(args.token)


if __name__ == "__main__":
    main()
