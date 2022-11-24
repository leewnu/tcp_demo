import socket 
import sys, os
import pandas as pd
import asyncio
import time
import json 

host = socket.gethostname()
port = 8888

dirname = os.path.dirname(os.path.abspath(__file__))

df_sample = pd.read_csv(dirname+'/data/iris.csv')

async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(host, port)

    print(f'Send: {message!r}')
    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()


for i in range(len(df_sample)):
    msg = {}
    for item in df_sample.columns: 
        msg[item] = df_sample.iloc[i, :][item]
    msg_json = json.dumps(msg)
    asyncio.run(tcp_echo_client(msg_json))
    time.sleep(2)