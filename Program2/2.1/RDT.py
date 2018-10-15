import Network
import argparse
from time import sleep
import hashlib


class Packet:
    ## the number of bytes used to store packet length
    seq_num_S_length = 10
    length_S_length = 10
    ## length of md5 checksum in hex
    checksum_length = 32

    def __init__(self, seq_num, msg_S):
        self.seq_num = seq_num
        self.msg_S = msg_S

    @classmethod
    def from_byte_S(self, byte_S):
        if Packet.corrupt(byte_S):
            raise RuntimeError('Cannot initialize Packet: byte_S is corrupt')
        #extract the fields
        seq_num = int(byte_S[Packet.length_S_length : Packet.length_S_length+Packet.seq_num_S_length])
        msg_S = byte_S[Packet.length_S_length+Packet.seq_num_S_length+Packet.checksum_length :]
        return self(seq_num, msg_S)


    def get_byte_S(self):
        #convert sequence number of a byte field of seq_num_S_length bytes
        seq_num_S = str(self.seq_num).zfill(self.seq_num_S_length)
        #convert length to a byte field of length_S_length bytes
        length_S = str(self.length_S_length + len(seq_num_S) + self.checksum_length + len(self.msg_S)).zfill(self.length_S_length)
        #compute the checksum
        checksum = hashlib.md5((length_S+seq_num_S+self.msg_S).encode('utf-8'))
        checksum_S = checksum.hexdigest()
        #compile into a string
        return length_S + seq_num_S + checksum_S + self.msg_S


    @staticmethod
    def corrupt(byte_S):
        #extract the fields
        length_S = byte_S[0:Packet.length_S_length]
        seq_num_S = byte_S[Packet.length_S_length : Packet.seq_num_S_length+Packet.seq_num_S_length]
        checksum_S = byte_S[Packet.seq_num_S_length+Packet.seq_num_S_length : Packet.seq_num_S_length+Packet.length_S_length+Packet.checksum_length]
        msg_S = byte_S[Packet.seq_num_S_length+Packet.seq_num_S_length+Packet.checksum_length :]

        #compute the checksum locally
        checksum = hashlib.md5(str(length_S+seq_num_S+msg_S).encode('utf-8'))
        computed_checksum_S = checksum.hexdigest()
        #and check if the same
        return checksum_S != computed_checksum_S


