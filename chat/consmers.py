import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer

from channels.db import database_sync_to_async

from .models import Thread, ChatMessage




class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print( "conneted" , event)

        #await asyncio.sleep(10)
        other_user = self.scope['url_route']['kwargs']['username']
        me = self.scope['user']
        #print(other_user,me)
        thread_obj = await self.get_thread(me, other_user)
        self.thread_obj = thread_obj
        #print(me, thread_obj.id)
        chat_room = f"thread_{thread_obj.id}"
        self.chat_room = chat_room
        #print(thread_obj)
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name #channel_name is default attribute of channels
        )

        await self.send({
            "type": "websocket.accept"
        })
    async def websocket_receive(self,event):
        # when a message is recieved from websocket
        print("recieve",event)
        front_text = event.get('text',None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
            msg = loaded_dict_data.get('message')
            #print(msg)
            user = self.scope['user']
            username = 'default'
            if user.is_authenticated:
                username = user.username
            myResponse = {
                'message':msg,
                'username': username
            }
            
            await self.create_chat_message(user,msg)
           
            # this broadcasts the message event to be sent
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type":"chat_message",
                    "text":json.dumps(myResponse)
                }
            )


            #await self.send()
        # recieve {'type': 'websocket.receive', 'text': '{"message":"sdfsdf"}'}

    async def chat_message(self,event):
        #print("message",event)
        # this sends the actual message
        await self.send({
            "type":"websocket.send",
            "text":event["text"]
        })

    async def websocket_disconnect(self,event):
        # when socket disconnects 
        print("disconnected",event)
    
    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user,other_username)[0]

    @database_sync_to_async
    def create_chat_message(self, me , msg):
        thread_obj = self.thread_obj
        
        return ChatMessage.objects.create(thread =thread_obj ,user = me ,message=msg)


