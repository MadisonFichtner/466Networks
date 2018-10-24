'''
Created on Oct 12, 2016
@author: mwittie
'''
import queue
import threading


## wrapper class for a queue of packets
class Interface:
    ## @param maxsize - the maximum size of the queue storing packets
    def __init__(self, maxsize=0):
        self.queue = queue.Queue(maxsize);
        self.mtu = None

    ##get packet from the queue interface
    def get(self):
        try:
            return self.queue.get(False)
        except queue.Empty:
            return None

    ##put the packet into the interface queue
    # @param pkt - Packet to be inserted into the queue
    # @param block - if True, block until room in queue, if False may throw queue.Full exception
    def put(self, pkt, block=False):
        self.queue.put(pkt, block)


## Implements a network layer packet (different from the RDT packet
# from programming assignment 2).
# NOTE: This class will need to be extended to for the packet to include
# the fields necessary for the completion of this assignment.
class NetworkPacket:
    ## packet encoding lengths
    #address length is the first 5 numbers
    dst_addr_S_length = 5
    #the flag indicating whether the packet is segmented is the 6th number (pkt_S[5])
    seg_flag_S_length = 1
    #the flag indicating the offset, or the packet ID is 2 numbers long, found at pkt_S[6:7]
    offset_S_length = 2

    ##@param dst_addr: address of the destination host
    # @param data_S: packet payload
    def __init__(self, dst_addr, seg_flag, offset, data_S):
        self.dst_addr = dst_addr
        self.data_S = data_S
        self.seg_flag = seg_flag
        self.offset = offset

    ## called when printing the object
    def __str__(self):
        return self.to_byte_S()

    ## convert packet to a byte string for transmission over links
    def to_byte_S(self):
        byte_S = str(self.dst_addr).zfill(self.dst_addr_S_length)
        byte_S += str(self.seg_flag).zfill(self.seg_flag_S_length)
        byte_S += str(self.offset).zfill(self.offset_S_length)
        byte_S += self.data_S
        return byte_S

    ## extract a packet object from a byte string
    # @param byte_S: byte string representation of the packet
    @classmethod
    def from_byte_S(self, byte_S):
        dst_addr = int(byte_S[0 : NetworkPacket.dst_addr_S_length])
        seg_flag = int(byte_S[NetworkPacket.dst_addr_S_length : NetworkPacket.dst_addr_S_length + NetworkPacket.seg_flag_S_length])
        offset = int(byte_S[NetworkPacket.dst_addr_S_length + NetworkPacket.seg_flag_S_length : NetworkPacket.dst_addr_S_length + NetworkPacket.seg_flag_S_length + NetworkPacket.offset_S_length])
        data_S = byte_S[NetworkPacket.dst_addr_S_length + NetworkPacket.seg_flag_S_length + NetworkPacket.offset_S_length:]
        return self(dst_addr, seg_flag, offset, data_S)


