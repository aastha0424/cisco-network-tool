import threading
import time

NEIGHBOR_TIMEOUT = 5  # Time before a silent neighbor is considered down
HELLO_INTERVAL = 2    # Time between sending HELLO packets

class Router(threading.Thread):
    def __init__(self, device_id, config, incoming_queue, outgoing_links):
        super().__init__()
        self.device_id = device_id
        self.config = config
        self.incoming_queue = incoming_queue
        self.outgoing_links = outgoing_links
        
        self.is_running = True
        self.pause_event = threading.Event()
        self.pause_event.set()
        
        self.routing_table = {self.device_id: (None, 0)}
        self.neighbor_liveness = {}
        self.last_check_time = time.time()
        self.last_hello_time = 0 # Initialize to ensure first HELLO is sent immediately

    def run(self):
        print(f"[{self.device_id}] Booting up...")

        while self.is_running:
            self.pause_event.wait()
            
            # --- THIS IS THE FIX ---
            # Periodically send out HELLO packets to all neighbors
            if time.time() - self.last_hello_time > HELLO_INTERVAL:
                self._send_hello_packets()
                self.last_hello_time = time.time()

            # Check for incoming packets
            try:
                if not self.incoming_queue.empty():
                    packet = self.incoming_queue.get()
                    self._process_packet(packet)
            except (OSError, ValueError):
                pass
            
            # Periodically check if neighbors have timed out
            if time.time() - self.last_check_time > NEIGHBOR_TIMEOUT / 2:
                self._check_neighbor_liveness()
                self.last_check_time = time.time()

            time.sleep(0.1)

    def stop(self):
        self.is_running = False

    def _check_neighbor_liveness(self):
        timed_out_neighbors = []
        # Use a copy of the keys to avoid issues when deleting during iteration
        for neighbor in list(self.neighbor_liveness.keys()):
            if time.time() - self.neighbor_liveness[neighbor] > NEIGHBOR_TIMEOUT:
                timed_out_neighbors.append(neighbor)
        
        for neighbor in timed_out_neighbors:
            print(f"[{self.device_id}] Link to {neighbor} timed out. Removing route.")
            if neighbor in self.routing_table: del self.routing_table[neighbor]
            if neighbor in self.neighbor_liveness: del self.neighbor_liveness[neighbor]
            if neighbor in self.outgoing_links: del self.outgoing_links[neighbor]

    def _send_hello_packets(self):
        """Sends a HELLO packet to all current neighbors."""
        for neighbor_queue in self.outgoing_links.values():
            try:
                neighbor_queue.put({'type': 'OSPF_HELLO', 'source': self.device_id})
            except (OSError, ValueError): # This can happen if a link was just failed
                pass

    def _process_packet(self, packet):
        ptype = packet.get('type')
        source = packet.get('source')

        if ptype == 'OSPF_HELLO':
            if source == self.device_id: return
            # Always update the liveness timer when we hear from a neighbor
            self.neighbor_liveness[source] = time.time()
            if source not in self.routing_table:
                print(f"[{self.device_id}] Established link with {source}")
                self.routing_table[source] = (source, 1)

        elif ptype == 'PING_REQUEST':
            destination = packet.get('destination')
            if destination == self.device_id:
                print(f"[{self.device_id}] Received PING from {source}. Sending reply.")
                reply = {'type': 'PING_REPLY', 'source': self.device_id, 'destination': source}
                if source in self.routing_table:
                    next_hop, _ = self.routing_table[source]
                    if next_hop in self.outgoing_links:
                        self.outgoing_links[next_hop].put(reply)
            else:
                if destination in self.routing_table:
                    next_hop, _ = self.routing_table[destination]
                    if next_hop in self.outgoing_links:
                        print(f"[{self.device_id}] Forwarding PING for {destination} via {next_hop}")
                        self.outgoing_links[next_hop].put(packet)
                else:
                    print(f"[{self.device_id}] No route to {destination}, dropping PING.")

        elif ptype == 'PING_REPLY':
            print(f"[{self.device_id}] Successfully received PING_REPLY from {source}")