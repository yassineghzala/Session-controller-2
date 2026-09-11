import os
import random
import re
import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


# ==========================================
# CHANNEL OWNERS
# ==========================================


CHANNEL_OWNERS = {
    "ayar": 514118592514752533,
    "ghzela": 395712756927561728,
    "zya": 639851669701525514
}


BOT_INTERACTIONS_CHANNEL = "bot-interactions"

WORD_RESPONSES = {
    "ah": "3asba",
    "six": "seven",
    "fat": "ass",
    "good": "boy",
    "zebi" : "creaming you",
}

EIGHT_BALL_ANSWERS = [
    "Absolutely.",
    "The canvas says yes.",
    "Maybe after one more coffee.",
    "Ask again when the lighting is better.",
    "I would not bet the whole painting on it.",
    "The vibes are surprisingly good.",
    "No. Add more contrast first.",
]

ART_PROMPTS = [

    # ==========================================
    # FUNNY
    # ==========================================

    "An animal trying to look intimidating",

    "Someone having the worst possible day",

    "A completely unnecessary amount of drama",

    "Someone who clearly made a terrible decision",

    "An animal in a situation it has no business being in",

    "Someone trying very hard to look cool",

    "A villain doing something extremely mundane",

    "A hero who is having second thoughts",

    "Someone caught doing something they shouldn't",

    "A very serious person surrounded by complete chaos",

    "Someone who just realized they forgot something important",

    "A character with a very embarrassing secret",

    "An animal dressed for a formal occasion",

    "Someone trying to impress someone else",

    "The most awkward interaction imaginable",

    "A character who desperately needs a vacation",

    "Someone pretending everything is fine",

    "A completely normal situation taken way too seriously",

    "A character whose plan has gone horribly wrong",

    "Something that would make a terrible superpower",


    # ==========================================
    # COOL / CINEMATIC
    # ==========================================

    "A character entering a place they shouldn't be",

    "A powerful character at their weakest moment",

    "A mysterious figure arriving somewhere",

    "A city at night",

    "A journey through an unfamiliar place",

    "A character preparing for something important",

    "A confrontation",

    "A character surrounded by people but completely alone",

    "A world after something has gone terribly wrong",

    "A place that looks impossible to reach",

    "A character standing somewhere far above the world",

    "A moment of complete silence before chaos",

    "A character discovering something unexpected",

    "A place hiding something beneath its surface",

    "A character walking away from something important",

    "A world where something fundamental is different",

    "A character with an unknown past",

    "A final encounter",

    "A journey that looks like it has no destination",

    "A place that feels like it belongs to another world",


    # ==========================================
    # CHARACTERS
    # ==========================================

    "Design a character based on a random object",

    "Design a character who looks friendly but isn't",

    "Design a character who looks terrifying but isn't",

    "Design a character with a very unusual job",

    "Design a character whose personality is obvious from their clothes",

    "Design a character who has clearly been through something",

    "Design a character from a world completely different from ours",

    "Design a character who doesn't fit into their own world",

    "Design a character with an unusual companion",

    "Design a character who is extremely confident",

    "Design a character who has absolutely no idea what they're doing",

    "Design a character who is hiding something",

    "Design a character using an unusual color palette",

    "Design a character based on a song",

    "Design a character based on a random word",

    "Design a character you would actually want to meet",

    "Design a character you would absolutely avoid",

    "Design a character who looks like they belong to another genre",


    # ==========================================
    # WORLDS / ENVIRONMENTS
    # ==========================================

    "A place where humans were never supposed to live",

    "A place that has been abandoned for a very long time",

    "A place that has suddenly become completely empty",

    "A place where nature has taken over",

    "A place during an unusual weather event",

    "A place that looks peaceful but isn't",

    "A place where something impossible is completely normal",

    "A place built around something enormous",

    "A place that exists far above the ground",

    "A place hidden beneath another place",

    "A place at the edge of civilization",

    "A place during its busiest moment",

    "A place during its quietest moment",

    "A place that looks completely different at night",

    "A place from a world where technology developed differently",

    "A place that looks like people left in a hurry",

    "A place where different eras somehow exist together",

    "A place that you would want to explore",

    "A place that you would immediately want to leave",


    # ==========================================
    # ANIMALS / CREATURES
    # ==========================================

    "An animal with an unusual occupation",

    "An animal adapted to an extreme environment",

    "An animal that looks completely harmless but isn't",

    "An animal that looks dangerous but is actually friendly",

    "An animal with an unexpected companion",

    "An animal that has clearly seen some things",

    "An animal living somewhere completely unexpected",

    "An animal as imagined by another civilization",

    "A creature that could realistically exist",

    "A creature that absolutely should not exist",

    "A creature built for a specific environment",

    "A creature that looks ancient",

    "A creature that looks futuristic",

    "A creature designed around an unusual ability",


    # ==========================================
    # OBJECTS / THINGS
    # ==========================================

    "An ordinary object with an extraordinary purpose",

    "An object that has clearly been used for years",

    "An object from the future",

    "An object from a forgotten civilization",

    "An object that should never have been invented",

    "An object that is far too large for its purpose",

    "An object that is far too small for its purpose",

    "An object that looks harmless but isn't",

    "An object that you would desperately want to own",

    "An object that you would never want to find",

    "A machine that does something completely unexpected",

    "Something broken that is still useful",

    "Something ordinary redesigned for another world",

    "Something you would find in the pocket of a mysterious person",


    # ==========================================
    # STORY / SCENES
    # ==========================================

    "Someone arriving somewhere",

    "Someone leaving somewhere",

    "A group of people waiting for something",

    "Two characters meeting for the first time",

    "Two characters who clearly know each other",

    "A character discovering something",

    "A character hiding something",

    "A character making an important choice",

    "A character realizing something too late",

    "A character returning somewhere after many years",

    "A celebration that isn't going as planned",

    "A journey coming to an end",

    "The aftermath of an event",

    "The beginning of an adventure",

    "A normal day that suddenly becomes strange",

    "A situation where nobody knows what to do",

    "A character seeing something they weren't supposed to see",

    "A moment that changes everything",

    "A group of strangers forced to work together",


    # ==========================================
    # STYLE / CREATIVE FREEDOM
    # ==========================================

    "Draw something in a style you normally wouldn't use",

    "Draw something as if it came from another era",

    "Draw something as if it came from the future",

    "Draw something inspired by the last thing you watched",

    "Draw something inspired by the last song you heard",

    "Draw someone else in the style of the last anime you watched",

    "Redesign something familiar in your own style",

    "Take something familiar and completely change its context",

    "Combine two things that normally don't belong together",

    "Make something ordinary look extremely expensive",

    "Make something beautiful look slightly wrong",

    "Make something intimidating look adorable",

    "Make something cute look terrifying",

    "Take a familiar idea and give it a completely different setting",


    # ==========================================
    # CHALLENGES
    # ==========================================

    "Use only three colors",

    "Use a color palette you normally wouldn't choose",

    "Draw without using your usual art style",

    "Draw something using as little detail as possible",

    "Draw something with an absurd amount of detail",

    "Draw from an unusual perspective",

    "Draw something without using your usual medium",

    "Start with a random shape and turn it into something",

    "Let someone else choose one element of your artwork",

    "Draw for exactly 15 minutes",

    "Draw the first idea that comes to mind",

    "Draw something without looking at references",

    "Take an old idea and completely redesign it",

    "Draw something based on three random words",

    "Make a serious artwork out of a ridiculous idea",


    # ==========================================
    # FRIEND / EASTER EGG
    # ==========================================

    "Draw one of your friends as a fictional character",

    "Draw one of your friends as a villain",

    "Draw one of your friends as a hero",

    "Draw yourself as imagined by one of your friends",

    "Redesign one of your friend's characters",

    "Draw a character inspired by someone's personality",

    "Give another person a prompt and interpret it your own way",

    "Everyone draws the same idea without seeing each other's work",

    "Draw something inspired by something another person made",

    "Take one of your friend's ideas and make it completely different",

    "Draw yourself as a character from the last game you played",

    "Draw a character from something you loved as a child",

    "Redesign a character you used to love",

    "Take a character you dislike and make them cool",

    "Take a character you love and make them ridiculous",


    # ==========================================
    # CHAOS
    # ==========================================

    "Draw something completely ridiculous",

    "Draw the coolest thing you can think of",

    "Draw something you would never normally draw",

    "Draw the most unnecessarily complicated version of something simple",

    "Draw something that looks like it belongs in a game",

    "Draw something that looks like it belongs on an album cover",

    "Draw something that looks like it belongs in a movie",

    "Draw something that looks like it came from a dream",

    "Draw something that looks like it shouldn't work, but somehow does",

    "Draw something that would make absolutely no sense without context",

    "Draw something that you would put on a wall",

    "Draw something you would use as a profile picture",

    "Draw something that would make a terrible tattoo",

    "Draw something you could imagine becoming a recurring character",

    "Draw whatever comes to mind, but make it interesting",

]





