import sys
import random
sys.path.insert(1, '.')
from source import DawnSimVis
import time 

ROOT = 0
###########################################################
# Override required functions
class Node(DawnSimVis.BaseNode):

    ###################
    def init(self):
        self.parent = None
        self.others = set()
        self.neighbours = set()
        self.neighbour_count = 0
        self.received_count = 0

    ###################
    def run(self):
        packet = {'type': "DISCOVER", 'source': self.id}
        self.send(DawnSimVis.BROADCAST_ADDR, packet)

        if self.id == ROOT:
            self.set_timer(1, self.send_probe)
    
    def send_probe(self):
        self.change_color(1,0,0)
        packet = {'type': "PROBE", 'source': self.id}
        self.send(DawnSimVis.BROADCAST_ADDR, packet)

    ###################
    def on_receive(self, pck):
        if pck['type'] == "DISCOVER":
            self.neighbours.add(pck['source'])
            self.neighbour_count += 1
            print(self.id, "received token from", pck['source'])
        elif pck['type'] == "PROBE":
            if self.parent is None and self.id != ROOT:
                self.parent = pck['source']
                self.send(DawnSimVis.BROADCAST_ADDR, {'type': "PROBE", 'source': self.id})
                self.change_color(0,0,1)
                if self.neighbour_count == 1:
                    self.send(self.parent, {'type': "ACK", 'source': self.id})
                    self.scene.addlink(self.parent, self.id, "prev")
            elif self.parent is not None:
                self.send(pck['source'], {'type': "REJECT", 'source': self.id})
        
        elif pck['type'] == "REJECT":
            self.received_count += 1
            self.others.add(pck['source'])
            if self.received_count == self.neighbour_count -1:
                self.send(self.parent, {'type': "ACK", 'source': self.id})
        
        elif pck['type'] == "ACK":
            self.received_count += 1
            self.others.add(pck['source'])
            if self.received_count == self.neighbour_count -1 and self.parent is not None:
                self.send(self.parent, {'type': "ACK", 'source': self.id})
                self.scene.addlink(self.parent, self.id, "prev")

        if self.received_count == self.neighbour_count-1 and self.id == ROOT:
            print("Distributed Spanning Tree With Termination Detection is Completed.")

def create_network():
    # place nodes over 100x100 grids
    for i in range(0, 10):
        sim.add_node(Node, (random.randint(0, 250) + 10, random.randint(0, 250)),100)


# create a Simulator object
sim = DawnSimVis.Simulator(
    duration=100,
    timescale=1,
    visual=True,
    terrain_size=(650, 650),
    title='Blank Template')

# add nodes here
create_network()
# start the simulation
sim.run()
