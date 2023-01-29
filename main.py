import asyncio
import json
from typing import List

import aio_pika
from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from fastapi import Request
from fastapi import Response
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

# locate templates
templates = Jinja2Templates(directory="templates")


app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RegisterValidator(BaseModel):
    username: str

    class Config:
        orm_mode = True


class SocketManager:
    def __init__(self):
        self.active_connections: List[(WebSocket, str)] = []

    async def connect(self, websocket: WebSocket, user: str):
        await websocket.accept()
        self.active_connections.append((websocket, user))

    def disconnect(self, websocket: WebSocket, user: str):
        self.active_connections.remove((websocket, user))

    async def broadcast(self, data):
        for connection in self.active_connections:
            await connection[0].send_json(data)


async def get_exchange(future_connection, future_exchange):
    connection = await aio_pika.connect_robust("amqp://user:password@localhost:5672/", loop=loop)
    future_connection.set_result(connection)
    channel = await connection.channel()

    # Declare the exchange
    exchange_name = 'my_exchange'
    routing_key = ''
    exchange_obj = await channel.declare_exchange(name=exchange_name, type='fanout')
    future_exchange.set_result(exchange_obj)


async def consumer(future_connection, future_exchange):
    connection = await future_connection

    # queue_name = "test_queue"
    routing_key = ""

    # Creating channel
    channel = await connection.channel()

    # Declaring exchange
    exchange = await future_exchange

    # Declaring queue
    queue = await channel.declare_queue(auto_delete=True)
    print(f"queue name: {queue.name}")

    # Binding queue
    await queue.bind(exchange, routing_key)

    async def process_message(message: aio_pika.abc.AbstractIncomingMessage) -> None:
        async with message.process():
            print(message.body)
            await manager.broadcast(json.loads(message.body))  # send to exchange
            await asyncio.sleep(1)

    # Receiving message
    await queue.consume(callback=process_message)

    try:
        # Wait until terminate
        await asyncio.Future()
    finally:
        await connection.close()


loop = asyncio.get_running_loop()
future_connection = loop.create_future()
future_exchange = loop.create_future()
loop.create_task(get_exchange(future_connection, future_exchange))
loop.create_task(consumer(future_connection, future_exchange))

manager = SocketManager()


@app.get("/")
def get_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/chat")
def get_chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.websocket("/api/chat")
async def chat(websocket: WebSocket):
    sender = websocket.query_params.get('user')
    # sender = websocket.cookies.get("X-Authorization")
    if sender:
        await manager.connect(websocket, sender)
        response = {
            "sender": sender,
            "message": "got connected"
        }
        await manager.broadcast(response)
        try:
            exchange = await future_exchange
            while True:
                data = await websocket.receive_json()
                # await manager.broadcast(data)  # send to exchange
                await exchange.publish(aio_pika.Message(body=json.dumps(data).encode()), routing_key='')
        except WebSocketDisconnect:
            manager.disconnect(websocket, sender)
            response['message'] = "left"
            await manager.broadcast(response)
        except Exception as e:
            print(e)


@app.get("/api/current_user")
def get_user(request: Request):
    return request.cookies.get("X-Authorization")


@app.post("/api/register")
def register_user(user: RegisterValidator, response: Response):
    response.set_cookie(key="X-Authorization", value=user.username, httponly=True)
