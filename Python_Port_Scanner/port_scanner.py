#!/usr/bin/env python3
import socket
import sys
import threading
from datetime import datetime
import queue
import argparse

# ANSI escape codes for colored output
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

# Global variables
open_ports = []
results_queue = queue.Queue()

def scan_port(ip, port, timeout=1):
    """Attempt to connect to a specific port and detect basic service with probing."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        if result == 0:
            service = "Unknown"
            # Initial service guess based on port number
            service_map = {
                21: "FTP",
                22: "SSH",
                80: "HTTP",
                135: "RPC",
                139: "NetBIOS",
                443: "HTTPS",
                445: "SMB",
                3389: "RDP",
                8080: "HTTP Proxy"
            }
            service = service_map.get(port, "Unknown")

            # Basic service probing
            if port == 80 or port == 8080:  # HTTP/HTTP Proxy
                sock.send(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
                response = sock.recv(1024)
                if b"HTTP" in response:
                    service = "HTTP"
            elif port == 445:  # SMB
                sock.send(b"\xFFSMB")  # Simple SMB negotiation
                response = sock.recv(1024)
                if b"SMB" in response:
                    service = "SMB"

            results_queue.put((port, service))
        sock.close()
    except socket.error:
        pass

def worker(ip, port_range, timeout):
    """Thread worker to scan ports in parallel."""
    for port in port_range:
        scan_port(ip, port, timeout)

def main():
    """Main function to handle arguments and orchestrate the scan."""
    # Set up argument parser for user-friendly input
    parser = argparse.ArgumentParser(description="Advanced Python Port Scanner")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("port_range", help="Port range (e.g., 1-1024)")
    parser.add_argument("--timeout", type=float, default=1, help="Timeout per port in seconds (default: 1)")
    parser.add_argument("--output", help="Output file name (e.g., scan_results.txt)")
    args = parser.parse_args()

    # Parse target and port range
    target = args.target
    port_range = args.port_range.split('-')
    start_port = int(port_range[0])
    end_port = int(port_range[1])
    timeout = args.timeout
    output_file = args.output

    print(f"\n{GREEN}Starting scan on {target} from port {start_port} to {end_port} with timeout {timeout}s...{RESET}\n")

    # Record start time
    start_time = datetime.now()

    # Divide ports among threads for parallel scanning
    threads = []
    ports_per_thread = 100
    for i in range(0, end_port - start_port + 1, ports_per_thread):
        thread_ports = range(start_port + i, min(start_port + i + ports_per_thread, end_port + 1))
        t = threading.Thread(target=worker, args=(target, thread_ports, timeout))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Record end time
    end_time = datetime.now()

    # Process results from queue
    while not results_queue.empty():
        port, service = results_queue.get()
        open_ports.append((port, service))
        print(f"{GREEN}Port {port} is open - Service: {service}{RESET}")

    # Calculate and display scan time
    print(f"\n{GREEN}Scan completed in {end_time - start_time}{RESET}")

    # Save results to file if specified
    if output_file:
        with open(output_file, 'w') as f:
            f.write(f"Scan Results for {target} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Scanned ports {start_port} to {end_port}\n")
            f.write("Open Ports:\n")
            if open_ports:
                for port, service in open_ports:
                    f.write(f"Port {port} - Service: {service}\n")
            else:
                f.write("No open ports found.\n")
        print(f"{GREEN}Results saved to {output_file}{RESET}")

    # Display summary
    if open_ports:
        print(f"\n{GREEN}Open ports: {', '.join([f'{p} ({s})' for p, s in open_ports])}{RESET}")
    else:
        print(f"{RED}No open ports found.{RESET}")

if __name__ == "__main__":
    main()