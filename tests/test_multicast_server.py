import select

from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, SO_REUSEPORT, IPPROTO_IP, IP_MULTICAST_TTL, inet_aton, INADDR_ANY, IP_ADD_MEMBERSHIP

import struct
from unittest import TestCase

from config import SERVER_GROUP_BASE_MULTICAST_ADDRESS, SERVER_GROUP_MULTICAST_PORT, BUFFER_SIZE


class TestRing:
    self = socket(AF_INET, SOCK_DGRAM)
    ttl = struct.pack('b', 1)
    self.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, ttl)
    self.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    self.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
    group = inet_aton(SERVER_GROUP_BASE_MULTICAST_ADDRESS)
    mreq = struct.pack('4sL', group, INADDR_ANY)
    self.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)
    self.bind(("", SERVER_GROUP_MULTICAST_PORT))

    while True:
        # Await an event on a readable socket descriptor
        (read, write, exception) = select.select([self], [], [])
        # Iterate through the tagged read descriptors
        for socket in read:
            # try:
            data, address = socket.recvfrom(BUFFER_SIZE)
            encoded_data = data.decode('utf-8')
            print("encoded_data")
            print(encoded_data)
