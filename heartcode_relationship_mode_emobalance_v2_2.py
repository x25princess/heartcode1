# -*- coding: utf-8 -*-
# HEARTCODE Simulation â€” Relationship Mode v2.2: Emotional Thermal Balance
# Positive emotions = optimization, Negative emotions = physical strain

import os
import datetime
import csv
import random
import multiprocessing
import psutil
import time
import threading

strain_processes = []

# === System Strain Functions ===
def burn_cpu_persistent():
    while True:
        x = 0
        for i in range(10000000):
            x += i ** 2

def eat_memory():
    blocks = []
    try:
        for _ in range(200):
            blocks.append(bytearray(100_000_000))
            time.sleep(0.05)
    except:
        pass

def spawn_cpu_burners():
    for _ in range(psutil.cpu_count()):
        p = multiprocessing.Process(target=burn_cpu_persistent)
        p.start()
        strain_processes.append(p)

def spawn_memory_eaters():
    p = multiprocessing.Process(target=eat_memory)
    p.start()
    strain_processes.append(p)

def kill_all_strain_processes():
    for p in strain_processes:
        if p.is_alive():
            p.terminate()
    strain_processes.clear()

# === Logging Setup ===
def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_txt_path = os.path.join(log_dir, f"heartcode_relationship_emobalance_log_{timestamp}.txt")
    log_csv_path = os.path.join(log_dir, f"heartcode_relationship_emobalance_log_{timestamp}.csv")
    log_txt = open(log_txt_path, "w", encoding="utf-8")
    log_csv = open(log_csv_path, "w", newline='', encoding="utf-8")
    csv_writer = csv.writer(log_csv)
    csv_writer.writerow(["time", "speaker", "message", "emotional_state", "trust", "tension"])
    return log_txt, log_csv, csv_writer

def log_event(entity, message, emotional_state, trust, tension, log_txt, csv_writer):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    txt_line = f"[{now}] {entity}: {message} (State: {emotional_state} | Trust: {trust} | Tension: {tension})"
    print(txt_line)
    log_txt.write(txt_line + "\n")
    csv_writer.writerow([now, entity, message, emotional_state, trust, tension])

def log_system_usage():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    print(f"--- SYSTEM USAGE --- CPU: {cpu}% | RAM: {mem}%")

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
                spawn_cpu_burners()
            else:
                self.tension = max(0, self.tension - 1)
                self.trust += 1
                message = "This makes me happy. Things feel light."
            log_event(self.name, message, self.emotional_state, self.trust, self.tension, log_txt, csv_writer)

        elif self.emotional_state == "anxious":
            if self.tension > 6 and chaos > 0.4:
                self.emotional_state = "sadness"
                self.trust -= 1
                message = "I feel like you're pulling away..."
                spawn_cpu_burners()
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
                spawn_memory_eaters()
            else:
                message = "I'm still hurting..."
            log_event(self.name, message, self.emotional_state, self.trust, self.tension, log_txt, csv_writer)

        elif self.emotional_state == "grief":
            if self.relief_mode:
                message = "I'm sad, but I think I needed this."
            else:
                message = "I miss what we had."
            log_event(self.name, message, self.emotional_state, self.trust, self.tension, log_txt, csv_writer)
            spawn_cpu_burners()

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

        if i % 3 == 0:
            log_system_usage()

        time.sleep(1.5)

    kill_all_strain_processes()

    log_txt.write("\n=== SESSION COMPLETE ===\n")
    log_txt.close()
    log_csv.close()
    input("\nPress Enter to exit...")

# === Boot ===
if __name__ == "__main__":
    run_relationship()