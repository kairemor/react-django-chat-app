from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
import json

from .models import Message 

class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        '''
        This function allow to fetch the last message when the user enter in the room 
        '''
        # messages = Message.get_10_message(10)
        messages = Message.objects.all()
        content = {
            'command':'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        '''
        this function is excuted when the websockect receive a new message 
        '''
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        msg_content = data['message']
        message = Message.objects.create(author=author_user, content=msg_content)
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)
    
    
    # commande allow to execute one the above fonction
    # the commande is a part of the message give by the user
    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def message_to_json(self, message):
        '''
        This method return a dictionary like a json 
        '''
        return {
            'author':message.author.username, 
            'content':message.content, 
            'msg_date': str(message.msg_date)
        }

    def messages_to_json(self, messages):
        return [self.message_to_json(message) for message in messages]

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )


    def receive(self, text_data):
        '''
            This function is the executed on when a event occur since the user 
            It will execute the command sended by the user. Neither the command is to fectch or 
            to create a new message 
        '''
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        '''
            this function allow to send message to room group
        '''
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))