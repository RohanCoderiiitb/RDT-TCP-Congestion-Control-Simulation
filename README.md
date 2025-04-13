# RDT-TCP-Congestion-Control-Simulation

# Reliable Data Transfer and TCP Congestion Control Protocols Implementation

This repository contains implementations of the following network protocols as part of a programming assignment:
- **RDT 2.2 (NAK-Free Reliable Data Transfer) Protocol**
- **RDT 3.0 (Reliable Data Transfer Over a Lousy Channel) Protocol**
- **TCP Tahoe Congestion Control Mechanism**
- **TCP Reno Congestion Control Mechanism**

These implementations are written in Python and aim to simulate the specified protocols with configurable parameters, logging, and (where applicable) visualization.

## Table of Contents
- [Overview](#overview)
- [Implementation Details](#implementation-details)
- [Files](#files)
- [Usage](#usage)
- [Parameters](#parameters)
- [Testing](#testing)
- [Deliverables](#deliverables)
- [Report](#report)
- [Contributing](#contributing)
- [License](#license)

## Overview
This project fulfills the requirements of a programming assignment focusing on reliable data transfer (RDT) and TCP congestion control protocols. Each implementation includes:
- Packet structures with sequence numbers, payloads, and checksums.
- Unreliable channel simulations with configurable error and loss rates.
- Finite State Machines (FSMs) for sender and receiver behavior.
- Timer mechanisms for retransmissions (RDT 3.0).
- Logging of state transitions, packet handling, and (for TCP) congestion window evolution.
- Optional visualization of TCP congestion window behavior.

## Implementation Details
- **RDT 2.2**: A stop-and-wait protocol that handles bit errors with ACKs, retransmitting on duplicate ACKs.
- **RDT 3.0**: Extends RDT 2.2 with packet loss handling and a timer-based retransmission mechanism.
- **TCP Tahoe**: Simulates congestion control with slow start, congestion avoidance, and a reset to 1 MSS on loss.
- **TCP Reno**: Adds fast recovery to TCP Tahoe, adjusting cwnd on triple duplicate ACKs.

All implementations use Python for simplicity and include logging for debugging and analysis.

## Files
- `rdt_2.2.py`: Implementation of RDT 2.2 protocol.
- `rdt_3.0.py`: Implementation of RDT 3.0 protocol.
- `tcp_tahoe.py`: Simulation of TCP Tahoe congestion control.
- `tcp_reno.py`: Simulation of TCP Reno congestion control.
- `README.md`: This file.
- `report.pdf`: A 2-3 page report (to be added) detailing the implementation, parameter choices, and sample outputs.

## Usage
1. **Prerequisites**:
   - Python 3.x
   - For TCP implementations, install matplotlib: `pip install matplotlib`

2. **Running the Code**:
   - Navigate to the directory containing the script (e.g., `rdt_3.0.py`).
   - Run `python rdt_3.0.py` in the terminal.
   - Follow prompts to input messages (type "done" to finish).

3. **TCP Visualization**:
   - Run `python tcp_tahoe.py` or `python tcp_reno.py` to see a plot of the congestion window.

## Parameters
- **RDT 2.2 and 3.0**:
  - `error_rate`: Probability of bit corruption (default 0.2 for RDT 3.0, adjustable in `NetworkChannel`).
  - `loss_rate`: Probability of packet loss (default 0.1 for RDT 3.0, not applicable in RDT 2.2).
  - Timer duration: 2 seconds in RDT 3.0 (adjustable in `time.sleep()`).
- **TCP Tahoe and Reno**:
  - `mss`: Maximum Segment Size (default 1).
  - `initial_ssthresh`: Initial slow start threshold (default 8).
  - `max_rtt`: Maximum simulation rounds (default 50).
  - `loss_interval`: Interval for loss events (default 15 or 8 to match graphs).

Modify these values in the `main()` function of each script.

## Testing
- Test RDT protocols by inputting multiple messages and varying `error_rate` and `loss_rate` to observe retransmissions and error handling.
- Test TCP protocols by adjusting `loss_interval` and observing the saw-tooth pattern in the generated plots.
- Sample outputs are logged to the console; graphical results are displayed for TCP simulations.

## Deliverables
- Source code files (`rdt_2.2.py`, `rdt_3.0.py`, `tcp_tahoe.py`, `tcp_reno.py`).
- A `report.pdf` (to be added) including:
  - Description of each implementation.
  - Rationale for parameter choices (e.g., error rates, timer duration).
  - Sample console outputs and graphical results for TCP.

## Report
The report is a 2-3 page PDF document detailing:
- Implementation approach for each protocol.
- Parameter selections and their impact.
- Sample logs and plots (e.g., TCP Tahoe/Reno saw-tooth behavior).
- Observations from testing under various error and loss conditions.
