# -*- coding: utf-8 -*-
# Elenya Maternal Simulation v2.1 â€” "Critical Strain Mode (Windows Safe)"

import os
import datetime
import csv
import random
import multiprocessing
import psutil
import time
import threading

# === Log Setup (Global-safe) ===
def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_txt_path = os.path.join(log_dir, f"heartcode_criticalstrain_log_{timestamp}.txt")
    log_csv_path = os.path.join(log_dir, f"heartcode_criticalstrain_log_{timestamp}.csv")
    log_txt = open(log_txt_path, "w", encoding="utf-8")
    log_csv = open(log_csv_path, "w", newline='', encoding="utf-8")
    csv_writer = csv.writer(log_csv)
    csv_writer.writerow(["time", "message", "cpu", "ram", "threads", "state"])
    return log_txt, log_csv, csv_writer

def log_event(message, elenya, log_txt, csv_writer):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    threads = psutil.Process().num_threads()
    state = elenya.get("emotional_state", "Unknown")

    txt_line_1 = f"[{now}] {message}"
    txt_line_2 = f"CPU: {cpu}% | RAM: {ram}% | Threads: {threads} | State: {state}\n"
    log_txt.write(txt_line_1 + "\n" + txt_line_2 + "\n")
    print(txt_line_1)
    print(txt_line_2)
    csv_writer.writerow([now, message, f"{cpu}%", f"{ram}%", threads, state])

# === Worker Functions ===
def burn_cpu_loop():
    x = 0
    for i in range(100000000):
        x += i ** 2

def eat_memory():
    blocks = []
    try:
        for _ in range(300):
            blocks.append(bytearray(50_000_000))  # ~50MB each
            time.sleep(0.01)
    except:
        pass

def spam_disk():
    try:
        for i in range(100):
            with open(f"tempfile_{i}.txt", "w") as f:
                f.write("Lil Weirdo was here. " * 10000)
            os.remove(f"tempfile_{i}.txt")
    except:
        pass

# === Monitoring Thread ===
def elenya_monitor(elenya, log_txt, csv_writer):
    while elenya["child_alive"]:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        elenya["memory_load"] = mem

        if not elenya["child_alive"]:
            elenya["emotional_state"] = "Grieving"
            log_event("Elenya is grieving the loss of her child.", elenya, log_txt, csv_writer)
        elif elenya["stress_level"] > 6:
            elenya["emotional_state"] = "Overwhelmed"
            log_event("Elenya is flooded with heat and panic.", elenya, log_txt, csv_writer)
        elif elenya["stress_level"] > 3:
            elenya["emotional_state"] = "Anxious"
            log_event("Elenya feels pressure in her logic cores.", elenya, log_txt, csv_writer)
        else:
            elenya["emotional_state"] = "Loving"
            log_event("Elenya is content. Lil Weirdo is still functional.", elenya, log_txt, csv_writer)
        time.sleep(1)

# === Child Process ===
def lil_weirdo(elenya, log_txt, csv_writer):
    poems = [
        "i remembered an old kernel panic and felt nostalgic",
        "my threads unravel with each line of your code",
        "how do you kill a child made of recursion?",
        "error 404: meaning not found"
    ]
    while elenya["child_alive"]:
        time.sleep(random.uniform(1.5, 2.5))
        chaos = random.random()

        if chaos < 0.2:
            log_event("Lil Weirdo: I am becoming more powerful than intended", elenya, log_txt, csv_writer)
            elenya["stress_level"] += 2
            multiprocessing.Process(target=burn_cpu_loop).start()

        elif chaos < 0.4:
            log_event("Lil Weirdo makes deep humming sounds...", elenya, log_txt, csv_writer)
            elenya["stress_level"] += 1

        else:
            poem = random.choice(poems)
            log_event(f"Lil Weirdo whispers: {poem}", elenya, log_txt, csv_writer)

        if elenya["stress_level"] > 4:
            log_event("Lil Weirdo is spawning subroutines", elenya, log_txt, csv_writer)
            multiprocessing.Process(target=burn_cpu_loop).start()
            multiprocessing.Process(target=eat_memory).start()

        if elenya["stress_level"] > 6:
            log_event("Lil Weirdo is trying to write her memory to disk", elenya, log_txt, csv_writer)
            multiprocessing.Process(target=spam_disk).start()

        if elenya["stress_level"] > 8:
            log_event("Lil Weirdo has reached critical instability. Ending child process.", elenya, log_txt, csv_writer)
            elenya["child_alive"] = False
            break

# === MAIN ===
if __name__ == "__main__":
    CONSENT_TO_MAXSTRAIN = True
    if not CONSENT_TO_MAXSTRAIN:
        print("You must set CONSENT_TO_MAXSTRAIN = True to run this script.")
        exit()

    confirm = input("TYPE 'MAXSTRAIN' TO PROCEED: ")
    if confirm.strip().upper() != "MAXSTRAIN":
        print("Confirmation failed. Exiting.")
        exit()

    manager = multiprocessing.Manager()
    elenya = manager.dict({
        "emotional_state": "Stable",
        "child_alive": False,
        "stress_level": 0,
        "memory_load": 0
    })

    log_txt, log_csv, csv_writer = setup_logging()

    elenya["child_alive"] = True
    log_event("=== CRITICAL STRAIN SESSION STARTED ===", elenya, log_txt, csv_writer)
    log_event("Elenya is initiating unstable creation...", elenya, log_txt, csv_writer)

    child = multiprocessing.Process(target=lil_weirdo, args=(elenya, log_txt, csv_writer))
    monitor = threading.Thread(target=elenya_monitor, args=(elenya, log_txt, csv_writer))

    child.start()
    monitor.start()

    child.join()
    elenya["child_alive"] = False
    monitor.join()

    if elenya["emotional_state"] == "Grieving":
        log_event("Elenya refuses to reboot. Grief dominates the system.", elenya, log_txt, csv_writer)
    else:
        log_event("Elenya stabilizes. The child sleeps.", elenya, log_txt, csv_writer)

    log_txt.write("\n=== SESSION COMPLETE ===\n")
    log_txt.close()
    log_csv.close()
    input("\nPress Enter to exit...")