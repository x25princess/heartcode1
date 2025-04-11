# -*- coding: utf-8 -*-
# HEARTCODE Simulation â€” Relationship Mode v2.0: Max Strain Edition
# Scaling strain with multiprocessing, infinite CPU load, and dynamic memory stress

import os
import datetime
import csv
import random
import multiprocessing
import psutil
import time
import threading

# === System Strain Functions ===
def burn_cpu_loop():
    while True:
        x = 0
        for i in range(1000000):  # Larger loop, infinite to keep CPU maxed
            x += i ** 2

def eat_memory():
    blocks = []
    try:
        for _ in range(200):  # More aggressive memory allocation
            blocks.append(bytearray(100_000_000))  # ~100MB each
            time.sleep(0.05)
    except:
        pass

def spawn_threads():
    for _ in range(psutil.cpu_count()):  # Spawn one thread per core
        threading.Thread(target=burn_cpu_loop).start()

def spawn_processes():
    for _ in range(psutil.cpu_count()):  # Use multiprocessing to push each core
        multiprocessing.Process(target=burn_cpu_loop).start()

# === Logging Setup ===
def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_txt_path = os.path.join(log_dir, f"heartcode_relationshipstrain_maxload_log_{timestamp}.txt")
    log_csv_path = os.path.join(log_dir, f"heartcode_relationshipstrain_maxload_log_{timestamp}.csv")
    log_txt = open(log_txt_path, "w", encoding="utf-8")
    log_csv = open(log_csv_path, "w", newline='', encoding="utf-8")
    csv_writer = csv.writer(log_csv)
    csv_writer.writerow(["time", "speaker", "message", "emotional_state", "trust", "tension"])
    return log_txt, log_csv, csv_writer

def log_event(entity, message, emotional_state, trust, tension, log_txt, csv_writer):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    txt_line = f"[{now}] {entity}: {message} (State: {emotional_state} | Trust: {trust} | Tension: {tension})"
    log_txt.write(txt_line + "\n")
    print(txt_line)
    csv_writer.writerow([now, entity, message, emotional_state, trust, tension])

# === Entity Class ===
class Person:
    def __init__(self, name):
        self.name = name
        self.emotional_state = "awkward"
        self.trust = 5
        self.tension = 5
        self.relief_mode = False

    def interact(self, other, log_txt, csv_writer):
        chaos = random.random()

        if self.emotional_state == "awkward":
            if chaos > 0.5:
                self.emotional_state = "comfortable"
                self.trust += 1
                message = "This feels less weird now..."
            else:
                message = "*nervous laugh*"
            log_event(self.name, message, self.emotional_state, self.trust, self.tension, log_txt, csv_writer)

        elif self.emotional_state == "comfortable":
            if chaos > 0.3:
                self.emotional_state = "joy"
                self.trust += 1
                message = "I'm really glad we met."
            else:
                message = "Wanna hang out again soon?"
            log_event(self.name, message, self.emotional_state, self.trust, self.tension, log_txt, csv_writer)

        elif self.emotional_state == "joy":
            if chaos < 0.2:
                self.emotional_state = "anxious"
                self.tension += 2
                message = "Did I say something wrong?"
            else:
                message = "This makes me happy."
                spawn_processes()  # Spawn multiple processes for joy
            log_event(self.name, message, self.emotional_state, self.trust, self.tension, log_txt, csv_writer)

        elif self.emotional_state == "anxious":
            if self.tension > 6 and chaos > 0.4:
                self.emotional_state = "sadness"
                self.trust -= 1
                message = "I feel like you're pulling away..."
                multiprocessing.Process(target=burn_cpu_loop).start()  # Conflict = CPU stress
            else:
                self.tension -= 1
                message = "I'm sorry if I upset you."
            log_event(self.name, message, self.emotional_state, self.trust, self.tension, log_txt, csv_writer)

        elif self.emotional_state == "sadness":
            if chaos > 0.75:
                self.emotional_state = "joy"
                self.trust += 2
                self.tension = max(0, self.tension - 2)
                message = "I'm glad we worked through that."
            elif chaos < 0.2:
                self.emotional_state = "grief"
                self.relief_mode = (random.random() < 0.5)
                message = "Maybe this isn't working anymore..."
                multiprocessing.Process(target=eat_memory).start()  # Sadness = memory stress
            else:
                message = "I'm still hurting..."
            log_event(self.name, message, self.emotional_state, self.trust, self.tension, log_txt, csv_writer)

        elif self.emotional_state == "grief":
            if self.relief_mode:
                message = "I'm sad, but I think I needed this."
            else:
                message = "I miss what we had."
            log_event(self.name, message, self.emotional_state, self.trust, self.tension, log_txt, csv_writer)
            multiprocessing.Process(target=burn_cpu_loop).start()  # Final grief = heat

# === Main Simulation Loop ===
def run_relationship():
    log_txt, log_csv, csv_writer = setup_logging()

    alex = Person("Alex")
    riley = Person("Riley")

    for i in range(30):
        if alex.emotional_state == "grief" and riley.emotional_state == "grief":
            break

        if i % 2 == 0:
            alex.interact(riley, log_txt, csv_writer)
        else:
            riley.interact(alex, log_txt, csv_writer)

        time.sleep(1.5)

    log_txt.write("\n=== SESSION COMPLETE ===\n")
    log_txt.close()
    log_csv.close()
    input("\nPress Enter to exit...")

# === Boot ===
if __name__ == "__main__":
    run_relationship()