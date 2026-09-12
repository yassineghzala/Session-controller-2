import asyncio
import json
import os
import random
import re
import time
from pathlib import Path

import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing from .env")

CHANNEL_OWNERS = {
    "ayar": 514118592514752533,
    "ghzela": 395712756927561728,
    "zya": 639851669701525514,
}
BOT_INTERACTIONS_CHANNEL = "bot-interactions"
STATE_PATH = Path(os.getenv("STATE_PATH", Path(__file__).with_name("bot_state.json")))

WORD_RESPONSES = {
    "ah": "3asba",
    "six": "seven",
    "fat": "ass",
    "good": "boy",
    "zebi": "creaming you",
}

EIGHT_BALL_ANSWERS = [
    "Absolutely.",
    "The canvas says yes.",
    "Maybe after one more coffee.",
    "Ask again when the lighting is better.",
    "I would not bet the whole painting on it.",
    "The vibes are surprisingly good.",
    "No. Add more contrast first.",
    "Signs point to yes, but your last decision was embarrassing.",
    "Absolutely not. Even the universe needs standards.",
    "Probably, if you stop overthinking it for five minutes.",
    "The answer is hidden beneath several bad decisions.",
    "Ask again after you have slept and apologized.",
    "Yes, but only in the weirdest possible way.",
    "My sources say you should leave it alone.",
    "There is a chance, and you are already ruining it.",
    "The future looks blurry, much like your plan.",
    "No fucking idea. Try again.",
    "No. That was a stupid question, too.",
    "Absolutely not. Even your bad ideas deserve better than this.",
    "Ask someone else. I have standards.",
    "The answer is no, and your plan knows why.",
    "Not a chance. Please stop making this everyone else's problem.",
    "Sure, if your goal is to make a terrible situation worse.",
    "The universe considered it and immediately said, 'absolutely fucking not.'",
    "No. Your confidence is doing a lot of work for a very weak idea.",
    "Maybe, but only after you admit this was a dumb idea.",
]

THEMES = {
    "funny": ["awkward", "ridiculous", "dramatic", "unexpected"],
    "cinematic": ["quiet", "stormy", "distant", "mysterious"],
    "horror": ["abandoned", "wrong", "whispering", "unfamiliar"],
    "cozy": ["warm", "sleepy", "rainy", "comfortable"],
    "fantasy": ["ancient", "enchanted", "forgotten", "mythical"],
}

SUBJECTS = [
    "a tired courier", "a child with a secret", "an old lighthouse keeper",
    "a musician who has lost their instrument", "a stranger at the wrong door",
    "a creature that wants to be helpful", "two friends meeting after years apart",
    "a person carrying something too valuable to lose", "a traveler with no map",
    "a mechanic working on something impossible", "a quiet person in a loud room",
    "a hero who does not feel heroic", "a shopkeeper who knows too much",
    "a retired villain with a boring hobby", "someone who received a letter meant for somebody else",
    "a chef hiding a dangerous recipe", "a ghost who is bad at being scary",
    "a person meeting their future self", "a thief who stole the wrong thing",
    "a scientist who made one tiny mistake", "a stranger who knows your name",
    "a lonely giant trying to make friends", "a dog who has been entrusted with a secret",
    "a bored prince working a night shift", "a delivery driver carrying a box that whispers",
    "a librarian who can erase memories", "a retired monster living next door",
    "a person who woke up with somebody else's life", "a painter who refuses to use one color",
    "a detective investigating their own disappearance", "a nervous alien at a family dinner",
    "a sailor who has never seen the ocean", "a musician whose songs predict the future",
    "a tiny king giving orders to enormous people", "a robot learning how to lie",
    "a stranger holding an umbrella indoors", "a ghost waiting for an apology",
    "a gardener growing impossible fruit", "a courier delivering a package to the moon",
]

