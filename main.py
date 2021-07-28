from logging import exception
from flask import Flask
import asyncio
import nest_asyncio
from openleadr.client import OpenADRClient
nest_asyncio.apply()
client = OpenADRClient(ven_name = 'myven', vtn_url='http://localhost:8000/local/webserver')
app = Flask(__name__)

@app.route('/home')
def home():
    return "Hello from the flask!"

@app.route('/create_party_registration', methods=['POST'])
async def create_party_registration():
  await client.create_party_registration()
  return {'status': 200, 'body': 'return from the create party registration'}

@app.route('/OadrPoll', methods=['POST'])
async def client_run():
  loop = asyncio.new_event_loop()
  loop.create_task(client.run())
  loop.run_forever()

if __name__ =="__main__":
  app.run()