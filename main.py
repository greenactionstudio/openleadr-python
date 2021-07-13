import asyncio
from openleadr.client import OpenADRClient
client = OpenADRClient(ven_name = 'myven', vtn_url='http://localhost:8000/local/webserver')
loop = asyncio.get_event_loop()
loop.create_task(client.run())
loop.run_forever()
