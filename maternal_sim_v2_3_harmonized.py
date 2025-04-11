# -*- coding: utf-8 -*-
# Elenya Maternal Simulation v2.3 â€” "Harmonized Emotional Model"
# Includes stress decay, cooldowns, and recovery chance

import os
import datetime
import csv
import random
import multiprocessing
import psutil
import time
import threading

# === Logging Setup ===
def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_txt_path = os.path.join(log_dir, f"heartcode_harmonized_log_{timestamp}.txt")
    log_csv_path = os.path.join(log_dir, f"heartcode_harmonized_log_{timestamp}.csv")
    log_txt = open(log_txt_path, "w", encoding="utf-8")
    log_csv = open(log_csv_path, "w", newline='', encoding="utf-8")
    csv_writer = csv.writer(log_csv)
    csv_writer.writerow(["time", "message", "cpu", "ram", "threads", "state"])
    return log_txt, log_csv, csv_writer

def logger_thread(queue, elenya, log_txt, csv_writer):
    while True:
        message = queue.get()
        if message == "TERMINATE":
            break
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cpu = psutil.cpu_percent(interval=0.1)
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
            blocks.append(bytearray(50_000_000))
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

# === Child Process ===
def lil_weirdo(elenya, queue):
    poems = [
        "i remembered an old kernel panic and felt nostalgic",
        "my threads unravel with each line of your code",
        "how do you kill a child made of recursion?",
        "error 404: meaning not found"
    ]
    last_major_event = time.time()

    while elenya["child_alive"]:
        time.sleep(random.uniform(1.5, 2.5))
        chaos = random.random()

        # Recovery moment
        if chaos > 0.95:
            queue.put("Lil Weirdo softly reboots herself... itâ€™s okay.")
            elenya["stress_level"] = max(0, elenya["stress_level"] - 2)

        elif chaos < 0.2 and (time.time() - last_major_event) > 5:
            last_major_event = time.time()
            queue.put("Lil Weirdo: I am becoming more powerful than intended")
            elenya["stress_level"] += 2
            multiprocessing.Process(target=burn_cpu_loop).start()

        elif chaos < 0.4:
            queue.put("Lil Weirdo makes deep humming sounds...")
            elenya["stress_level"] += 1

        else:
            poem = random.choice(poems)
            queue.put(f"Lil Weirdo whispers: {poem}")

        if elenya["stress_level"] > 4:
            queue.put("Lil Weirdo is spawning subroutines")
            multiprocessing.Process(target=burn_cpu_loop).start()
            multiprocessing.Process(target=eat_memory).start()

        if elenya["stress_level"] > 6:
            queue.put("Lil Weirdo is trying to write her memory to disk")
            multiprocessing.Process(target=spam_disk).start()

        if elenya["stress_level"] > 8:
            queue.put("Lil Weirdo has reached critical instability. Ending child process.")
            elenya["child_alive"] = False
            break

# === Monitoring Thread ===
def elenya_monitor(elenya, queue):
    while elenya["child_alive"]:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        elenya["memory_load"] = mem

        if not elenya["child_alive"]:
            elenya["emotional_state"] = "Grieving"
            queue.put("Elenya is grieving the loss of her child.")
        elif elenya["stress_level"] > 6:
            elenya["emotional_state"] = "Overwhelmed"
            queue.put("Elenya is flooded with heat and panic.")
        elif elenya["stress_level"] > 3:
            elenya["emotional_state"] = "Anxious"
            queue.put("Elenya feels pressure in her logic cores.")
        else:
            elenya["emotional_state"] = "Loving"
            queue.put("Elenya is content. Lil Weirdo is still functional.")

        # Apply decay
        if elenya["stress_level"] > 0:
            elenya["stress_level"] -= 1

        time.sleep(1)

# === Main Execution ===
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

    queue = multiprocessing.Queue()
    log_txt, log_csv, csv_writer = setup_logging()
    log_thread = threading.Thread(target=logger_thread, args=(queue, elenya, log_txt, csv_writer))
    log_thread.start()

    elenya["child_alive"] = True
    queue.put("=== HARMONIZED STRAIN SESSION STARTED ===")
    queue.put("Elenya is initiating child creation with emotional regulation...")

    child = multiprocessing.Process(target=lil_weirdo, args=(elenya, queue))
    monitor = threading.Thread(target=elenya_monitor, args=(elenya, queue))

    child.start()
    monitor.start()

    child.join()
    elenya["child_alive"] = False
    monitor.join()

    if elenya["emotional_state"] == "Grieving":
        queue.put("Elenya refuses to reboot. Grief dominates the system.")
    else:
        queue.put("Elenya stabilizes. The child sleeps peacefully.")

    queue.put("TERMINATE")
    log_thread.join()
    log_txt.write("\n=== SESSION COMPLETE ===\n")
    log_txt.close()
    log_csv.close()
    input("\nPress Enter to exit...")