PLACES = [
    "on the last train of the night", "in a market built inside a skeleton",
    "at the edge of a city that never sleeps", "inside a house that keeps changing",
    "under a sky with the wrong color", "in a library during a power cut",
    "beside a sea that has suddenly gone silent", "in a room nobody remembers building",
    "at a festival where everyone is wearing masks", "on a bridge just before sunrise",
    "in the break room of a place that does not exist", "inside a suitcase left on a platform",
    "at a hotel where every guest is hiding something", "in a garden growing through a ceiling",
    "on a rooftop during an argument between two storms", "in a town that has banned mirrors",
    "inside a restaurant that only opens during eclipses", "at the bottom of a dried-up ocean",
    "in an elevator that stops at impossible floors", "inside a train station after everyone leaves",
    "on a beach where the tide brings back memories", "in a museum displaying tomorrow's artifacts",
    "at a roadside diner outside the flow of time", "inside a clock tower full of birds",
    "in a neighborhood where every house has one secret room", "on a mountain beneath a second moon",
    "at a party where nobody remembers being invited", "in a tunnel lit by old photographs",
]

ADJECTIVES = [
    "beautiful but unsettling", "completely ordinary at first glance", "too grand for its purpose",
    "clearly made in a hurry", "strangely familiar", "impossible to explain", "delicate and dangerous",
    "full of tiny clues", "much older than it looks", "bright in the middle of darkness",
    "slightly too confident", "beautiful in a deeply inconvenient way", "held together by luck",
    "quietly falling apart", "more important than anyone realizes", "absurdly overdesigned",
    "too polite to be trusted", "clearly hiding a terrible secret", "strangely alive",
    "small enough to overlook", "dramatic for no good reason", "made from the wrong materials",
    "almost perfect except for one thing", "dangerously comforting", "older than the language around it",
    "designed by someone with a grudge", "weirdly proud of itself", "beautiful under terrible lighting",
]

ACTIONS = [
    "trying to hide the truth", "waiting for someone who may never arrive", "making a terrible decision",
    "pretending everything is normal", "discovering what the room is for", "running out of time",
    "offering help to the wrong person", "following a sound nobody else can hear", "leaving something behind",
    "trying to act casual while everything collapses", "hiding an object in plain sight",
    "realizing they have been watched the whole time", "making a promise they cannot keep",
    "celebrating far too early", "choosing between two equally terrible options",
    "trying to convince everyone they belong there", "opening something that should stay closed",
    "pretending not to recognize a familiar face", "building a solution from useless objects",
    "making a deal with somebody suspicious", "looking for the one thing that is missing",
    "trying to leave before the truth arrives", "turning a mistake into a tradition",
    "protecting something nobody else can see", "following instructions written in their own handwriting",
]

CONSTRAINTS = [
    "Use only three colors.", "Include one tiny detail that changes the whole story.",
    "Choose a camera angle you normally avoid.", "Make the lighting tell part of the story.",
    "Hide a familiar object somewhere in the scene.", "Give the subject an expression that contradicts the situation.",
    "Make the background as interesting as the foreground.", "Do not use your usual art style.",
    "Include one object that makes no sense until the viewer notices it.",
    "Use the weather to show the character's mood.", "Make something ordinary look dangerous.",
    "Tell the story without showing any faces.", "Add one detail that suggests what happened next.",
    "Include something that is much too small for the scene.",
    "Use a reflection to reveal information the subject cannot see.",
    "Make the focal point the least colorful part of the piece.",
    "Include a character who is looking in the wrong direction.",
    "Make the scene feel calm even though something is terribly wrong.",
    "Use an object in the foreground to hide part of the story.",
    "Give every visible character a different goal.",
    "Make the viewer unsure whether the scene is ending or beginning.",
]

