# ***dns-client***

CS455 dns client project. Implement a DNS client in order to query a DNS server for domain name to IP address. 
Reads hostname given by user when running the program and prepare a query message that adheres to DNS protocol specifications. Creates a UDP socket connection to the server and send the DNS query message. Receive the response from the DNS server, process the response, and extract the necessary information to display to the user on the command line.

## ***Requirements***

```
pip install dnslib
```
* This DNS client uses the python dnslib in order to process the DNS response message
* To view more information about this library: https://pypi.org/project/dnslib/

## ***How to run***

```bash
$ ./btal-dns-client.py <insert url here>

$ python3 btal-dns-client.py <insert url here>
```

## ***Examples***

![example 1][example]
![example 2][example2]
![example 3][example3]

## ***Acknowledgements***

Professor Maha Shamseddine


[example]: ./pictures/example1.png
[example2]: ./pictures/example2.png
[example3]: ./pictures/example3.png