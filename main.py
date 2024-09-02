
import asyncio
import motor.motor_asyncio
from beanie import init_beanie

import server as sv
import documents as dc

MONGO_URI = 'mongodb://localhost'
collection_name = 'contadores'
db_name = 'RomaDBgps'


async def initialize_beanie():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    db = client[db_name]
    await init_beanie(database=db,
                      document_models=[dc.Contador])

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Conectamos MongoDB
    # client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    # db = client[db_name]
    loop.run_until_complete(initialize_beanie())

    factory = sv.MySocketServerFactory("ws://127.0.0.1:9000")
    factory.protocol = factory.create_protocol
    coro = loop.create_server(factory, '127.0.0.1', 9000)
    server = loop.run_until_complete(coro)
    print("server started", server.sockets)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