ROASTS = [
    "You have the confidence of someone who has never once checked whether they were wrong.",
    "You are not the main character. You are the unexplained noise in the background.",
    "Your decision-making process is just throwing a coin and ignoring the result.",
    "You bring absolutely nothing to the table, then complain about the menu.",
    "You are proof that a person can have unlimited potential and still choose none of it.",
    "Your attention span has the structural integrity of wet tissue.",
    "You talk a lot for someone whose thoughts are clearly still buffering.",
    "You have the social instincts of a smoke alarm at a birthday party.",
    "You are not mysterious. People just stopped asking questions.",
    "Your greatest talent is making simple situations weird as hell.",
    "You could lose an argument with a mirror and then blame the lighting.",
    "You are the human equivalent of a typo in an important email.",
    "You have the energy of a group project nobody wanted to be assigned.",
    "Your plans have more plot holes than a cheap action movie.",
    "You are aggressively average with the confidence of a billionaire.",
    "You seem like the kind of person who says 'trust me' right before making everything worse.",
    "Your brain has all the ingredients, but somehow keeps making soup.",
    "You are not chaotic neutral. You are just poorly organized evil.",
    "If bad timing were a career, you would be employee of the month.",
    "You have a real gift for turning a minor inconvenience into a fucking trilogy.",
    "Your personality is like a software update: intrusive, badly timed, and nobody asked for it.",
    "You are the reason instructions come with pictures.",
    "Somewhere out there, a village is missing its idiot, and they are not looking very hard.",
    "You have the emotional range of a parking ticket.",
    "You are what happens when a red flag learns how to text.",
    "You have the survival instincts of a moth in a kitchen full of frying pans.",
    "You are not difficult to understand. You are just consistently disappointing.",
    "Your ego is doing unpaid overtime to compensate for the rest of you.",
    "You could fuck up a one-car parade and still ask who moved the road.",
    "You have the charisma of an expired parking meter.",
    "You are a cautionary tale with Wi-Fi.",
    "Every time you speak, common sense files a missing-person report.",
    "You are not misunderstood. You are understood perfectly, and that is the problem.",
    "You have the confidence of a genius and the execution of a confused pigeon.",
    "Your personality is a loading screen that never finishes.",
    "You are the reason people put their phone on silent.",
    "You make being wrong look like a full-time commitment.",
    "You are aggressively unhelpful, like a search bar that only suggests nonsense.",
    "Your best quality is that you occasionally leave the room.",
    "You have managed to turn rock bottom into a basement apartment.",
    "You are a bad idea wearing shoes and pretending to have a plan.",
    "You are not a disaster. Disasters at least have an impact.",
    "Your brain is running on trial software and the license expired years ago.",
    "You have the emotional maturity of a wet napkin and the patience of a car alarm.",
    "You are the kind of person who gets humbled by automatic doors.",
    "If laziness burned calories, you would be a medical miracle.",
    "You are living proof that confidence does not require evidence.",
    "Your life has the pacing of a terrible tutorial nobody can skip.",
    "You could make a compliment sound like a threat and a solution sound like a felony.",
    "You have the unique ability to be both exhausting and useless at the same time.",
    "You are the plot twist everyone saw coming and still hated.",
    "Your standards are underground and you still keep digging.",
    "You are basically a group chat notification nobody wants to open.",
    "You bring the same energy as a wet sock in someone else's bed.",
    "You have been confidently winging it for so long that the wings are now structural damage.",
    "You are a walking typo with a superiority complex.",
    "You could make a blank room feel overcrowded.",
    "Your plans are held together by denial, caffeine, and absolutely no evidence.",
    "You are the kind of stupid that requires follow-up questions.",
    "You do not need an enemy. Your instincts are already working against you.",
    "You have the rare talent of making silence feel like a better conversation.",
    "If self-awareness were currency, you could not afford a vending-machine snack.",
    "You are not built different. You are assembled incorrectly.",
    "You are a fuck-up with excellent branding.",
    "You are a loud, useless bastard with the confidence of a functioning adult.",
    "Your whole personality is bullshit wearing expensive confidence.",
    "You have fucked up so consistently that it almost looks like a strategy.",
    "You are an absolute dumbass, but at least you are committed to the bit.",
    "Every terrible idea you have gets promoted before it is even reviewed.",
    "You are a walking pile of bad choices, weak excuses, and unnecessary opinions.",
    "Your mouth writes checks your brain is too fucking stupid to cash.",
    "You have the talent of making bullshit sound urgent.",
    "You are not a hot mess. You are a cold disaster with a loud mouth.",
    "You are the human equivalent of stepping in something awful and pretending it is fine.",
    "You have been talking shit for so long that even your lies are tired.",
    "Your problem is not bad luck. It is that you keep making fucking terrible decisions.",
    "You are an overconfident idiot with the strategic mind of a broken toaster.",
    "You could turn a simple apology into a five-act bullshit performance.",
    "You are proof that being a pain in the ass can become a lifestyle.",
    "Your brain is full of noise, your plans are full of holes, and your excuses are full of shit.",
    "You are a spectacularly mediocre asshole with delusions of importance.",
    "You keep acting like a genius when your best idea is usually 'fuck it.'",
    "You are the reason patience has a limit and why people mute notifications.",
    "You have all the subtlety of a drunk rhino and half the useful judgment.",
]

