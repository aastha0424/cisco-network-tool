import time
from multiprocessing import Queue
from .device import Router

class SimulationEngine:
    def __init__(self, graph):
        self.graph = graph
        self.devices = {}
        # Each device gets one incoming queue, identified by its name
        self.incoming_queues = {node_id: Queue() for node_id in graph.nodes()}

    def setup(self):
        """Sets up devices with one incoming queue and a dict of outgoing queues."""
        for node_id, node_data in self.graph.nodes(data=True):
            # A device's outgoing links are the incoming queues of its neighbors
            outgoing_links = {
                neighbor: self.incoming_queues[neighbor] 
                for neighbor in self.graph.neighbors(node_id)
            }
            
            # Each device gets its own dedicated incoming queue
            incoming_queue = self.incoming_queues[node_id]
            
            self.devices[node_id] = Router(node_id, node_data, incoming_queue, outgoing_links)

    def run(self):
        self.setup()
        for device in self.devices.values():
            device.start()

        print("--- Network settling, please wait 2 seconds... ---")
        time.sleep(2)
        
        print("\n--- Simulation Running. Type 'help' for commands. ---")
        try:
            while True:
                cmd = input("> ").strip().lower().split()
                if not cmd: continue

                if cmd[0] == 'exit': break
                elif cmd[0] == 'pause': self.pause()
                elif cmd[0] == 'resume': self.resume()
                elif cmd[0] == 'ping' and len(cmd) == 3: self.ping(cmd[1].upper(), cmd[2].upper())
                elif cmd[0] == 'fail' and len(cmd) == 4 and cmd[1] == 'link': self.fail_link(cmd[2].upper(), cmd[3].upper())
                elif cmd[0] == 'help': print("Commands: ping <src> <dst>, fail link <d1> <d2>, pause, resume, exit")
                else: print("Unknown command.")
        finally:
            self.stop()

    def ping(self, source, dest):
        """Initiates a ping from the engine by placing it in the source's IN-queue."""
        if source in self.devices:
            print(f"--- Sending PING from {source} to {dest} ---")
            packet = {'type': 'PING_REQUEST', 'source': source, 'destination': dest, 'sender': 'ENGINE'}
            self.incoming_queues[source].put(packet)
        else:
            print(f"Error: Source device {source} not found.")

    def fail_link(self, d1, d2):
        print(f"--- Simulating link failure between {d1} and {d2} ---")
        # To fail a link, we tell each device to remove the other from its outgoing links
        if d1 in self.devices and d2 in self.devices[d1].outgoing_links:
            del self.devices[d1].outgoing_links[d2]
        if d2 in self.devices and d1 in self.devices[d2].outgoing_links:
            del self.devices[d2].outgoing_links[d1]

    def pause(self):
        print("--- Pausing simulation... ---")
        for device in self.devices.values(): device.pause_event.clear()

    def resume(self):
        print("--- Resuming simulation... ---")
        for device in self.devices.values(): device.pause_event.set()

    def stop(self):
        print("--- Stopping simulation... ---")
        for device in self.devices.values(): device.stop()
        for device in self.devices.values(): device.join()
        print("--- Simulation Stopped ---")