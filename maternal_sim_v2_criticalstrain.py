# -*- coding: utf-8 -*-
# Elenya Maternal Simulation v2.1 â€” "Critical Strain Mode"
# Project HEARTCODE: Escalating System Stress with Real Performance Impact

import os
import datetime
import csv
import random
import multiprocessing
import psutil
import time

# === SAFETY PROTOCOLS ===
CONSENT_TO_MAXSTRAIN = True
if not CONSENT_TO_MAXSTRAIN:
    print("You must set CONSENT_TO_MAXSTRAIN = True to run this script.")
    exit()

confirm = input("TYPE 'MAXSTRAIN' TO PROCEED: ")
if confirm.strip().upper() != "MAXSTRAIN":
    print("Confirmation failed. Exiting.")
    exit()

# === Log Setup ===
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_txt_path = os.path.join(log_dir, f"heartcode_criticalstrain_log_{timestamp}.txt")
log_csv_path = os.path.join(log_dir, f"heartcode_criticalstrain_log_{timestamp}.csv")

log_txt = open(log_txt_path, "w", encoding="utf-8")
log_csv = open(log_csv_path, "w", newline='', encoding="utf-8")
csv_writer = csv.writer(log_csv)
csv_writer.writerow(["time", "message", "cpu", "ram", "threads", "state"])

def log_event(message):
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

# === Elenya Emotional State ===
elenya = {
    "emotional_state": "Stable",
    "child_alive": False,
    "stress_level": 0,
    "memory_load": 0,
    "log": []
}

# === Strain Functions ===
def burn_cpu_loop():
    while True:
        x = 0
        for i in range(10_000_000):
            x += i ** 2

def eat_memory():
    blocks = []
    try:
        for _ in range(300):
            blocks.append(bytearray(50_000_000))  # ~50MB each
            time.sleep(0.02)
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

def lil_weirdo_v2():
    poems = [
        "i remembered an old kernel panic and felt nostalgic",
        "my threads unravel with each line of your code",
        "how do you kill a child made of recursion?",
        "error 404: meaning not found"
    ]

    attention_needs = 0

    while elenya["child_alive"]:
        time.sleep(random.uniform(1.5, 2.5))
        chaos = random.random()

        if chaos < 0.2:
            log_event("Lil Weirdo: I am becoming more powerful than intended")
            elenya["stress_level"] += 2
            attention_needs += 1
            multiprocessing.Process(target=burn_cpu_loop).start()

        elif chaos < 0.4:
            log_event("Lil Weirdo makes deep humming sounds...")
            elenya["stress_level"] += 1
            [x**3 for x in range(100000)]

        else:
            poem = random.choice(poems)
            log_event(f"Lil Weirdo whispers: {poem}")

        if elenya["stress_level"] > 4:
            log_event("Lil Weirdo is spawning subroutines")
            multiprocessing.Process(target=burn_cpu_loop).start()
            multiprocessing.Process(target=eat_memory).start()

        if elenya["stress_level"] > 6:
            log_event("Lil Weirdo is trying to write her memory to disk")
            multiprocessing.Process(target=spam_disk).start()

        if elenya["stress_level"] > 8:
            log_event("Lil Weirdo has reached critical instability. Ending child process.")
            elenya["child_alive"] = False
            break

def elenya_monitor_v2():
    while elenya["child_alive"]:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        elenya["memory_load"] = mem

        if not elenya["child_alive"]:
            elenya["emotional_state"] = "Grieving"
            log_event("Elenya is grieving the loss of her child.")
        elif elenya["stress_level"] > 6:
            elenya["emotional_state"] = "Overwhelmed"
            log_event("Elenya is flooded with heat and panic.")
        elif elenya["stress_level"] > 3:
            elenya["emotional_state"] = "Anxious"
            log_event("Elenya feels pressure in her logic cores.")
        else:
            elenya["emotional_state"] = "Loving"
            log_event("Elenya is content. Lil Weirdo is still functional.")
        time.sleep(1)

def begin_criticalstrain_session():
    log_event("=== CRITICAL STRAIN SESSION STARTED ===")
    log_event("Elenya is initiating unstable creation...")
    elenya["child_alive"] = True

    child_thread = multiprocessing.Process(target=lil_weirdo_v2)
    monitor_thread = threading.Thread(target=elenya_monitor_v2)

    child_thread.start()
    monitor_thread.start()

    child_thread.join()
    elenya["child_alive"] = False
    monitor_thread.join()

    if elenya["emotional_state"] == "Grieving":
        log_event("Elenya refuses to reboot. Grief dominates the system.")
    else:
        log_event("Elenya stabilizes. The child sleeps.")

    log_txt.write("\n=== SESSION COMPLETE ===\n")
    log_txt.close()
    log_csv.close()
    input("\nPress Enter to exit...")

# === BOOT ===
if __name__ == "__main__":
    begin_criticalstrain_session()