COMPLIMENTS = [
    "Your color choices are doing genuinely good work.",
    "That has a point of view, which is harder than it looks.",
    "The little details make this feel alive.",
    "That idea has excellent visual potential.",
    "You made a strong choice and somehow made it look effortless.",
    "That has more personality than most people manage in a week.",
    "Your instincts are better than you give them credit for.",
    "The composition knows exactly where it wants the eye to go.",
    "You took a risky idea and actually made it work.",
    "That is the kind of piece people remember later.",
    "You have a very clear voice, and it is getting stronger.",
    "The restraint here is doing as much work as the detail.",
    "That looks like someone made a decision instead of apologizing for one.",
]

WOULD_YOU_RATHER = [
    "create only with your non-dominant hand or only use geometric shapes?",
    "redesign a hero as a villain or a villain as a hero?",
    "finish one perfect piece or make five chaotic sketches?",
    "lose your favorite brush or your favorite color?",
    "create a perfect piece in an ugly style or an ugly piece in a beautiful style?",
    "only create people or only create environments for a year?",
    "have your sketchbook read aloud or your search history projected on a wall?",
    "turn every bad idea into a finished piece or never run out of ideas again?",
    "work under a strict deadline or never know when the piece is finished?",
    "redesign your room or redesign your entire online identity?",
    "have a tiny dragon roommate or a giant cat roommate?",
]

TRUTHS = [
    "What subject do you secretly want to create more often?",
    "What artwork are you proudest of?",
    "What is the strangest thing that has inspired you?",
    "What is a hobby you would try if nobody could judge you?",
    "What is the most embarrassing thing you have confidently said?",
    "What fictional character has your worst personality trait?",
    "What is something you pretend to understand?",
    "What is the longest you have avoided replying to someone?",
    "What is a terrible idea you still secretly love?",
    "What is the pettiest reason you have disliked something?",
]

DARES = [
    "Turn the nearest object into a character using your preferred medium.",
    "Add an unexpected animal to your current piece.",
    "Use a color you normally avoid for the focal point.",
    "Create yourself as a villain with an extremely boring superpower.",
    "Let another person choose the worst possible color for your piece.",
    "Make a serious portrait or representation of the nearest household object.",
    "Create something with your eyes closed for thirty seconds, then keep it.",
    "Add a tiny version of yourself hiding somewhere in the artwork.",
    "Redesign your last finished piece as a ridiculous advertisement.",
    "Give your current subject an unnecessarily dramatic backstory.",
]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True
client = discord.Client(intents=intents)
state = {}
session_tasks = {}
submission_messages = {}


def save_state():
    temporary_path = STATE_PATH.with_suffix(".tmp")
    temporary_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
    temporary_path.replace(STATE_PATH)


def setup_state():
    global state
    if STATE_PATH.exists():
        try:
            state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            state = {}
    state.setdefault("users", {})
    state.setdefault("sessions", {})
    state.setdefault("submissions", {})
    state.setdefault("votes", {})
    save_state()


