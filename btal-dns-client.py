import socket
import sys
import struct
import random


def create_dns_query(hostname):
    """Create a DNS query message.

    Args:
        hostname (string): Given by user through the command line.

    Returns:
        bytes: DNS query message in bytes.
    """
    # Header
    header_row_0 = random.randint(0, 65535)
    # header_row_0 = 1000

    header_row_1 = 0x0100
    header_row_2 = 0x01
    header_row_3, header_row_4, header_row_5 = 0x00, 0x00, 0x00

    header = struct.pack(
        "!HHHHHH",
        header_row_0,
        header_row_1,
        header_row_2,
        header_row_3,
        header_row_4,
        header_row_5,
    )

    # Question
    q_type = 1
    encoded_domain = hostname_to_qname(hostname)

    # Combining header and question to form DNS query message.
    question = encoded_domain + struct.pack("!HH", q_type, 1)
    dns_message = header + question

    return dns_message


def hostname_to_qname(hostname):
    """Encoding the hostname for a DNS query message

    Args:
        hostname (string): url given from the command line

    Returns:
        bytes: url encoded for qname of DNS message
    """
    qname_parts = []
    for part in hostname.split("."):
        length = len(part)
        qname_parts.append(chr(length))
        qname_parts.append(part)
    qname_parts.append("\x00")
    qname = "".join(qname_parts)
    return qname.encode()


def send_dns_query_message(server, port, query):
    """Creates a UDP socket in order to form a connection with a DNS server. Sends the
    query message to the DNS server and waits for a response.

    Args:
        server (string): IP address of the DNS server
        port (int): port number of DNS server
        query (bytes): DNS query message created.
    """
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        udp_sock.sendto(query, (server, port))
        udp_sock.settimeout(5)
        data = udp_sock.recv(1024)

        process_dns_response(data)
    finally:
        udp_sock.close()


def process_dns_response(response):
    print(response)


# Error checking for command line arguments
if len(sys.argv) == 1:
    print(
        "\nPlease include hostname to prepare a DNS query\n\
Example input: btal-dns-client.py gmu.edu"
    )
    exit(0)
elif len(sys.argv) > 2:
    print(
        "\nPlease include only 1 hostname to prepare a DNS query.\n\
Example input: btal-dns-client.py gmu.edu"
    )
    exit(0)


dns_server = "8.8.8.8"
dns_port_number = 53

hostname = sys.argv[1]
query = create_dns_query(hostname)
send_dns_query_message(dns_server, dns_port_number, query)
