#!/usr/bin/env python

import socket
from twisted.internet import protocol, reactor, endpoints
from twisted.internet.protocol import DatagramProtocol

class ProxyServer(DatagramProtocol):

    def __init__(self, dst_addr):
        self.dst_addr = dst_addr
        self.clients = {}
        self.next_port = 3000

    def datagramReceived(self, data, src_addr):
        # print 'Received from %s:%d' % src_addr
        client = self.clients.get(src_addr, None)
        if client is None:
            print 'Accepted client'
            client = Client(src_addr, self.dst_addr, self)
            reactor.listenUDP(self.next_port, client)

            self.next_port += 1
            self.clients[src_addr] = client


        client.recvFromPlayer(data)

    def recvFromServer(self, data, dst_addr):
        #print 'Received from Server, sending to Client'
        self.transport.write(data, dst_addr)

class Client(DatagramProtocol):

    def __init__(self, src_addr, dst_addr, proxy_server):
        self.src_addr = src_addr
        self.dst_addr = dst_addr
        self.proxy_server = proxy_server
        self.port = None

    def datagramReceived(self, data, src_addr):
        self.proxy_server.recvFromServer(data, self.src_addr)

    def recvFromPlayer(self, data):
        #print 'Received from Client, sending to Server'
        self.transport.write(data, self.dst_addr)

# reactor.listenUDP(7777, ProxyServer(('74.91.122.184', 7777)))
reactor.listenUDP(7777, ProxyServer(('104.166.70.234', 7777)))
reactor.run()
