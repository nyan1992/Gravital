# Full Tutorial
This guide covers the entire setup process for getting your own personal AI chatbot working. Currently, it does not describe how to train the model on your own hardware (mostly because I haven't written that part yet), but if you have an Nvidia GPU and want to do that, then I assume you know what you're doing. Just remember that you need to install the right version of `cudatoolkit` using pip, since pytorch does not use your system's cuda installation. Version info can be found [here.](https://pytorch.org/get-started/locally/)
## Initial Setup
Before we can do anything bot-related or AI-related, we need to "set the table", so to speak, with all of the software and libraries that Gravital uses. 

1. Click "code" at the top of this page and then download the ZIP file, and from there, extract it to its own folder wherever you like.
2. Install the necessary software.
  - Python. I strongly recommend using [Miniconda](https://docs.conda.io/en/latest/miniconda.html) to keep things tidy and contained.
    * If you've got conda, type `conda create --name aibot python=3.9` to set up a new environment for this bot. Then, do `conda activate aibot` to enter it.
  - Install the necessary Python packages using `pip install discord` and then `pip install aitextgen`. This will take a little while, as pytorch is pretty huge.

## Data Gathering And Processing
Any AI needs data to work with, and for this project, that data will be your very own discord server's message history. Before we do anything, though, let's go ahead and get our bot user created. This is essentially the "account" that your bot will use, and conveniently enough, it's also what we'll be using to grab the data!

Create your bot user using [this](https://discordpy.readthedocs.io/en/stable/discord.html) tutorial. Add your bot to your discord server. When done, you're going to want to download the [Discord Chat Exporter](https://github.com/Tyrrrz/DiscordChatExporter/wiki) tool that we're going to be using for this tutorial. It's much easier on Windows than anywhere else, but regardless, follow their wiki to figure out what you're doing and get the channels that you want. Download a few, but not all of them. General channels are your best bet because they always have a lot of conversational text in them. Avoid things like bot command channels and welcome channels, as they're normally stuffed with command outputs and other unsatisfying junk data that we don't want influencing out AI's outputs.

Now is also when you should start to consider the kind of output you want out of your bot. It's probably a good idea to not download any vent-oriented or otherwise serious channels, for example, because you have to remember: garbage in, garbage out. Me and my friends included our debate channel in our bot's model because because we thought it'd be funny to try and debate with it, but it's generally probably not a good idea to include channels focused on anything heated, heavy, or serious. Machines don't have the ettiquite and context awareness that humans do. This thing will be learning from you, and you alone are responsible for what you teach it.

That aside, now that you have your text files, you're going to want to combine them all into one big singular file. Make sure that it's encoded as UTF-8 in order to avoid weird character errors in your generated output. Now, rename your combined file to "rawtext.txt" and move it to the folder where you unzipped this project's code. Now, we have to get rid of things like empty space and the lines indicating which user sent a message, since these are not things we want an interactive chatbot to be saying. Run datacleaner.py to get your complete dataset in a file named dataset.txt. (Alternatively, you could skip this step and do the next step anyway. This would be bad for making a chatbot, but would be great for creating a "conversation simulator" that tries to generate what it thinks a conversation in your server would look like.)

## Training
Now it's time to train our AI! As per the notice at the top of this tutorial, we will be using Google Colab, which gives you (limited) free access to GPUs in the cloud for AI training. [This](https://colab.research.google.com/drive/15qBZx5y9rdaQSyWpsreMDnTiZ5IlN0zD?usp=sharing) "notebook" (a way of storing text right alongside Python code) will walk you through the process. When you get to the `ai.train` cell, be sure to change `save_gdrive` to True so that you don't lose your work. After all is said and done, download your new folder from your google drive, rename it to "trained_model" and move it to the Gravital folder. This contains, well, the trained model, and is the "brain" of the bot. You can swap out this folder for another of the same model at any time, and the bot will continue to work just fine, just with a different way of generating outputs.

## Starting the bot
Now all that's left to do is to run the bot itself! Open up a terminal, and in it, open up the Gravital folder. Run `main.py --token YourBot'sTokenFromEarlier` and Gravital (or whatever you've decided to name yours) will awaken! I recommend you run this same command every time to start it up, as it's more secure then storing your token in plain text within `main.py`, but you can also of course do that if you deem that the convenience to be worth it.

### Options
Gravital comes with some useful command-line arguments for customizing your bot. They are listed below:
- `--help` Prints a quick guide on what these parameters are
- `--response_chance` Sets how likely your bot is to respond to a message without being spoken to, on a scale from 0 (default) to 1. If you enable this option, I recommend confining your bot to a certain channel or channels so that it doesn't spam the whole server or get overloaded.
- `--test` Lets you test your AI without launching the discord bot. You will be able to talk to it one-one-one, providing any input you like. Note that context-awareness (ability to take into account the last several messages instead of just the most recent) is not yet supported in this mode.