class RDT:
    ## latest sequence number used in a packet
    seq_num = 1
    ## buffer of bytes read from network
    byte_buffer = ''

    def __init__(self, role_S, server_S, port):
        self.network = Network.NetworkLayer(role_S, server_S, port)

    def disconnect(self):
        self.network.disconnect()

    def rdt_1_0_send(self, msg_S):
        p = Packet(self.seq_num, msg_S)
        self.seq_num += 1
        self.network.udt_send(p.get_byte_S())

    def rdt_1_0_receive(self):
        ret_S = None
        byte_S = self.network.udt_receive()
        self.byte_buffer += byte_S
        #keep extracting packets - if reordered, could get more than one
        while True:
            #check if we have received enough bytes
            if(len(self.byte_buffer) < Packet.length_S_length):
                return ret_S #not enough bytes to read packet length
            #extract length of packet
            length = int(self.byte_buffer[:Packet.length_S_length])
            print(length)
            if len(self.byte_buffer) < length:
                return ret_S #not enough bytes to read the whole packet
            #create packet from buffer content and add to return string
            p = Packet.from_byte_S(self.byte_buffer[0:length])
            ret_S = p.msg_S if (ret_S is None) else ret_S + p.msg_S
            #remove the packet bytes from the buffer
            self.byte_buffer = self.byte_buffer[length:]
            #if this was the last packet, will return on the next iteration


    def rdt_2_1_send(self, msg_S):
        send_p = Packet(self.seq_num, msg_S)                                    #copied from rdt_1_0_send
        attempt = 0
        while True:                                                             #until we break due to packet being successfully sent and a ACK being recieved
            attempt += 1
            print("SENDING ATTEMPT: ", attempt)
            self.network.udt_send(send_p.get_byte_S())                          #send the current packet until a ack response is received
            recieved_p = ''                                                     #create a recieved packet

            while recieved_p == '':                                             #while the client hasn't received a response, listen to receive
                recieved_p = self.network.udt_receive()

            response_length = int(recieved_p[:Packet.length_S_length])          #save the length of the packet stored in the packet's length_S_length value
            self.byte_buffer = recieved_p[response_length:]                     #put the packet in the buffer

            if Packet.corrupt(recieved_p[:response_length]):                    #check if packet is corrupt, if it is, reset buffer as there isn't a valid packet in it
                self.byte_buffer = ''
                print("RECEIVED PACKET CORRUPTED ON ATTEMPT: ", attempt, "| RESENDING")
            else:
                responding_packet = Packet.from_byte_S(recieved_p[:response_length])    #if packet isn't corrupt, create a new responding packet made of the recieved packet's bytes and length
                if responding_packet.seq_num < self.seq_num:                    #if the received packets sequence number is lower than selfs, then it's behind and send an acknowledgement
                    ack_packet = Packet(responding_packet.seq_num, '1')
                    self.network.udt_send(ack_packet.get_byte_S())
                    print("BEHIND SEQ_NUM, ACK SENT")
                elif responding_packet.msg_S == "1":                            #if the recieved packets message is a 1, that means it's acknowledged and receieved correctly
                    self.seq_num += 1                                           #increment the seq_num to move onto the next message/packet to be sent
                    print("ACK RECEIVED")
                    break                                                       #break from loop. note: this is the single case the program can break from the "while True" loop
                elif responding_packet.msg_S == "0":                            #if the recieved packets message is a 0, that means it was not acknowledged as valid
                    self.byte_buffer = ''                                       #reset the buffer to receive a new version of ack / nak after sending the packet a second time
                    print("NAK RECEIVED")
                    continue

    def rdt_2_1_receive(self):
        ret_S = None                                                            #copied from rdt_1_0_recieve
        byte_S = self.network.udt_receive()                                     #copied from rdt_1_0_recieve
        self.byte_buffer += byte_S                                              #copied from rdt_1_0_recieve
        current_sequence = self.seq_num                                         #set the current sequence number to keep track of whether the server or client is behind on ack / nak and sending
        while current_sequence == self.seq_num:
            if len(self.byte_buffer) < Packet.length_S_length:                  # if the length of the packet reseived (added to buffer) is less than correct length, break
                break

            recieved_length = int(self.byte_buffer[:Packet.length_S_length])    #save length of received packet for later use

            if len(self.byte_buffer) < recieved_length:                         #Make sure that the buffer is correctly storing the received packet
                break

            if Packet.corrupt(self.byte_buffer):                                #check if packet is corrupt. If it is, send nak back
                nak_packet = Packet(self.seq_num, '0')                          #use the current sequence number (since it hasn't been incremented, that means a packet hasn't been received) and 0 (nak)
                self.network.udt_send(nak_packet.get_byte_S())
                print("RECEIVED PACKET CORRUPTED. NAKE SENT")
            else:                                                               #if packet isn't corrupt, send ack based on what the seq number of the received packet is
                responding_packet = Packet.from_byte_S(self.byte_buffer[:recieved_length])      #create a "responding packet" that contains the packets bytes
                if responding_packet.msg_S != '1' and responding_packet.msg_S != '0':
                    if responding_packet.seq_num < self.seq_num:                    #if the responding packet has a sequence number less than the self's sequence number, it's a duplicate and send an ack
                        ack_packet = Packet(responding_packet.seq_num, '1')
                        self.network.udt_send(ack_packet.get_byte_S())
                        print("SENT ACK PACKET")
                    elif responding_packet.seq_num == self.seq_num:                 #if the responding packet sequence number is equal to self's sequence number, it's the correct packet, send an ack
                        ack_packet = Packet(responding_packet.seq_num, '1')
                        self.network.udt_send(ack_packet.get_byte_S())
                        self.seq_num += 1
                        print("SENT ACK PACKET")
                if ret_S is None:                                               #If no packet has been received prior, set the return string to the packets message
                    ret_S = responding_packet.msg_S
                else:                                                           #If it isn't the first packet to be received, increment the return string with the most recent packets message
                    ret_S += responding_packet.msg_S
            self.byte_buffer = self.byte_buffer[recieved_length:]               #reset the buffer for the next packet
        return ret_S

    def rdt_3_0_send(self, msg_S):
        pass

    def rdt_3_0_receive(self):
        pass


if __name__ == '__main__':
    parser =  argparse.ArgumentParser(description='RDT implementation.')
    parser.add_argument('role', help='Role is either client or server.', choices=['client', 'server'])
    parser.add_argument('server', help='Server.')
    parser.add_argument('port', help='Port.', type=int)
    args = parser.parse_args()

    rdt = RDT(args.role, args.server, args.port)
    if args.role == 'client':
        rdt.rdt_2_1_send('MSG_FROM_CLIENT')
        sleep(2)
        print(rdt.rdt_2_1_receive())
        rdt.disconnect()


    else:
        sleep(1)
        print(rdt.rdt_2_1_receive())
        rdt.rdt_2_1_send('MSG_FROM_SERVER')
        rdt.disconnect()
