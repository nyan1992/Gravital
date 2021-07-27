## What's This?
This is my ongoing attempt at adapting NickBrisebois' project from using [gpt-2-simple](https://github.com/minimaxir/gpt-2-simple) to using [aitextgen](https://github.com/minimaxir/aitextgen). In my own experience, trying to train the model locally with my 3060 was a version-incompatibility dependency nightmare (mostly because of gpt-2-simple's reliance on old tensorflow, which relied on old python and old CUDA, which relied on older drivers on Linux, etc), and I ended up just doing it in colab and copying that model over, which I was never really satisfied with. 

I'm intending to solve this by switching the project over to using aitextgen as the new backend. It's created by the same person as gpt-2-simple, and has been officially named as its successor, boasting faster and more memory efficient generation, support for GPT Neo, and, most importantly, compatibility with modern versions of TensorFlow and CUDA. This should make it easier to train models on modern hardware as well as generally speed things up (generation time on CPU so far is looking slightly better than before as promised).

## Project status?
**Early, but kind of functional!** It's kind of barebones, and doesn't do all that I want it to, but to my surprise it works just fine and generates text really fast. Improvements and features on the way.

## What are you planning on changing?
At least for now, I'm getting rid of the Docker parts of the project, since I don't quite yet know what I'm doing with that enough to continue it. I'll add it back in later, but the no-gpu training option is staying gone in favor of including a simple tutorial on how to train your model in colab and port it over to the bot.

I'll be rewriting a lot of the `ChatAI` class in order to adapt it to aitextgen, and because of that, at least for right now anything training-related is going to be moved to a separate script and taken out of the main file's args.

I also plan on making this new bot context-aware: it will pull the last several messages sent in a given channel and use them as a prefix for generating a response. I did this before and in my experience it makes the text much more appropriate and conversational, at the cost of sometimes getting stuck in a pattern repeating itself with very similar messages before people break it out of it by talking about something else.

## Known / expected issues and roadblocks?
aitextgen does not yet include a function to truncate the prefix of a generated sample, which could end up being an issue, although I have some hacky workarounds in mind. Training on windows is also in my experience non-functional, as per this issue: https://github.com/minimaxir/aitextgen/issues/9

# Full Tutorial
This guide covers the entire setup process for getting your own personal AI chatbot working. Currently, it does not describe how to train the model on your own hardware (mostly because I haven't written that part yet), but if you have an Nvidia GPU and want to do that, then I assume you know what you're doing. Just remember that you need to install the right version of `cudatoolkit` using pip, since pytorch does not use your system's cuda installation. Version info can be found [here.](https://pytorch.org/get-started/locally/)
## Initial Setup
Before we can do anything bot-related or AI-related, we need to "set the table", so to speak, with all of the software and libraries that DiscordChatAI-GPT2 uses. 

1. Click "code" at the top of this page and then download the ZIP file, and from there, extract it to its own folder wherever you like.
2. Install the necessary software.
  - Python. I strongly recommend using [Miniconda](https://docs.conda.io/en/latest/miniconda.html) to keep things tidy and contained.
    * If you've got conda, type `conda create --name aibot python=3.9` to set up a new environment for this bot. Then, do `conda activate aibot` to enter it.
  - Install the necessary Python packages using `pip install discord` and then `pip install aitextgen`. This will take a little while.

## Data Gathering And Processing
Any AI needs data to work with, and for this project, that data will be your very own discord server's message history. Before we do anything, though, let's go ahead and get our bot user created. This is essentially the "account" that your bot will use, and conveniently enough, it's also what we'll be using to grab the data!

Create your bot user using [this](https://discordpy.readthedocs.io/en/stable/discord.html) tutorial. Add your bot to your discord server. When done, you're going to want to download the [Discord Chat Exporter](https://github.com/Tyrrrz/DiscordChatExporter/wiki) tool that we're going to be using for this tutorial. It's much easier on Windows than anywhere else, but regardless, follow their wiki to figure out what you're doing and get the channels that you want. Download a few, but not all of them. General channels are your best bet because they always have a lot of conversational text in them. Avoid things like bot command channels, as they're normally stuffed with command outputs and other unsatisfying junk data that we don't want influencing out AI's outputs.
