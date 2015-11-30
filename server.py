#!/usr/bin/env python

import socket
from twisted.internet import protocol, reactor, endpoints
from twisted.internet.protocol import DatagramProtocol
from twisted.internet.udp import Port

class ProxyServer(DatagramProtocol):

    def __init__(self, dst_addr):
        self.dst_addr = dst_addr
        self.clients = {}

    def datagramReceived(self, data, src_addr):
        # print 'Received from %s:%d' % src_addr
        client = self.clients.get(src_addr, None)
        if client is None:
            client = Client(src_addr, self.dst_addr, self)
            self.clients[src_addr] = client

            p = reactor.listenUDP(0, client)
            print 'Accepted client, using port %d' % p._realPortNumber

        client.recvFromPlayer(data)

    def recvFromServer(self, data, dst_addr):
        #print 'Received from Server, sending to Client'
        self.transport.write(data, dst_addr)

class Client(DatagramProtocol):

    def __init__(self, src_addr, dst_addr, proxy_server):
        self.src_addr = src_addr
        self.dst_addr = dst_addr
        self.proxy_server = proxy_server

    def datagramReceived(self, data, src_addr):
        self.proxy_server.recvFromServer(data, self.src_addr)

    def recvFromPlayer(self, data):
        #print 'Received from Client, sending to Server'
        self.transport.write(data, self.dst_addr)

reactor.listenUDP(7777, ProxyServer(('104.166.70.234', 7777)))
reactor.listenUDP(7778, ProxyServer(('74.91.122.184', 7777)))
reactor.listenUDP(7779, ProxyServer(('192.223.31.8', 7777)))
reactor.run()
