import socket
import sys
import struct
import random
import binascii


def create_dns_query(hostname):
    # Header
    header_row_0 = random.randint(0, 65535)
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

    parts = hostname.split(".")
    encoded_parts = [struct.pack("!B", len(parts)) + part.encode() for part in parts]
    encoded_domain = b"".join(encoded_parts) + b"\x00"

    # Combining header and question to form DNS query message.
    question = encoded_domain + struct.pack("!HH", qtype, 1)
    dns_message = header + question

    return dns_message


# Error checking for command line arguments

if len(sys.argv) == 1:
    print(
        "\nPlease include hostname to prepare a DNS query\n\
Example input: btal-dns-client.py gmu.edu"
    )
elif len(sys.argv) > 2:
    print(
        "\nPlease include only 1 hostname to prepare a DNS query.\n\
Example input: btal-dns-client.py gmu.edu"
    )


dns_server = "8.8.8.8"
dns_port_number = 53

hostname = sys.argv[1]
header_row_0 = random.randint(0, 65535)
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
qtype = 1
parts = hostname.split(".")
hex_parts = []
for part in parts:
    hex_parts.append("".join(hex(ord(word))[2:] for word in part))
print(hex_parts)

encoded_parts = [struct.pack("!B", len(part)) + part.encode() for part in parts]
# encoded_parts = [struct.pack("!B", len(part)) + part.encode() for part in hex_parts]
# print(encoded_parts)
encoded_domain = b"".join(encoded_parts) + b"\x00"
# print(encoded_domain)


question = encoded_domain + struct.pack("!HH", qtype, 1)
dns_message = header + question
print(dns_message)
