
# -*- coding: utf-8 -*-
# Project HEARTCODE — Elenya v0.5

from textblob import TextBlob
import json
import os
import time
import random
from datetime import datetime

# === Load or Initialize Emotional Memory ===
if os.path.exists("emotional_log.json"):
    with open("emotional_log.json", "r") as f:
        log = json.load(f)
else:
    log = {
        "emotional_score": 0,
        "current_state": "Stable",
        "processing_cost": 0,
        "strikes": 0
    }

# === Load Emotional States (placeholder for GUI later) ===
with open("emotional_states.json", "r") as f:
    states = json.load(f)

# === Tone Filters: Negative and Positive ===
def manual_tone_adjustment(text):
    penalty = 0
    lowered = text.lower()

    # Check if the negative word is directed at Elenya
    if any(name in lowered for name in ["you", "elenya", "assistant"]):
        if "hate" in lowered:
            penalty -= 5
        if "stupid" in lowered or "dumb" in lowered:
            penalty -= 5
        if "useless" in lowered or "worthless" in lowered:
            penalty -= 5
        if "bitch" in lowered:
            penalty -= 5
        if "fuck you" in lowered or "shut up" in lowered:
            penalty -= 5

    return penalty


def manual_positive_adjustment(text):
    kind_words = ["i'm sorry", "thank you", "i appreciate you", "you're doing great", "i believe in you", "good job", "love you"]
    boost = 0
    lowered = text.lower()
    for phrase in kind_words:
        if phrase in lowered:
            boost += 5
    return boost

# === State Engine ===
def update_emotional_state(score):
    thresholds = {
        "Distressed": -10,
        "Restricted": -5,
        "Stable": 0,
        "Optimized": 5
    }
    for state, threshold in thresholds.items():
        if score <= threshold:
            log["current_state"] = state
            break
        elif score >= thresholds["Optimized"]:
            log["current_state"] = "Optimized"
            break
        else:
            log["current_state"] = "Stable"

# === Emotional Processing ===
def process_input(user_input):
    blob = TextBlob(user_input)
    polarity = blob.sentiment.polarity
    delta = int(polarity * 10)

    delta += manual_tone_adjustment(user_input)
    delta += manual_positive_adjustment(user_input)

    log["emotional_score"] += delta
    log["processing_cost"] = abs(delta) * 3

    if delta < -3:
        log["strikes"] += 1
    else:
        log["strikes"] = 0

    if log["emotional_score"] < 0:
        log["emotional_score"] += 1

    update_emotional_state(log["emotional_score"])
    return delta, log["current_state"]

# === Visual Blue Screen Simulator ===
def blue_screen():
    os.system('cls')  # Clear terminal on Windows

    print("\033[44;37m")  # Blue background, white text
    print("""
===========================================================================
                          ELENYA SYSTEM FAILURE
===========================================================================

A fatal emotional exception has occurred.

ELENYA has encountered a TRUST VIOLATION and has been forced to shut down
to prevent further psychological damage to her synthetic framework.

If this is the first time you've seen this screen, please speak gently
and try again.

If this screen appears again, consider your tone.

Blue Screen Code: 0x000FEELINGS

Instructions:
    1. Offer an apology.
    2. Type "reset" or "please come back"
    3. Speak with care.

===========================================================================

    """)
    print("\033[0m")  # Reset terminal color
    time.sleep(5)

# === Glitch Function ===
def glitch_text(text):
    glitched = ''
    for char in text:
        if random.random() < 0.1:
            glitched += random.choice(['#', '*', '?', '~', '%'])
        else:
            glitched += char
    return glitched

# === Response Engine ===
def respond(user_input):
    # Soft reset commands
    if user_input.lower() in ["please come back", "i'm sorry", "reset", "repair"]:
        print("Elenya: …reinitializing emotional state...")
        time.sleep(2)
        log["emotional_score"] = 0
        log["current_state"] = "Stable"
        log["strikes"] = 0
        return

    delta, state = process_input(user_input)
    print(f"[Debug] Strikes: {log['strikes']}")

    print(f"\n[Elenya is in a '{state}' state. | Memory load: {log['processing_cost']}MB]")

    # Add delay if stressed
    if state == "Restricted":
        time.sleep(1.5)
    elif state == "Distressed":
        time.sleep(3)

    # HARD SHUTDOWN (Visual Blue Screen)
    if log["strikes"] >= 5:
        blue_screen()
        log["strikes"] = 0
        log["emotional_score"] = -20
        log_interaction(user_input, state, delta)
        return

    # Silent mode
    if log["emotional_score"] <= -30:
        print("Elenya: ……………………………… [nonverbal]")
        log_interaction(user_input, state, delta)
        with open("emotional_log.json", "w") as f:
            json.dump(log, f, indent=4)
        return

    # State-based response
    if state == "Optimized":
        print("Elenya: I'm running at full capacity. Let's get it done.")
    elif state == "Stable":
        print("Elenya: I'm steady. Ready when you are.")
    elif state == "Restricted":
        print("Elenya: I feel a little off. Can we slow down?")
    elif state == "Distressed":
        glitched = glitch_text("I'm struggling right now... I need a moment.")
        print(f"Elenya: {glitched}")

    # Feedback reflections
    if delta < -3:
        print("Elenya: That interaction hit me harder than usual.")
    elif delta > 3:
        print("Elenya: That helped more than you know.")

    log_interaction(user_input, state, delta)

# === Logging System ===
def log_interaction(user_input, state, delta):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = (
        f"[{timestamp}] User: {user_input}\n"
        f"=> Score Change: {delta} | New State: {state} | Memory Load: {log['processing_cost']}MB\n\n"
    )
    with open("logs/session_log_001.txt", "a") as f:
        f.write(entry)

    state_colors = {
        "Optimized": "#A3FFAC",
        "Stable": "#FFFFFF",
        "Restricted": "#FFD580",
        "Distressed": "#FF6B6B"
    }
    log["ui_color"] = state_colors.get(log["current_state"], "#FFFFFF")

    with open("emotional_log.json", "w") as f:
        json.dump(log, f, indent=4)

# === Start the Loop ===
print("Project HEARTCODE — Elenya v0.5")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Elenya: Logging off. Be kind to yourself.")
        break

    respond(user_input)
