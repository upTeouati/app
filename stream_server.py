import asyncio
import websockets
import json
import cv2
import base64
from threading import Thread
import socket

class StreamServer:
    def __init__(self, host='0.0.0.0', port=8765):
        self.host = host
        self.port = port
        self.server = None
        self.clients = set()
        self.running = False
        self.server_thread = None
        
    def start(self):
        """Start the WebSocket server"""
        self.running = True
        self.server_thread = Thread(target=self._run_server)
        self.server_thread.start()
        
    def stop(self):
        """Stop the WebSocket server"""
        self.running = False
        # Cleanup will be handled in _run_server
        
    def get_connection_url(self):
        """Get the WebSocket URL for clients to connect to"""
        # Get local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return f"ws://{ip}:{self.port}"
        
    async def _handle_client(self, websocket, path):
        """Handle individual client connections"""
        self.clients.add(websocket)
        try:
            async for message in websocket:
                # Handle client messages if needed
                pass
        finally:
            self.clients.remove(websocket)
            
    def _run_server(self):
        """Run the WebSocket server in an event loop"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        start_server = websockets.serve(self._handle_client, self.host, self.port)
        self.server = loop.run_until_complete(start_server)
        
        try:
            loop.run_forever()
        finally:
            self.server.close()
            loop.run_until_complete(self.server.wait_closed())
            loop.close()
            
    async def broadcast_frame(self, frame):
        """Broadcast frame to all connected clients"""
        if not self.clients:
            return
            
        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        # Convert to base64
        frame_data = base64.b64encode(buffer).decode('utf-8')
        
        # Create message
        message = json.dumps({
            'type': 'frame',
            'data': frame_data
        })
        
        # Broadcast to all clients
        websockets.broadcast(self.clients, message)