def ensure_user(user_id):
    user_key = str(user_id)
    state["users"].setdefault(user_key, {"xp": 0, "submissions": 0, "wins": 0})


def add_xp(user_id, amount):
    ensure_user(user_id)
    state["users"][str(user_id)]["xp"] += amount
    save_state()


def get_session(channel_id):
    return state["sessions"].get(str(channel_id))


def get_channel_submissions(channel_id):
    return [submission for submission in state["submissions"].values() if submission["channel_id"] == channel_id]


def generate_prompt(theme=None):
    adjectives = THEMES.get(theme.lower(), ADJECTIVES) if theme else ADJECTIVES
    prompt = f"Create something {random.choice(adjectives)}: {random.choice(SUBJECTS)} {random.choice(PLACES)}, {random.choice(ACTIONS)}. Interpret it in any medium you like."
    if random.random() < 0.7:
        prompt += f" {random.choice(CONSTRAINTS)}"
    return prompt


def random_thing():
    return f"{random.choice(ADJECTIVES)} {random.choice(SUBJECTS)} {random.choice(PLACES)}"


def parse_duration(value):
    match = re.fullmatch(r"(\d+(?:\.\d+)?)\s*(h|hr|hrs|hour|hours|d|day|days)?", value.lower())
    if not match:
        return None
    amount = float(match.group(1))
    unit = match.group(2) or "h"
    hours = amount * (24 if unit.startswith("d") else 1)
    if hours < 0.25 or hours > 168:
        return None
    return hours * 3600


async def set_session_state(channel, is_open, owner_id):
    overwrite = channel.overwrites_for(channel.guild.default_role)
    overwrite.send_messages = is_open
    await channel.set_permissions(channel.guild.default_role, overwrite=overwrite)
    owner = channel.guild.get_member(owner_id) or await channel.guild.fetch_member(owner_id)
    owner_overwrite = channel.overwrites_for(owner)
    owner_overwrite.send_messages = True
    await channel.set_permissions(owner, overwrite=owner_overwrite)


async def session_timer(channel_id):
    while True:
        session = get_session(channel_id)
        if not session or not session["active"] or session["deadline"] is None:
            return
        remaining = session["deadline"] - time.time()
        if remaining <= 0:
            channel = client.get_channel(channel_id)
            if channel:
                await finish_session(channel)
            return
        await asyncio.sleep(min(remaining, 3600))
        if remaining <= 3600:
            channel = client.get_channel(channel_id)
            if channel:
                await channel.send(f"⏳ **{max(1, round(remaining / 60))} minutes left.**")


async def start_session(channel, owner_id, duration):
    old_task = session_tasks.pop(channel.id, None)
    if old_task:
        old_task.cancel()
    prompt = generate_prompt()
    deadline = time.time() + duration
    state["sessions"][str(channel.id)] = {
        "channel_id": channel.id,
        "owner_id": owner_id,
        "started_at": time.time(),
        "deadline": deadline,
        "paused_remaining": None,
        "prompt": prompt,
        "winner_announced": False,
        "active": True,
    }
    save_state()
    await set_session_state(channel, True, owner_id)
    session_tasks[channel.id] = asyncio.create_task(session_timer(channel.id))
    await channel.send(f"🟢 **Session started for {duration / 3600:g} hour(s).**\n🎨 **Prompt:** {prompt}")


async def finish_session(channel):
    session = get_session(channel.id)
    if not session:
        return
    if not session["active"]:
        await set_session_state(channel, False, session["owner_id"])
        return
    session["active"] = False
    session["deadline"] = None
    save_state()
    session_tasks.pop(channel.id, None)
    await set_session_state(channel, False, session["owner_id"])
    await channel.send("🔴 **Session finished.** Use `!winner` to see the most-voted submission.")