async def set_session_state(channel, is_open, owner_id):
    """Set the session channel state while preserving the owner's write access."""
    overwrite = channel.overwrites_for(channel.guild.default_role)
    overwrite.send_messages = is_open
    await channel.set_permissions(channel.guild.default_role, overwrite=overwrite)

    owner = channel.guild.get_member(owner_id)
    if owner is None:
        owner = await channel.guild.fetch_member(owner_id)

    owner_overwrite = channel.overwrites_for(owner)
    owner_overwrite.send_messages = True
    await channel.set_permissions(owner, overwrite=owner_overwrite)


# ==========================================
# BOT READY
# ==========================================

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    print("Art Session Bot is ready!")


# ==========================================
# MESSAGE HANDLER
# ==========================================

@client.event
async def on_message(message):

    # Ignore bots
    if message.author.bot:
        return

    channel_name = message.channel.name


    # ======================================
    # OWNER SESSION CHANNELS
    # ======================================

    if channel_name in CHANNEL_OWNERS:

        owner_id = CHANNEL_OWNERS[channel_name]

        # Only the owner can use !open / !close
        if message.author.id != owner_id:
            return


        # ==================================
        # OPEN
        # ==================================

        if message.content.lower().strip() == "!open":

            try:
                await set_session_state(
                    message.channel,
                    is_open=True,
                    owner_id=owner_id,
                )
            except discord.Forbidden:
                await message.channel.send(
                    "I need the **Manage Channels** permission to open this session."
                )
                return

            await message.channel.send(
                f"🟢 **{message.author.display_name} opened the session.**\n"
                f"Everyone can talk now. Go make some art."
            )


        # ==================================
        # CLOSE
        # ==================================

        elif message.content.lower().strip() == "!close":

            try:
                await set_session_state(
                    message.channel,
                    is_open=False,
                    owner_id=owner_id,
                )
            except discord.Forbidden:
                await message.channel.send(
                    "I need the **Manage Channels** permission to close this session."
                )
                return

            await message.channel.send(
                f"🔴 **{message.author.display_name} closed the session.**\n"
                f"The channel is closed."
            )


    # ======================================
    # BOT INTERACTIONS
    # ======================================
    # Future commands/functions go here.
    # ======================================

    elif channel_name == BOT_INTERACTIONS_CHANNEL:

        command_text = message.content.strip()
        command, _, argument = command_text.partition(" ")
        command = command.lower()
        argument = argument.strip()

        words = re.findall(r"[a-z0-9']+", message.content.lower())
        for word in words:
            if word in WORD_RESPONSES:
                await message.channel.send(WORD_RESPONSES[word])
                return

        if command in ("!help", "!commands"):
            await message.channel.send(
                "**Bot commands**\n"
                "`!roll` or `!roll 20` - Roll a die\n"
                "`!coinflip` - Flip a coin\n"
                "`!8ball your question` - Ask the Magic 8-Ball\n"
                "`!prompt` - Get a random art prompt\n"
                "`!choose red | blue | green` - Let me choose"
            )

        elif command == "!roll":
            try:
                sides = int(argument) if argument else 6
            except ValueError:
                await message.channel.send("Use a whole number of sides, like `!roll 20`.")
                return

            if sides < 2 or sides > 1000:
                await message.channel.send("Choose between 2 and 1000 sides.")
                return

            await message.channel.send(f"🎲 You rolled **{random.randint(1, sides)}** (d{sides}).")

        elif command in ("!coinflip", "!coin"):
            await message.channel.send(f"🪙 **{random.choice(('Heads', 'Tails'))}!**")

        elif command in ("!8ball", "!ask"):
            if not argument:
                await message.channel.send("Ask me something, like `!8ball should I add more color?`.")
                return

            await message.channel.send(f"🔮 **{random.choice(EIGHT_BALL_ANSWERS)}**")

        elif command in ("!prompt", "!artprompt"):
            await message.channel.send(f"🎨 **Art prompt:** {random.choice(ART_PROMPTS)}")

        elif command == "!choose":
            options = [option.strip() for option in argument.split("|") if option.strip()]
            if len(options) < 2:
                await message.channel.send("Give me at least two options, separated by `|`.")
                return

            await message.channel.send(f"🤔 I choose **{random.choice(options)}**.")


client.run(TOKEN)
