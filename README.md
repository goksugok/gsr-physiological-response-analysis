# GSR-Based Physiological Response Measurement and Analysis

An Arduino–Python data acquisition and analysis workflow used in an experiment involving real and AI-generated facial stimuli.

> **Portfolio status:** Archived research code with a synthetic reproducibility example. This repository documents the implementation; it does not include participant records or make claims about statistical outcomes.

## Overview

The project combined an Arduino-based galvanic skin response (GSR) sensor circuit, a Python serial logger, and OpenSesame stimulus presentation. GSR readings and experimental events were recorded separately, then aligned for trial-level analysis.

### Pipeline

1. `arduino/ard_python.ino`: read analog values from pin A0 and print them to the serial port (9600 baud; 500 ms delay).
2. `python/gsr_logger.py`: save serial readings to participant-specific `time,gsr` CSV files. The archived version is configured for Windows COM9; change this to match your computer. Stop it with Ctrl+C (the original script does not explicitly close the file in a `finally` block).
3. OpenSesame: present stimuli and record trial events and responses. The original packaged experiment is not distributed here because image redistribution rights have not been confirmed.
4. `python/analysis.py`: align event timestamps to GSR time using manually recorded first-image synchronization offsets, then calculate baseline, peak, and a peak-minus-baseline measure in a 4-second window for each trial.
5. `python/merge_final.py`: concatenate all participant-level trial files into one CSV for further analysis.

## Project structure

```text
arduino/ard_python.ino
python/gsr_logger.py
python/analysis.py
python/merge_final.py
examples/synthetic/             # fabricated measurements and events, not participants
run_demo.py                      # runs a self-contained demonstration
requirements.txt
.gitignore
```

## Try the processing pipeline

Python 3.9+ is sufficient for the analysis scripts and demo; `pyserial` is only required for acquiring data from an Arduino.

```bash
python run_demo.py
```

The demo uses a temporary directory and synthetic inputs and checks that trial-level outputs were produced. No private data is needed. For a real experiment, `analysis.py` expects the following structure in its current working directory:

```text
opensesame_files/subject-1.csv
  # rows with time_image_screen, trial_id, stimulus, familiarity,
  # response, correct, response_time
gsr_files/gsr_001.csv
  # rows with time, gsr
first_photo_times.csv
  # participant, gsr_first_photo_time
```

## Analysis definition and cautions

For each image onset, the original pipeline selects GSR samples from onset through onset + 4 seconds (inclusive). It defines `baseline_gsr` as the first observed sample in this window, `peak_gsr` as the maximum in that window, and `scr` as `peak_gsr - baseline_gsr`.

**Important:** These are changes in raw Arduino ADC counts, not calibrated skin conductance in microsiemens (µS). Peak-minus-first-sample is a simplified trial-level proxy, and should not automatically be identified with a validated electrodermal SCR amplitude. Event synchronization depends on `first_photo_times.csv` and should be independently validated before scientific interpretation. Raw timestamps and missing samples can affect results.

## Privacy and assets

No real participant-level datasets, potentially identifying logs, or research stimulus images are included. The `examples/synthetic/` data are fabricated and are only for demonstrating the code. Real participant data should not be pushed to a public repository without appropriate consent and ethical review, even when direct identifiers have been removed.

## Next steps

- Add a confirmed circuit schematic and photographs without identifiable participants.
- Review the OpenSesame experiment for a redistributable version without third-party stimuli.
- Add validated signal preprocessing and quality-control visualizations.
- Document the acquisition hardware, sensor calibration, study protocol, and research outcomes only after checking the original records.

## Technologies

Arduino / C++, Python, pyserial, OpenSesame, CSV, serial communication, data acquisition, experimental stimulus timing.
