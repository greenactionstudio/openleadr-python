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
from openleadr.utils import report_callback
from openleadr.enums import MEASUREMENTS
import logging
## set the defualt logging config to DEBUG mode
logging.basicConfig(level = logging.WARNING)

nest_asyncio.apply()
client = OpenADRClient(ven_name = 'myven', vtn_url='http://127.0.0.1:8080/OpenADR2/Simple/2.0b')
client.add_report(report_callback,client.ven_id, report_name = 'TELEMETRY_STATUS')
client.add_report(report_callback,client.ven_id, report_name = 'TELEMETRY_USAGE', measurement= MEASUREMENTS.POWER_REAL)
#client.add_report(report_callback,client.ven_id, report_name = 'TELEMETRY_USAGE', measurement= MEASUREMENTS.ENERGY_REAL)
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

@app.route('/stop')
async def stop_server():
    await client.stop()
    return {'status': 200, 'body': 'The VEN has been stopped.'}

@app.route('/register_reports')
async def register_reports():
    if client.reports:
        await client.register_reports(client.reports)
    return {'status': 200, 'body': 'The VEN has sent register report with metadata.'}


    

def client_run():
    loop = asyncio.new_event_loop()
    loop.create_task(client.run())
    loop.run_forever()


if __name__ =="__main__":
    t1 = threading.Thread(target=app.run)
    t2 = threading.Thread(target=client_run)
    t1.start()
    t2.start()

