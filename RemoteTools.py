from langchain.tools import BaseTool
from uuid import uuid4
from pydantic import BaseModel, Field, Extra
import requests

class BaseRemoteTool(BaseTool):
    url: str = Field(default='http://10.0.0.55:8080')

    def _send_cmd(self, cmd: str):
        return requests.post(f'{self.url}/run', json={'cmd': cmd}).json()

    class Config(BaseTool.Config):
        arbitrary_types_allowed = True
        extra = Extra.forbid

class BatteryStatusTool(BaseRemoteTool, BaseTool):
    name = 'Battery Status'
    description = (
        'Get the current battery status of the device.'
        'Useful for determining if the device is charging or not.'
        'Useful for getting the battery level.'
    )

    def _run(self):
        return self._send_cmd('termux-battery-status')
    
    async def _arun(self):
        return self._run()

class BrightnessTool(BaseRemoteTool, BaseTool):
    name = 'Brightness'
    description = (
        'Set the screen brightness.'
        'Useful for setting the screen brightness.'
        'Accepts an integer between 0 and 255 OR the string "auto".'
    )

    def _run(self, level: int = 'auto'):
        return self._send_cmd(f'termux-brightness {level}')

    async def _arun(self, level: int = 0):
        return self._run(level)

class PhotoTool(BaseRemoteTool, BaseTool):
    name = 'Take Photo'
    description = (
        'Take a photo with the device camera.'
        'Useful for taking a photo with the device camera.'
        'Accepts an optional integer camera id. Default is 0.'
    )

    def _run(self, camera_id: int = 0):
        fn = f'photo-{str(uuid4())}.png'
        resp = self._send_cmd(f'termux-camera-photo -c {camera_id} {fn}')
        return {'file': fn, 'response': resp}

    async def _arun(self, camera_id: int = 0):
        return self._run(camera_id)

class ClipboardGetTool(BaseRemoteTool, BaseTool):
    name = 'Clipboard Get'
    description = (
        'Get the current clipboard contents.'
        'Useful for getting the current clipboard contents.'
    )

    def _run(self):
        return self._send_cmd('termux-clipboard-get')

    async def _arun(self):
        return self._run()

class ClipboardSetTool(BaseRemoteTool, BaseTool):
    name = 'Clipboard Set'
    description = (
        'Set the current clipboard contents.'
        'Useful for setting the current clipboard contents.'
        'Accepts a string.'
    )

    def _run(self, text: str):
        return self._send_cmd(f'termux-clipboard-set {text}')

    async def _arun(self, text: str):
        return self._run(text)

class FingerprintTool(BaseRemoteTool, BaseTool):
    name = 'Fingerprint'
    description = (
        'Asks the user to scan their fingerprint.'
        'Useful for getting authentication from the device owner.'
    )

    def _run(self):
        return self._send_cmd('termux-fingerprint')

    async def _arun(self):
        return self._run()

class LocationTool(BaseRemoteTool, BaseTool):
    name = 'Location'
    description = (
        'Get the current location of the device.'
        'Useful for getting the current location of the device.'
    )

    def _run(self):
        return self._send_cmd('termux-location')

    async def _arun(self):
        return self._run()

class MediaPlayTool(BaseRemoteTool, BaseTool):
    name = 'Play Media'
    description = (
        'Play a media file.'
        'Useful for playing a media file.'
        'Accepts a string file path.'
    )

    def _run(self, path: str):
        return self._send_cmd(f'termux-media-player play {path}')

    async def _arun(self, path: str):
        return self._run(path)

class MediaPauseTool(BaseRemoteTool, BaseTool):
    name = 'Pause Media'
    description = (
        'Pause the currently playing media.'
        'Useful for pausing the currently playing media.'
    )

    def _run(self):
        return self._send_cmd('termux-media-player pause')

    async def _arun(self):
        return self._run()

class RecordMicTool(BaseRemoteTool, BaseTool):
    name = 'Record Microphone'
    description = (
        'Record audio from the device microphone.'
        'Useful for recording audio from the device microphone.'
        'Accepts an integer duration in seconds.'
        'Returns filename.'
    )

    def _run(self, duration: int):
        fn = f'record-{str(uuid4())}.mp3'
        resp = self._send_cmd(f'termux-microphone-record -d {duration} {fn}')
        return {'file': fn, 'response': resp}

    async def _arun(self, duration: int = 3):
        return self._run(duration)

