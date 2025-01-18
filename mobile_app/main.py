from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.graphics.texture import Texture
import websockets
import asyncio
import json
import base64
from io import BytesIO
from PIL import Image as PILImage
import threading

class ScreenViewerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Server URL input
        self.url_input = TextInput(
            text='ws://192.168.1.1:8765',
            multiline=False,
            size_hint_y=None,
            height=50
        )
        self.layout.add_widget(self.url_input)
        
        # Connect/Disconnect button
        self.connect_button = Button(
            text='Connect',
            size_hint_y=None,
            height=50
        )
        self.connect_button.bind(on_press=self.toggle_connection)
        self.layout.add_widget(self.connect_button)
        
        # Status label
        self.status_label = Label(
            text='Disconnected',
            size_hint_y=None,
            height=30
        )
        self.layout.add_widget(self.status_label)
        
        # Screen display
        self.image_widget = Image()
        self.layout.add_widget(self.image_widget)
        
        # Initialize websocket variables
        self.websocket = None
        self.connected = False
        self.ws_thread = None
        
        return self.layout
    
    def toggle_connection(self, instance):
        if not self.connected:
            # Start connection
            self.ws_thread = threading.Thread(target=self.run_async_connection)
            self.ws_thread.daemon = True
            self.ws_thread.start()
            self.connect_button.text = 'Disconnect'
            self.status_label.text = 'Connecting...'
        else:
            # Disconnect
            self.connected = False
            if self.websocket:
                asyncio.run(self.websocket.close())
            self.connect_button.text = 'Connect'
            self.status_label.text = 'Disconnected'
    
    def run_async_connection(self):
        asyncio.run(self.connect_to_server())
    
    async def connect_to_server(self):
        try:
            self.websocket = await websockets.connect(self.url_input.text)
            self.connected = True
            self.status_label.text = 'Connected'
            await self.receive_frames()
        except Exception as e:
            self.status_label.text = f'Error: {str(e)}'
            self.connect_button.text = 'Connect'
            self.connected = False
    
    async def receive_frames(self):
        try:
            while self.connected:
                message = await self.websocket.recv()
                data = json.loads(message)
                if data['type'] == 'frame':
                    # Decode base64 image
                    img_data = base64.b64decode(data['data'])
                    # Convert to PIL Image
                    img = PILImage.open(BytesIO(img_data))
                    # Convert to Kivy texture
                    texture = self.pil_to_texture(img)
                    # Update image widget
                    Clock.schedule_once(lambda dt: self.update_image(texture))
        except websockets.exceptions.ConnectionClosed:
            self.status_label.text = 'Connection closed'
            self.connect_button.text = 'Connect'
            self.connected = False
        except Exception as e:
            self.status_label.text = f'Error: {str(e)}'
            self.connect_button.text = 'Connect'
            self.connected = False
    
    def pil_to_texture(self, pil_image):
        raw_data = pil_image.tobytes()
        texture = Texture.create(size=pil_image.size)
        texture.blit_buffer(raw_data, colorfmt='rgb', bufferfmt='ubyte')
        return texture
    
    def update_image(self, texture):
        self.image_widget.texture = texture

if __name__ == '__main__':
    ScreenViewerApp().run()
