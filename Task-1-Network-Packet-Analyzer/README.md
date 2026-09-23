# Network Packet Analyzer

A simple network packet analyzer developed in Python using the Scapy
library.

This project captures network packets and displays important information
such as:

- Source IP address
- Destination IP address
- Protocol
- Packet length
- Packet payload preview
- Capture time

## Features

- Captures live network packets
- Supports TCP, UDP, ICMP, IP, and ARP packets
- Displays source and destination addresses
- Displays packet size
- Displays a limited printable payload preview
- Supports network-interface selection
- Supports packet-count limits
- Supports BPF packet filters
- Provides organized terminal output

## Technologies Used

- Python 3
- Scapy
- Command Line Interface

## Project Structure

```text
Task-1-Network-Packet-Analyzer/
│
├── packet_analyzer.py
├── requirements.txt
└── README.md