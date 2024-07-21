# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Player, FriendRequest
from channels.db import database_sync_to_async


class FriendRequestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.room_group_name = f'friend_requests_{self.user_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        if action == 'send_friend_request':
            await self.send_friend_request(data)

    async def send_friend_request(self, data):
        sender_id = data['sender_id']
        receiver_id = data['receiver_id']

        sender = await self.get_player(sender_id)
        receiver = await self.get_player(receiver_id)

        if sender and receiver:
            friend_request, status = await self.create_friend_request(sender, receiver)
            if status == "error":
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'Friend request already sent.'
                }))
            else:
                await self.channel_layer.group_send(
                    f'friend_requests_{receiver_id}',
                    {
                        'type': 'friend_request_notification',
                        'sender_id': sender_id,
                        'sender_username': sender.nickname,
                        'receiver_id': receiver_id,
                        'timestamp': str(friend_request.timestamp),
                    }
                )

    @database_sync_to_async
    def get_player(self, player_id):
        try:
            return Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            return None

    @database_sync_to_async
    def create_friend_request(self, sender, receiver):
        new, created = FriendRequest.objects.get_or_create(sender=sender, receiver=receiver)
        if not created:
            return None, "error"
        return new, "success"

    async def friend_request_notification(self, event):
        await self.send(text_data=json.dumps(event))
