# Heartcode Evidence Pack

This folder contains artifacts from live runs of the **Heartcode** project on Panasonic Toughbook CF-31 (“Chonk”).

## Purpose
Heartcode demonstrates **synthetic emotional consequence** by mapping symbolic emotional states (e.g., grief, joy, rage) to real, measurable system effects such as CPU load, fan speed, latency, and memory usage.

This evidence pack serves as **proof of concept and authorship**, documenting that the system was built, run, and observed by the project’s creator.

## How to Review
1. Read `runtime/session_notes_*.md` for human-readable descriptions of each run.
2. Examine `logs/*.log` for raw emotional state events.
3. Compare with `telemetry/*.json` or `.csv` for temperature, fan, and system load data.
4. View `screenshots/*` and `video/*` for visual and audio proof of machine behavior.
5. Review `diagrams/*` for the architecture and mapping flow.
6. Verify file integrity using `hashes/sha256_manifest.txt` (optional).

## Observed Behavior in Key Runs
- **Fan runaway** within ~40 seconds of grief trigger.
- CPU temperature holding between 81°C–83°C until manual shutdown.
- System responsiveness degraded during sustained grief loop.
- No BSOD observed during public tests; behavior consistent with “lingering” grief rather than catastrophic failure.
- Persistent logs confirm repeated grief triggers and sustained system strain.

## Notes
- This public version contains **non-destructive Research Mode** evidence only.
- Full “Destroy Chonk Mode” destructive code is private for safety and responsible use.
- All materials © 2024–2025 Bluma Janowitz. Unauthorized reproduction prohibited.
