#!/usr/bin/env python3
"""
Shower Arguments - The Comeback Generator
For the arguments you should have won
Generates the devastating comeback you thought of 3 hours later
"""

import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Comeback templates by category
COMEBACK_TEMPLATES = {
    "intellectual": [
        "Actually, if you'd read literally any {FIELD} from the last {YEARS} years, you'd know that {POINT}.",
        "That's a fascinating perspective if you ignore {OBVIOUS_THING} and {OTHER_OBVIOUS_THING}.",
        "I find it interesting that you feel confident enough to have an opinion without having done any actual research.",
        "Your argument would be compelling if it weren't contradicted by {EVIDENCE}.",
        "I'm sure that sounded smarter in your head.",
        "That's certainly one interpretation. A wrong one, but an interpretation nonetheless.",
    ],
    "calm_devastating": [
        "I hope your day is as pleasant as you are.",
        "I would explain it to you, but I left my crayons at home.",
        "You're not wrong because you're stupid. You're stupid because you're wrong.",
        "I'd agree with you, but then we'd both be wrong.",
        "Somewhere out there is a tree tirelessly producing oxygen for you. You owe it an apology.",
        "I'm not saying I hate you, but I would unplug your life support to charge my phone.",
        "If I wanted to hear from an ass, I'd fart.",
    ],
    "witty": [
        "I've been called worse things by better people.",
        "I'd call you a tool, but at least tools are useful.",
        "If you were any more wrong, you'd be a politician.",
        "I'm sorry, I don't speak 'confidently incorrect.'",
        "Your opinion is noted. And discarded.",
        "That's a lot of words to say absolutely nothing.",
        "I'll try being nicer when you try being smarter.",
    ],
    "philosophical": [
        "The confidence with which you're wrong is almost admirable.",
        "In another life, you might have been right. But not this one.",
        "You've given me a lot to think about. Mostly about how I ended up in this conversation.",
        "Your capacity for missing the point is genuinely impressive.",
        "I didn't think it was possible to be this wrong, and yet here we are.",
        "The universe is infinite, and somehow you chose to be this.",
    ],
    "professional": [
        "Per the evidence you clearly didn't review...",
        "I appreciate your input, but I'm going to go with what actually works.",
        "I see you've prepared for this conversation as thoroughly as expected.",
        "That's one way to interpret the data. A wrong way, but a way.",
        "I value your perspective, which is why I'm ignoring it.",
        "Let's revisit this when you've caught up with the rest of us.",
    ],
    "exhausted_but_correct": [
        "I'm too tired to explain why you're wrong, but you are.",
        "This isn't the hill I planned to die on, but fine, I'll die on it.",
        "I don't have the energy to unpack all of that, but wow.",
        "You've said a lot of incorrect things, but that one... that one was impressive.",
        "I've explained this three times. I'm not going to explain it a fourth time, but you're still wrong.",
    ],
}

# Filler content for templates
FIELDS = ["psychology", "economics", "literally any science", "history", "common sense", "basic logic"]
YEARS = ["10", "50", "100", "literally all of human"]
OBVIOUS_THINGS = ["basic facts", "reality", "evidence", "how things actually work", "the obvious counterexample", "literally everything else you said"]
EVIDENCE = ["reality", "the facts", "basic observation", "what literally just happened", "your own previous statement"]

# Argument types for context
ARGUMENT_TYPES = {
    "someone was condescending": "intellectual",
    "someone was just mean": "calm_devastating",
    "someone made a dumb point": "witty",
    "someone was confidently wrong": "philosophical",
    "work disagreement": "professional",
    "i was right but couldn't articulate it": "exhausted_but_correct",
}

# Additional modifiers
OPENERS = [
    "You know what?",
    "Here's the thing:",
    "Let me be clear:",
    "With respect,",
    "Look,",
    "",
    "",
    "",  # Empty strings for variety
]

CLOSERS = [
    "But you know that, don't you?",
    "And deep down, you know that.",
    "Have a great day.",
    "We're done here.",
    "Just something to think about.",
    "*walks away*",
    "",
    "",
    "",
]


def fill_template(template):
    """Fill in a template with random content."""
    result = template
    if "{FIELD}" in result:
        result = result.replace("{FIELD}", random.choice(FIELDS))
    if "{YEARS}" in result:
        result = result.replace("{YEARS}", random.choice(YEARS))
    if "{OBVIOUS_THING}" in result:
        result = result.replace("{OBVIOUS_THING}", random.choice(OBVIOUS_THINGS))
    if "{OTHER_OBVIOUS_THING}" in result:
        result = result.replace("{OTHER_OBVIOUS_THING}", random.choice(OBVIOUS_THINGS))
    if "{EVIDENCE}" in result:
        result = result.replace("{EVIDENCE}", random.choice(EVIDENCE))
    if "{POINT}" in result:
        result = result.replace("{POINT}", "your entire premise is flawed")
    return result


def generate_comebacks(situation, context=""):
    """Generate comebacks for a situation."""
    # Determine category
    category = None
    situation_lower = situation.lower()

    for trigger, cat in ARGUMENT_TYPES.items():
        if any(word in situation_lower for word in trigger.split()):
            category = cat
            break

    if not category:
        category = random.choice(list(COMEBACK_TEMPLATES.keys()))

    # Generate 3 comebacks
    templates = COMEBACK_TEMPLATES[category]
    comebacks = []

    for _ in range(3):
        template = random.choice(templates)
        comeback = fill_template(template)

        opener = random.choice(OPENERS)
        closer = random.choice(CLOSERS)

        full_comeback = " ".join(filter(None, [opener, comeback, closer]))
        comebacks.append(full_comeback)

    return {
        "category": category.replace("_", " ").title(),
        "comebacks": comebacks,
        "bonus_advice": random.choice([
            "Deliver this with a calm, slightly disappointed tone for maximum effect.",
            "The key is to say this and then immediately change the subject.",
            "Maintain eye contact. Don't blink. They'll blink first.",
            "Say this, then take a sip of your drink like you're in a movie.",
            "The power move is to say this and then walk away before they respond.",
            "Practice in the mirror. You've got this.",
        ]),
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    situation = data.get("situation", "")
    context = data.get("context", "")

    if not situation.strip():
        return jsonify({"error": "Describe your situation"}), 400

    result = generate_comebacks(situation, context)
    return jsonify(result)


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  Shower Arguments")
    print("=" * 50)
    print("\n  Generating comebacks at: http://localhost:5013")
    print("  Press Ctrl+C to stop\n")
    app.run(debug=True, port=5013)
