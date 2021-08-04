from logging import debug, exception
from openleadr.messaging import parse_message
from flask import Flask, request
from xml.etree.ElementTree import fromstring, XML
import asyncio
import threading
import ssl
import aiohttp
import nest_asyncio
import json
from openleadr.client import OpenADRClient
nest_asyncio.apply()
client = OpenADRClient(ven_name = 'myven', vtn_url='http://127.0.0.1:8080/OpenADR2/Simple/2.0b')
app = Flask(__name__)

@app.route('/home')
def home():
    return "Hello from the flask!"

@app.route('/create_party_registration', methods=['GET'])
async def create_party_registration():
    await client.create_party_registration()
    return {'status': 200, 'body': 'return from the create party registration'}


@app.route('/create_opt', methods =['POST'])
async def create_opt():
    # _ , message_payload = parse_message(request.data)
    # print(message_payload)
    # return await client.create_opt(message_payload)
    return await client.create_opt(request.data)


@app.route('/cancel_opt', methods = ['POST'])
async def cancel_opt():
    return await client.cancel_opt(request.data)


    

def client_run():
    loop = asyncio.new_event_loop()
    loop.create_task(client.run())
    loop.run_forever()


if __name__ =="__main__":
    t1 = threading.Thread(target=app.run)
    t2 = threading.Thread(target=client_run)
    t1.start()
    t2.start()

