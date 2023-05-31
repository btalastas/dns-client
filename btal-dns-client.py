import socket
import sys
import struct
import random
from dnslib import DNSRecord


def create_dns_query(hostname):
    """Create a DNS query message.

    Args:
        hostname (string): Given by user through the command line.

    Returns:
        bytes: DNS query message in bytes.
    """
    print("Preparing DNS query..")
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
        print("Contacting DNS Server..")
        udp_sock.sendto(query, (server, port))
        print("Sending DNS query")
        udp_sock.settimeout(5)
        data = udp_sock.recv(1024)
        process_dns_response(query, data)
    finally:
        udp_sock.close()


def process_dns_response(query, response):
    """Function to print the DNS query and response

    Args:
        query (bytes): DNS query message
        response (bytes): DNS response message
    """
    print("Processing DNS response..")

    dns_response = DNSRecord.parse(response)
    dns_header = dns_response.header
    dns_question = dns_response.questions[0]
    dns_answer = dns_response.rr
    print(
        "----------------------------------------------------------------------------"
    )
    print(
        f"header.ID = {dns_header.id}\nheader.QR = {dns_header.qr}\n"
        f"header.OPCODE = {dns_header.opcode}\nheader.RD = {dns_header.rd}\n"
        f"header.QDCOUNT = {dns_header.q}"
    )
    print(
        f"question.QNAME = {dns_question.qname}\nquestion.QTYPE = {dns_question.qtype}\n"
        f"question.QCLASS = {dns_question.qclass}"
    )
    print(
        f"answer.NAME = {dns_answer[0].rname}\nanswer.TYPE = {dns_answer[0].rtype}\n"
        f"answer.CLASS = {dns_answer[0].rclass}\nanswer.TTL = {dns_answer[0].ttl}\n"
        f"answer.RDATA = {dns_answer[0].rdata}"
    )
    print(
        "----------------------------------------------------------------------------"
    )


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
