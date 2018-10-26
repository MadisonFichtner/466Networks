'''
Created on Oct 12, 2016
@author: mwittie
'''
import network_2
import link_2
import threading
from time import sleep

##configuration parameters
router_queue_size = 0 #0 means unlimited
simulation_time = 5 #give the network sufficient time to transfer all packets before quitting

if __name__ == '__main__':
    object_L = [] #keeps track of objects, so we can kill their threads

    #-------------------------
    #create network hosts 1-4
    host1 = network_2.Host(1)
    object_L.append(host1)
    host2 = network_2.Host(2)
    object_L.append(host2)
    host3 = network_2.Host(2)
    object_L.append(host3)
    host4 = network_2.Host(2)
    object_L.append(host4)
    #-------------------------
    #Create network routers A-D
    router_a = network_2.Router(name='A', intf_count=1, max_queue_size=router_queue_size)
    object_L.append(router_a)
    router_b = network_2.Router(name='B', intf_count=1, max_queue_size=router_queue_size)
    object_L.append(router_b)
    router_c = network_2.Router(name='C', intf_count=1, max_queue_size=router_queue_size)
    object_L.append(router_c)
    router_d = network_2.Router(name='D', intf_count=1, max_queue_size=router_queue_size)
    object_L.append(router_d)
    #-------------------------
    #create a Link Layer to keep track of links between network nodes
    link_layer1 = link_2.LinkLayer()
    object_L.append(link_layer1)

    link_layer2 = link_2.LinkLayer()
    object_L.append(link_layer2)


    #add all the links
    #link parameters: from_node, from_intf_num, to_node, to_intf_num, mtu
    #Linklayer for Host1
    link_layer1.add_link(link_2.Link(host1, 0, router_a, 0, 50))
    link_layer1.add_link(link_2.Link(router_a, 0, router_b, 0, 50))
    link_layer1.add_link(link_2.Link(router_b, 0, router_d, 0, 50))
    link_layer1.add_link(link_2.Link(router_d, 0, host3, 0, 50))

    #Linklayer for Host2
    link_layer2.add_link(link_2.Link(host2, 1, router_a, 1, 50))
    link_layer2.add_link(link_2.Link(router_a, 1, router_c, 1, 50))
    link_layer2.add_link(link_2.Link(router_c, 1, router_d, 1, 50))
    link_layer2.add_link(link_2.Link(router_d, 1, host4, 1, 50))

    #start all the objects
    thread_L = []
    thread_L.append(threading.Thread(name=client.__str__(), target=client.run))
    thread_L.append(threading.Thread(name=server.__str__(), target=server.run))
    thread_L.append(threading.Thread(name=router_a.__str__(), target=router_a.run))

    thread_L.append(threading.Thread(name="Network", target=link_layer.run))

    for t in thread_L:
        t.start()


    #create some send events
    data_S = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed quis massa tempus, lacinia dolor a, consequat diam. Donec non dolor vestibulum, pharetra nisl et, faucibus arcu. Ut condimentum, augue a condimentum imperdiet, mauris diam interdum sem, vel egestas justo nulla non turpis. Curabitur auctor metus eget suscipit aliquet. Praesent pulvinar ac tortor non tincidunt. Donec eu lorem sed dui euismod laoreet sit amet ut eros. Vestibulum ornare lorem ut lacus dignissim sagittis. Pellentesque ut aliquam purus, tempus porta ex. In hac habitasse platea dictumst. Curabitur ultrices massa sit amet sodales hendrerit. "
    #data_S2 = "Sometimes I'll start a sentence and I don't even know where it's going. I just hope I find it along the way."
    client.udt_send(2, data_S)
    #client.udt_send(2, data_S2)


    #give the network sufficient time to transfer all packets before quitting
    sleep(simulation_time)

    #join all threads
    for o in object_L:
        o.stop = True
    for t in thread_L:
        t.join()

    print("All simulation threads joined")



# writes to host periodically
