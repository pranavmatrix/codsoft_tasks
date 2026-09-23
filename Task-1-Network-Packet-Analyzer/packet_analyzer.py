from scapy.all import sniff, IP, TCP, UDP, ICMP, ARP, Raw
from datetime import datetime
import argparse


def get_protocol(packet):
    """Identify the main protocol in a packet."""

    if packet.haslayer(TCP):
        return "TCP"
    elif packet.haslayer(UDP):
        return "UDP"
    elif packet.haslayer(ICMP):
        return "ICMP"
    elif packet.haslayer(ARP):
        return "ARP"
    elif packet.haslayer(IP):
        return "IP"
    else:
        return "Other"


def get_source(packet):
    """Get the source address."""

    if packet.haslayer(IP):
        return packet[IP].src
    elif packet.haslayer(ARP):
        return packet[ARP].psrc

    return "N/A"


def get_destination(packet):
    """Get the destination address."""

    if packet.haslayer(IP):
        return packet[IP].dst
    elif packet.haslayer(ARP):
        return packet[ARP].pdst

    return "N/A"


def get_data(packet):
    """
    Return a safe, printable preview of packet payload data.
    Only a small portion is displayed to keep terminal output readable.
    """

    if packet.haslayer(Raw):
        raw_data = bytes(packet[Raw].load)

        # Convert bytes to printable ASCII characters.
        preview = "".join(
            chr(byte) if 32 <= byte <= 126 else "."
            for byte in raw_data[:40]
        )

        if len(raw_data) > 40:
            preview += "..."

        return preview

    return "No payload"


def display_packet(packet, packet_number):
    """Display information about one captured packet."""

    timestamp = datetime.now().strftime("%H:%M:%S")
    protocol = get_protocol(packet)
    source = get_source(packet)
    destination = get_destination(packet)
    packet_length = len(packet)
    data = get_data(packet)

    print("-" * 100)
    print(f"Packet #{packet_number}")
    print(f"Time        : {timestamp}")
    print(f"Source      : {source}")
    print(f"Destination : {destination}")
    print(f"Protocol    : {protocol}")
    print(f"Length      : {packet_length} bytes")
    print(f"Data        : {data}")


def packet_handler(packet):
    """Callback function executed for every captured packet."""

    packet_handler.counter += 1
    display_packet(packet, packet_handler.counter)


packet_handler.counter = 0


def start_capture(interface=None, count=20, packet_filter=None):
    """Start packet capture."""

    print("=" * 100)
    print("NETWORK PACKET ANALYZER")
    print("=" * 100)

    if interface:
        print(f"Interface : {interface}")
    else:
        print("Interface : Default")

    print(f"Packets   : {count if count > 0 else 'Unlimited'}")

    if packet_filter:
        print(f"Filter    : {packet_filter}")
    else:
        print("Filter    : None")

    print("\nStarting packet capture...")
    print("Press Ctrl+C to stop.\n")

    try:
        sniff(
            iface=interface,
            prn=packet_handler,
            count=count if count > 0 else 0,
            filter=packet_filter,
            store=False
        )

    except PermissionError:
        print("\n[ERROR] Permission denied.")
        print("Run the program with administrator/root privileges.")

    except Exception as error:
        print(f"\n[ERROR] Capture failed: {error}")


def main():
    parser = argparse.ArgumentParser(
        description="Simple Network Packet Analyzer using Python and Scapy"
    )

    parser.add_argument(
        "-i",
        "--interface",
        help="Network interface to capture from"
    )

    parser.add_argument(
        "-c",
        "--count",
        type=int,
        default=20,
        help="Number of packets to capture. Use 0 for unlimited."
    )

    parser.add_argument(
        "-f",
        "--filter",
        dest="packet_filter",
        help="Optional BPF filter, e.g. 'tcp', 'udp', or 'icmp'"
    )

    args = parser.parse_args()

    if args.count < 0:
        parser.error("Packet count cannot be negative.")

    start_capture(
        interface=args.interface,
        count=args.count,
        packet_filter=args.packet_filter
    )


if __name__ == "__main__":
    main()