class NotificationTool(BaseRemoteTool, BaseTool):
    name = 'Notification'
    description = (
        'Send a notification to the device.'
        'Useful for sending a notification to the device.'
        'Accepts a string title and a string message.'
    )

    def _run(self, title: str, message: str):
        return self._send_cmd(f'termux-notification -t {title} -c {message}')

    async def _arun(self, title: str, message: str):
        return self._run(title, message)

class ListNotificationsTool(BaseRemoteTool, BaseTool):
    name = 'List Notifications'
    description = (
        'List the current notifications on the device.'
        'Useful for listing the current notifications on the device.'
        'Returns a list of dicts.'
    )

    def _run(self):
        return self._send_cmd('termux-notification-list')

    async def _arun(self):
        return self._run()

class URLOpenerTool(BaseRemoteTool, BaseTool):
    name = 'Open URL'
    description = (
        'Open a URL in the default browser.'
        'Useful for opening a URL in the default browser.'
        'Accepts a string URL.'
    )

    def _run(self, url: str):
        return self._send_cmd(f'termux-open-url {url}')

    async def _arun(self, url: str):
        return self._run(url)

class TorchTool(BaseRemoteTool, BaseTool):
    name = 'Torch'
    description = (
        'Turn the device torch on or off.'
        'Useful for turning the device torch on or off.'
        'Accepts a string on or off.'
    )

    def _run(self, state: str):
        if not state in ('on', 'off'):
            return 'Error: argument must be "on" or "off"'
        return self._send_cmd(f'termux-torch {state}')

    async def _arun(self, state: str):
        return self._run(state)

class SpeakTool(BaseRemoteTool, BaseTool):
    name = 'Speak'
    description = (
        'Speak a string with TTS.'
        'Useful for speaking a string.'
        'Accepts a string.'
    )

    def _run(self, text: str):
        return self._send_cmd(f'termux-tts-speak {text}')

    async def _arun(self, text: str):
        return self._run(text)

class GetVolumeTool(BaseRemoteTool, BaseTool):
    name = 'Get Volume'
    description = (
        'Get the current volume.'
        'Useful for getting the current volume.'
        'Returns a dict.'
    )

    def _run(self):
        return self._send_cmd('termux-volume')

    async def _arun(self):
        return self._run()

class SetVolumeTool(BaseRemoteTool, BaseTool):
    name = 'Set Volume'
    description = (
        'Set the current volume.'
        'Useful for setting the current volume.'
        'Accepts a string type and an integer value.'
    )

    def _run(self, type: str, value: int):
        if not type in ('music', 'alarm', 'notification', 'ring'):
            return 'Error: type must be "music", "alarm", "notification", or "ring"'
        return self._send_cmd(f'termux-volume {type} {value}')

    async def _arun(self, type: str, value: int):
        return self._run(type, value)

class WiFiInfoTool(BaseRemoteTool, BaseTool):
    name = 'WiFi Info'
    description = (
        'Get information about the WiFi connection.'
        'Useful for getting information about the WiFi connection.'
        'Returns a dict.'
    )

    def _run(self):
        return self._send_cmd('termux-wifi-connectioninfo')

    async def _arun(self):
        return self._run()

class WiFiScanTool(BaseRemoteTool, BaseTool):
    name = 'WiFi Scan'
    description = (
        'Scan for WiFi networks.'
        'Useful for scanning for WiFi networks.'
        'Returns a list of dicts.'
    )

    def _run(self):
        return self._send_cmd('termux-wifi-scaninfo')

    async def _arun(self):
        return self._run()

class VibratorTool(BaseRemoteTool, BaseTool):
    name = 'Vibrator'
    description = (
        'Vibrate the device.'
        'Useful for vibrating the device.'
        'Accepts an integer duration in milliseconds.'
    )

    def _run(self, duration: int):
        return self._send_cmd(f'termux-vibrate -f -d {duration}')

    async def _arun(self, duration: int):
        return self._run(duration)

ALL_TOOLS = [
    BatteryStatusTool(),
    BrightnessTool(),
    PhotoTool(),
    ClipboardGetTool(),
    ClipboardSetTool(),
    FingerprintTool(),
    LocationTool(),
    MediaPauseTool(),
    RecordMicTool(),
    NotificationTool(),
    ListNotificationsTool(),
    URLOpenerTool(),
    TorchTool(),
    SpeakTool(),
    GetVolumeTool(),
    SetVolumeTool(),
    WiFiInfoTool(),
    WiFiScanTool(),
    VibratorTool(),
    MediaPlayTool()
]