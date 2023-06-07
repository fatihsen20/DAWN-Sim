import sys
sys.path.insert(1, '.')
from source import DawnSimVis
import time

ROOT = 0
# neighbours = {
#     0: [1],
#     1: [0, 2, 3],
#     2: [1, 3, 5],
#     3: [1, 2, 4, 5],
#     4: [3, 5],
#     5: [2, 3, 4]
# }

###########################################################
# Override required functions
class Node(DawnSimVis.BaseNode):
    
    ###################
    def init(self):
        self.parent = None
        self.used = {}
        self.neighbours = neighbours[self.id]
    ###################
    def run(self):
        if self.id == ROOT:
            packet = {'type': "TOKEN", 'source': ROOT}
            self.send(DawnSimVis.BROADCAST_ADDR, packet)
            print("Tarry's Algorithm is started!")
            print("-"*30)
            self.parent = None
            self.change_color(1,0,0)
            time.sleep(1)
        
    ###################
    def on_receive(self, pck):
        if self.parent is None:
            self.parent = pck["source"]
            self.change_color(0,0,1)
        i = 0
        while i < len(self.neighbours):
            if self.neighbours[i] not in self.used and self.neighbours[i] != self.parent:
                self.used[self.neighbours[i]] = True
                self.send(self.neighbours[i], {'type': "TOKEN", 'source': self.id})
                print(f"Sending token from {self.id} --> {self.neighbours[i]}")
                self.change_color(0,0,1)
                time.sleep(1)
                break
            i += 1
        
        if i == len(self.neighbours):
            if self.id != ROOT:
                self.used[self.parent] = True
                self.send(self.parent, {'type': "TOKEN", 'source': self.id})
                print(f"Sending token from {self.id} --> {self.parent}")
                if self.parent == ROOT:
                    print("-"*30)
                    print("Tarry's Algorithm is finished!")
                self.change_color(0,0,1)
                time.sleep(1)
            
# create a Simulator object
sim = DawnSimVis.Simulator(
    duration=100,
    timescale=1,
    visual=True,
    terrain_size=(650, 650),
    title="Tarry's Algorithm")

# add nodes here
sim.add_node(Node, (50,50), 75)
sim.add_node(Node, (50,100), 75)
sim.add_node(Node, (50,150), 75)
sim.add_node(Node, (100,150), 75)
sim.add_node(Node, (150,200), 75)
sim.add_node(Node, (100,200), 75)

def find_neighbours():
    neighbours = {}
    for node in sim.nodes:
        neighbours[node.id] = []
        for other in sim.nodes:
            if node.id != other.id:
                x_diff = abs(node.pos[0] - other.pos[0])
                y_diff = abs(node.pos[1] - other.pos[1])
                if x_diff <= node.tx_range and y_diff <= node.tx_range:
                    neighbours[node.id].append(other.id)
    return neighbours

neighbours = find_neighbours()
# start the simulation
sim.run()