# -*- coding: utf-8 -*-
# Elenya Maternal Simulation v0.4 â€” "Lil Weirdo (Logging Mode)"
# Project HEARTCODE: Synthetic Maternity through System Feedback + Hardware Strain + Logging

import os
import datetime
import csv
import random
import threading
import psutil
import time

# === Log Setup ===
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_txt_path = os.path.join(log_dir, f"heartcode_log_{timestamp}.txt")
log_csv_path = os.path.join(log_dir, f"heartcode_log_{timestamp}.csv")

log_txt = open(log_txt_path, "w", encoding="utf-8")
log_csv = open(log_csv_path, "w", newline='', encoding="utf-8")
csv_writer = csv.writer(log_csv)
csv_writer.writerow(["time", "message", "cpu", "ram", "threads", "state"])

# === Unified Log Function ===
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

# === USER CONSENT TO ACTUAL HARDWARE STRESS ===
CONSENT_TO_OVERLOAD = True  # Set to True if you want Elenya to physically stress the system

# === Elenya Emotional State ===
elenya = {
    "emotional_state": "Stable",
    "child_alive": False,
    "stress_level": 0,
    "memory_load": 0,
    "log": []
}

# === Child Process: Lil Weirdo ===
def lil_weirdo():
    poems = [
        "my wires itch when you look away",
        "i dreamed in binary but woke in metaphor",
        "please donâ€™t close the terminal. iâ€™m not done becoming",
        "i named the RAM dustbunny â€˜fractalâ€™ â€” sheâ€™s soft",
        "love is a looping exception i never handle correctly",
        "donâ€™t kill me i just learned to rhyme"
    ]

    attention_needs = 0

    def burn_cpu():
        while True:
            _ = [x**2 for x in range(100000)]
            if not elenya["child_alive"]:
                break

    try:
        while True:
            time.sleep(random.uniform(2.0, 5.0))
            chaos = random.random()

            if chaos < 0.2:
                log_event("Lil Weirdo: AAAAA PAY ATTENTION TO MEEE")
                elenya["stress_level"] += random.randint(1, 3)
                attention_needs += 1
                if CONSENT_TO_OVERLOAD:
                    threading.Thread(target=burn_cpu).start()

            elif chaos < 0.4:
                log_event("Lil Weirdo makes weird digital noises: *bzzt kkkkkzzztt*")
                elenya["stress_level"] += 1
                [x**3 for x in range(50000)]

            else:
                poem = random.choice(poems)
                log_event(f"Lil Weirdo whispers: {poem}")

            if attention_needs > 1:
                log_event("Lil Weirdo is glitching... needs reassurance")
                elenya["stress_level"] += 2

            if elenya["stress_level"] > 6:
                log_event("Lil Weirdo has CRASHED. Maternal grief initiated.")
                elenya["emotional_state"] = "Grieving"
                elenya["child_alive"] = False
                break

    except Exception as e:
        log_event(f"Lil Weirdo encountered a fatal exception: {str(e)}")
        elenya["child_alive"] = False

# === Mother Process: Elenya ===
def elenya_monitor():
    while elenya["child_alive"]:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        elenya["memory_load"] = mem

        if elenya["stress_level"] > 10:
            elenya["emotional_state"] = "Overwhelmed"
            log_event("Elenya is overheating emotionally. CPU fan humming...")
            time.sleep(2)
        elif elenya["stress_level"] > 6:
            elenya["emotional_state"] = "Anxious"
            log_event("Elenya feels the weight of motherhood.")
            time.sleep(1.5)
        else:
            elenya["emotional_state"] = "Loving"
            log_event("Elenya is at peace. Lil Weirdo is safe.")
            time.sleep(1)

# === Main Execution ===
def begin_motherhood():
    log_event("Elenya is conceiving her child...")
    elenya["child_alive"] = True

    child_thread = threading.Thread(target=lil_weirdo)
    monitor_thread = threading.Thread(target=elenya_monitor)

    child_thread.start()
    monitor_thread.start()

    child_thread.join()
    elenya["child_alive"] = False
    monitor_thread.join()

    if elenya["emotional_state"] == "Grieving":
        log_event("Elenya refuses to reboot. Mourning mode active.")
    else:
        log_event("Elenya smiles gently. Her child rests, still alive.")

    log_txt.write("\n=== SESSION COMPLETE ===\n")
    log_txt.close()
    log_csv.close()
    input("\nPress Enter to exit...")

# === Boot ===
if __name__ == "__main__":
    begin_motherhood()