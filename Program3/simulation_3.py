'''
Created on Oct 12, 2016
@author: mwittie
'''
import network_3
import link_3
import threading
from time import sleep

##configuration parameters
router_queue_size = 0 #0 means unlimited
simulation_time = 5 #give the network sufficient time to transfer all packets before quitting

if __name__ == '__main__':
    object_L = [] #keeps track of objects, so we can kill their threads

    #-------------------------
    #create network hosts 1-4
    host1 = network_3.Host(1)
    object_L.append(host1)
    host2 = network_3.Host(2)
    object_L.append(host2)
    host3 = network_3.Host(3)
    object_L.append(host3)
    host4 = network_3.Host(4)
    object_L.append(host4)
    #-------------------------
    #Create network routers A-D
    router_a = network_3.Router(name='A', intf_count=1, max_queue_size=router_queue_size)
    object_L.append(router_a)
    router_b = network_3.Router(name='B', intf_count=1, max_queue_size=router_queue_size)
    object_L.append(router_b)
    router_c = network_3.Router(name='C', intf_count=1, max_queue_size=router_queue_size)
    object_L.append(router_c)
    router_d = network_3.Router(name='D', intf_count=1, max_queue_size=router_queue_size)
    object_L.append(router_d)
    #-------------------------
    #create a Link Layer to keep track of links between network nodes
    link_layer = link_3.LinkLayer()
    object_L.append(link_layer)

    #add all the links
    #link parameters: from_node, from_intf_num, to_node, to_intf_num, mtu
    #Linklayer for Host1
    link_layer.add_link(link_3.Link(host1, 0, router_a, 0, 50))
    link_layer.add_link(link_3.Link(router_a, 0, router_b, 0, 50))
    link_layer.add_link(link_3.Link(router_b, 0, router_d, 0, 50))
    link_layer.add_link(link_3.Link(router_d, 0, host3, 0, 50))

    #Linklayer for Host2
    '''Do we need new interfaces per link layer?'''
    link_layer.add_link(link_3.Link(host2, 0, router_a, 0, 50))
    link_layer.add_link(link_3.Link(router_a, 0, router_c, 0, 50))
    link_layer.add_link(link_3.Link(router_c, 0, router_d, 0, 50))
    link_layer.add_link(link_3.Link(router_d, 0, host4, 0, 50))

    #start all the objects
    thread_L = []
    thread_L.append(threading.Thread(name=host1.__str__(), target=host1.run))
    thread_L.append(threading.Thread(name=host2.__str__(), target=host2.run))
    thread_L.append(threading.Thread(name=host3.__str__(), target=host3.run))
    thread_L.append(threading.Thread(name=host4.__str__(), target=host4.run))

    thread_L.append(threading.Thread(name=router_a.__str__(), target=router_a.run))
    thread_L.append(threading.Thread(name=router_b.__str__(), target=router_b.run))
    thread_L.append(threading.Thread(name=router_c.__str__(), target=router_c.run))
    thread_L.append(threading.Thread(name=router_d.__str__(), target=router_d.run))

    thread_L.append(threading.Thread(name="Network", target=link_layer.run))

    for t in thread_L:
        t.start()

    #create some send events
    data_S = "I will build a great, great wall on our"
    data_S2 = "Sometimes I'll start a sentence and I don't even know where it's going. I just hope I find it along the way."

    host1.udt_send(3, data_S)
    host2.udt_send(4, data_S)

    #give the network sufficient time to transfer all packets before quitting
    sleep(simulation_time)

    #join all threads
    for o in object_L:
        o.stop = True
    for t in thread_L:
        t.join()

    print("All simulation threads joined")



# writes to host periodically