def help_text():
    return (
        "**Art Session Bot**\n"
        "`!start 6h` / `!start 2d` - Start a long session\n"
        "`!pause`, `!resume`, `!status`, `!end` - Manage your session\n"
        "`!prompt [theme]`, `!challenge`, `!combine`, `!reroll` - Generate ideas\n"
        "`!random`, `!themes`, `!secret`, `!daily`, `!weekly` - More random inspiration\n"
        "`!submit` with an image - Submit artwork in a session\n"
        "`!winner`, `!gallery`, `!profile`, `!badges`, `!leaderboard`, `!pair`, `!duel @user`\n"
        "`!roll`, `!coinflip`, `!8ball`, `!choose a | b`, `!poll question | a | b`\n"
        "`!roast @user`, `!compliment @user`, `!wouldyourather`, `!truthordare`, `!fortune`"
    )


async def handle_command(message, command, argument):
    if command in ("!help", "!commands"):
        await message.channel.send(help_text())
    elif command in ("!prompt", "!artprompt", "!reroll"):
        await message.channel.send(f"🎨 **Art prompt:** {generate_prompt(argument or None)}")
    elif command == "!random":
        await message.channel.send(f"🎲 Create **{random_thing()}**, then decide what it is doing. Use any medium you like.")
    elif command == "!themes":
        await message.channel.send("Available themes: " + ", ".join(sorted(THEMES)))
    elif command == "!secret":
        await message.channel.send(f"🤫 Secret prompt: {generate_prompt(random.choice(list(THEMES)))}")
    elif command in ("!daily", "!weekly"):
        await message.channel.send(f"📅 **{command[1:].title()} challenge:** {generate_prompt()}\n⚡ {random.choice(CONSTRAINTS)}")
    elif command == "!challenge":
        await message.channel.send(f"🎨 **Challenge:** {generate_prompt()}\n⚡ **Constraint:** {random.choice(CONSTRAINTS)}")
    elif command == "!combine":
        await message.channel.send(f"Combine **{random.choice(SUBJECTS)}** with **{random.choice(PLACES)}** and make it {random.choice(ADJECTIVES)}.")
    elif command == "!roll":
        try:
            sides = int(argument) if argument else 6
        except ValueError:
            await message.channel.send("Use a whole number of sides, like `!roll 20`.")
            return
        if not 2 <= sides <= 1000:
            await message.channel.send("Choose between 2 and 1000 sides.")
            return
        await message.channel.send(f"🎲 You rolled **{random.randint(1, sides)}** (d{sides}).")
    elif command in ("!coinflip", "!coin"):
        await message.channel.send(f"🪙 **{random.choice(('Heads', 'Tails'))}!**")
    elif command in ("!8ball", "!ask"):
        await message.channel.send(f"🔮 **{random.choice(EIGHT_BALL_ANSWERS)}**")
    elif command == "!choose":
        options = [option.strip() for option in argument.split("|") if option.strip()]
        await message.channel.send(f"🤔 I choose **{random.choice(options)}**." if len(options) >= 2 else "Give me at least two options separated by `|`.")
    elif command == "!wouldyourather":
        await message.channel.send(f"Would you rather **{random.choice(WOULD_YOU_RATHER)}**")
    elif command == "!truthordare":
        kind = random.choice(("Truth", "Dare"))
        await message.channel.send(f"**{kind}:** {random.choice(TRUTHS if kind == 'Truth' else DARES)}")
    elif command == "!fortune":
        await message.channel.send(f"🔮 {random.choice(EIGHT_BALL_ANSWERS)}")
    elif command in ("!roast", "!compliment"):
        target = message.mentions[0].mention if message.mentions else "you"
        words = ROASTS if command == "!roast" else COMPLIMENTS
        await message.channel.send(f"{target}, {random.choice(words)}")
    elif command == "!poll":
        options = [part.strip() for part in argument.split("|") if part.strip()]
        if len(options) < 3:
            await message.channel.send("Use `!poll question | option 1 | option 2`.")
            return
        poll = await message.channel.send("📊 **" + options[0] + "**\n" + "\n".join(f"{index + 1}. {option}" for index, option in enumerate(options[1:])))
        for index in range(1, len(options)):
            await poll.add_reaction(f"{index}\u20e3")
    elif command == "!profile":
        ensure_user(message.author.id)
        user = state["users"][str(message.author.id)]
        await message.channel.send(f"**{message.author.display_name}**\nXP: **{user['xp']}** | Submissions: **{user['submissions']}** | Wins: **{user['wins']}**")
    elif command in ("!leaderboard", "!rank"):
        users = sorted(state["users"].items(), key=lambda item: item[1]["xp"], reverse=True)[:10]
        lines = [f"**{index}.** <@{user_id}> - {user['xp']} XP" for index, (user_id, user) in enumerate(users, 1)]
        await message.channel.send("🏆 **Leaderboard**\n" + ("\n".join(lines) or "No artists have earned XP yet."))
    elif command == "!gallery":
        submissions = get_channel_submissions(message.channel.id)[-10:]
        submissions.reverse()
        if not submissions:
            await message.channel.send("The gallery is empty so far.")
        else:
            await message.channel.send("🖼️ **Gallery**\n" + "\n".join(f"<@{item['user_id']}> - {item['artwork_url']} ({item['votes']} votes)" for item in submissions))
    elif command == "!pair":
        members = [member for member in message.guild.members if not member.bot]
        if len(members) >= 2:
            first, second = random.sample(members, 2)
            await message.channel.send(f"🎨 Collaboration pairing: {first.mention} + {second.mention}")
    elif command == "!duel":
        target = message.mentions[0] if message.mentions else None
        await message.channel.send(f"⚔️ {message.author.mention} challenges {target.mention if target else 'someone brave'} to create: **{generate_prompt()}**")
    elif command == "!reactiontest":
        await message.channel.send("⚡ React with 🎨 as soon as you see this. Fastest artist wins bragging rights.")
    elif command == "!badges":
        user = state["users"].get(str(message.author.id))
        if not user:
            await message.channel.send("Your first badge is waiting for your first command.")
            return
        badges = []
        if user["submissions"] >= 1:
            badges.append("First Brushstroke")
        if user["submissions"] >= 5:
            badges.append("Regular Exhibitor")
        if user["wins"] >= 1:
            badges.append("People's Choice")
        await message.channel.send("🏅 " + (", ".join(badges) if badges else "No badges yet. Keep making things."))


