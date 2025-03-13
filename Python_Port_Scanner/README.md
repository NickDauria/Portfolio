# Python Port Scanner

## Overview
This project is an advanced Python port scanner designed to identify open ports and detect basic services on a target IP address or hostname. It leverages threading for speed, service detection for insight, and file output for documentation, making it a powerful tool for network security assessments.

## Features
- **Parallel Scanning**: Uses threading to scan multiple ports simultaneously, improving efficiency.
- **Service Detection**: Identifies common services (e.g., SSH, HTTP, HTTPS, RPC, SMB, RDP) on open ports through port mapping and basic probing.
- **Customizable Timeout**: Adjustable per-port timeout via command-line argument.
- **Output to File**: Saves scan results to a specified text file.
- **Color-Coded Output**: Highlights open ports in green for quick identification.

## Prerequisites
- Python 3.x installed on your system.
- Basic understanding of command-line usage.

## Usage
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/[YourUsername]/CybersecurityProjects.git
