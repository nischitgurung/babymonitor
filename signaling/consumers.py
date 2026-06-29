import json
from channels.generic.websocket import AsyncWebsocketConsumer

# One shared room for the 1-to-1 baby monitor session.
# If you ever need multi-room support, derive room_name from the URL route.
ROOM_GROUP = "babymonitor_room"


class SignalingConsumer(AsyncWebsocketConsumer):
    """
    Pure relay: every message received from one peer is forwarded to the
    *other* peer(s) in the same group.  Django never inspects SDP/ICE
    payloads — that is intentional and keeps the server media-agnostic.
    """

    async def connect(self):
        await self.channel_layer.group_add(ROOM_GROUP, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(ROOM_GROUP, self.channel_name)
        # Tell the remaining peer that the other side left so it can reset.
        await self.channel_layer.group_send(
            ROOM_GROUP,
            {
                "type": "signal_message",
                "data": json.dumps({"type": "peer-disconnected"}),
                # Stamp the sender so the broadcast handler can skip them.
                "sender_channel": self.channel_name,
            },
        )

    async def receive(self, text_data=None, bytes_data=None):
        """Relay every message to every OTHER peer in the room."""
        await self.channel_layer.group_send(
            ROOM_GROUP,
            {
                "type": "signal_message",
                "data": text_data,
                # Tag the originating channel so we can skip the echo.
                "sender_channel": self.channel_name,
            },
        )

    # ------------------------------------------------------------------ #
    # Group-send handler                                                   #
    # ------------------------------------------------------------------ #
    async def signal_message(self, event):
        # Do NOT echo back to the sender — this is the fix for Bug 4.
        if event.get("sender_channel") == self.channel_name:
            return
        await self.send(text_data=event["data"])