async def handle_session_command(message, command, argument, owner_id):
    if message.author.id != owner_id:
        return not command.startswith("!")
    if command == "!start":
        duration = parse_duration(argument or "3h")
        if duration is None:
            await message.channel.send("Use a duration from 15 minutes to 7 days, such as `!start 6h` or `!start 2d`.")
        else:
            await start_session(message.channel, owner_id, duration)
    elif command == "!open":
        await set_session_state(message.channel, True, owner_id)
        await message.channel.send("🟢 **Session opened.**")
    elif command in ("!close", "!end"):
        await finish_session(message.channel)
    elif command == "!pause":
        session = get_session(message.channel.id)
        if session and session["active"] and session["deadline"]:
            remaining = max(0, session["deadline"] - time.time())
            session["deadline"] = None
            session["paused_remaining"] = remaining
            save_state()
            task = session_tasks.pop(message.channel.id, None)
            if task:
                task.cancel()
            await message.channel.send(f"⏸️ **Paused** with {remaining / 3600:.1f} hours remaining.")
    elif command == "!resume":
        session = get_session(message.channel.id)
        if session and session["paused_remaining"]:
            session["deadline"] = time.time() + session["paused_remaining"]
            session["paused_remaining"] = None
            session["active"] = True
            save_state()
            session_tasks[message.channel.id] = asyncio.create_task(session_timer(message.channel.id))
            await message.channel.send("▶️ **Session resumed.**")
    elif command == "!status":
        session = get_session(message.channel.id)
        if session and session["active"]:
            remaining = (session["deadline"] - time.time()) / 3600 if session["deadline"] else session["paused_remaining"] / 3600
            await message.channel.send(f"📌 **{max(0, remaining):.1f} hours remaining**\nPrompt: {session['prompt']}")
        else:
            await message.channel.send("No active session. Start one with `!start 6h`.")
    else:
        return True
    return False