## Implements a network host for receiving and transmitting data
class Host:
    ##@param addr: address of this node represented as an integer
    def __init__(self, addr):
        self.addr = addr
        self.in_intf_L = [Interface()]
        self.out_intf_L = [Interface()]
        self.stop = False #for thread termination
        self.packet_id = 10

    ## called when printing the object
    def __str__(self):
        return 'Host_%s' % (self.addr)

    ## create a packet and enqueue for transmission
    # @param dst_addr: destination address for the packet
    # @param data_S: data being transmitted to the network layer
    def udt_send(self, dst_addr, data_S):
        if len(data_S) > self.out_intf_L[0].mtu:                                #packet is bigger than max transmission size
            length = self.out_intf_L[0].mtu - 8                                #the addresses length is 8, so subtract that from mtu
            if len(data_S) % self.out_intf_L[0].mtu != 0:
                num_packets = int(len(data_S) / self.out_intf_L[0].mtu) + 1
            packets=[]
            for i in range(num_packets):
                if(i == num_packets-1):
                    packet = NetworkPacket(dst_addr, 2, self.packet_id, data_S[:length])
                    self.out_intf_L[0].put(packet.to_byte_S())
                    print('%s: sending packet "%s" on the out interface with mtu=%d' % (self, packet, self.out_intf_L[0].mtu))
                    data_S = data_S[length:]
                else:
                    packet = NetworkPacket(dst_addr, 1, self.packet_id, data_S[:length])
                    self.out_intf_L[0].put(packet.to_byte_S())
                    print('%s: sending packet "%s" on the out interface with mtu=%d' % (self, packet, self.out_intf_L[0].mtu))
                    data_S = data_S[length:]
            self.packet_id += 10
        else:
            p = NetworkPacket(dst_addr, 0, self.packet_id, data_S)
            self.out_intf_L[0].put(p.to_byte_S()) #send packets always enqueued successfully
            print('%s: sending packet "%s" on the out interface with mtu=%d' % (self, p, self.out_intf_L[0].mtu))

    def reconstruct(self, segments, id):
        original_data = ''
        for seg in segments:
            if seg[6:8] == id:
                original_data += seg[8:]
        return original_data

    reconstructed_packet = ''
    segments = []
    ## receive packet from the network layer                                    #TODO, will probably need another method for reconstructing packets as well
    def udt_receive(self):                                         #need to check if packet is a segment, and then reconstruct
        pkt_S = self.in_intf_L[0].get()
        if pkt_S is not None:
            print(pkt_S[5])
            current_packet_id = pkt_S[6:8]
            if pkt_S[5] == '1':               #check if packet is segment of a larger packet, if it is, add it to array
                self.segments.append(pkt_S)
            elif pkt_S[5] == '2':
                self.segments.append(pkt_S)
                original_data = self.reconstruct(self.segments, current_packet_id)
                original_packet = NetworkPacket(pkt_S[:5], 0, current_packet_id, original_data)
                print('%s: successfully reconstructed packet "%s" on the in interface' % (self, original_packet))
                #print(current_packet_id)
            print('%s: received packet "%s" on the in interface' % (self, pkt_S))


    ## thread target for the host to keep receiving data
    def run(self):
        print (threading.currentThread().getName() + ': Starting')
        while True:
            #receive data arriving to the in interface
            self.udt_receive()
            #terminate
            if(self.stop):
                print (threading.currentThread().getName() + ': Ending')
                return



## Implements a multi-interface router described in class
class Router:

    ##@param name: friendly router name for debugging
    # @param intf_count: the number of input and output interfaces
    # @param max_queue_size: max queue length (passed to Interface)
    def __init__(self, name, intf_count, max_queue_size):
        self.stop = False #for thread termination
        self.name = name
        #create a list of interfaces
        self.in_intf_L = [Interface(max_queue_size) for _ in range(intf_count)]
        self.out_intf_L = [Interface(max_queue_size) for _ in range(intf_count)]

    ## called when printing the object
    def __str__(self):
        return 'Router_%s' % (self.name)

    ## look through the content of incoming interfaces and forward to
    # appropriate outgoing interfaces
    def forward(self):                                                          #TODO implement the forwarding decision making down below where indicated. Right now it only forwards the first half of packet
        for i in range(len(self.in_intf_L)):                                    #TODO the segmentation. We need to split the two packets into segments here
            pkt_S = None                                                        #TODO need to check that the packet isn't over the max length (mtu), and if it is we need to segment further
            try:
                #get packet from interface i
                pkt_S = self.in_intf_L[i].get()
                #if packet exists make a forwarding decision
                if pkt_S is not None:
                    p = NetworkPacket.from_byte_S(pkt_S) #parse a packet out
                    # HERE you will need to implement a lookup into the
                    # forwarding table to find the appropriate outgoing interface
                    # for now we assume the outgoing interface is also i
                    self.out_intf_L[i].put(p.to_byte_S(), True)
                    print('%s: forwarding packet "%s" from interface %d to %d with mtu %d' \
                        % (self, p, i, i, self.out_intf_L[i].mtu))
            except queue.Full:
                print('%s: packet "%s" lost on interface %d' % (self, p, i))
                pass

    ## thread target for the host to keep forwarding data
    def run(self):
        print (threading.currentThread().getName() + ': Starting')
        while True:
            self.forward()
            if self.stop:
                print (threading.currentThread().getName() + ': Ending')
                return