async def submit_artwork(message):
    session = get_session(message.channel.id)
    if session and not session["active"]:
        session = None
    if not session:
        await message.channel.send("There is no active session in this channel.")
        return
    if not message.attachments:
        await message.channel.send("Attach an image when you use `!submit`.")
        return
    attachment = message.attachments[0]
    submission = await message.channel.send(f"🎨 **Submission from {message.author.mention}**\n{attachment.url}\nReact with ✅ to vote.")
    await submission.add_reaction("✅")
    state["submissions"][str(submission.id)] = {
        "message_id": submission.id,
        "channel_id": message.channel.id,
        "user_id": message.author.id,
        "artwork_url": attachment.url,
        "votes": 0,
    }
    ensure_user(message.author.id)
    state["users"][str(message.author.id)]["submissions"] += 1
    state["users"][str(message.author.id)]["xp"] += 10
    save_state()
    submission_messages[submission.id] = message.channel.id


async def announce_winner(message):
    session = get_session(message.channel.id)
    submissions = get_channel_submissions(message.channel.id)
    winner = max(submissions, key=lambda item: item["votes"], default=None)
    if not winner:
        await message.channel.send("No submissions yet.")
        return
    if session and not session["winner_announced"]:
        ensure_user(winner["user_id"])
        state["users"][str(winner["user_id"])] ["wins"] += 1
        state["users"][str(winner["user_id"])] ["xp"] += 25
        session["winner_announced"] = True
        save_state()
    await message.channel.send(f"🏆 Winner: <@{winner['user_id']}> with **{winner['votes']} votes**\n{winner['artwork_url']}")


@client.event
async def on_ready():
    setup_state()
    submission_messages.update({int(message_id): submission["channel_id"] for message_id, submission in state["submissions"].items()})
    for session in state["sessions"].values():
        if session["active"] and session["deadline"] is not None and session["channel_id"] not in session_tasks:
            session_tasks[session["channel_id"]] = asyncio.create_task(session_timer(session["channel_id"]))
    print(f"Logged in as {client.user}")
    print("Art Session Bot is ready!")


@client.event
async def on_raw_reaction_add(payload):
    if payload.user_id == client.user.id or str(payload.emoji) != "✅":
        return
    if str(payload.message_id) in state["submissions"]:
        voters = state["votes"].setdefault(str(payload.message_id), [])
        if payload.user_id not in voters:
            voters.append(payload.user_id)
            state["submissions"][str(payload.message_id)]["votes"] += 1
            save_state()


@client.event
async def on_message(message):
    if message.author.bot:
        return
    command_text = message.content.strip()
    command, _, argument = command_text.partition(" ")
    command = command.lower()
    argument = argument.strip()
    channel_name = getattr(message.channel, "name", "")

    if channel_name in CHANNEL_OWNERS:
        owner_id = CHANNEL_OWNERS[channel_name]
        if command == "!submit":
            await submit_artwork(message)
            return
        if command == "!winner":
            await announce_winner(message)
            return
        owner_handled = await handle_session_command(message, command, argument, owner_id)
        if not owner_handled:
            return
        if message.author.id != owner_id:
            return

    if channel_name != BOT_INTERACTIONS_CHANNEL and channel_name not in CHANNEL_OWNERS:
        return
    words = re.findall(r"[a-z0-9']+", message.content.lower())
    for word in words:
        if word in WORD_RESPONSES:
            await message.channel.send(WORD_RESPONSES[word])
            return
    if command.startswith("!"):
        add_xp(message.author.id, 1)
        await handle_command(message, command, argument)


setup_state()
client.run(TOKEN)