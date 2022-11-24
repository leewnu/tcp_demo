import socket as sk

import asyncio

host = sk.gethostname()

print(host)
port = 8888

async def handle_echo(reader, writer):
    data = ''
    while True: 
        data += (await reader.read(10)).decode()
        print(data)
        if data[-1] == '}': 
            break
    # data = await reader.read(10)

    message = data ##.decode()
    print(message[-1])
    addr = writer.get_extra_info('peername')

    print(f"Received {message!r} from {addr!r}")

    print(f"Send: {message!r}")
    writer.write(data.encode())
    await writer.drain()

    print("Close the connection")
    writer.close()

async def main():
    server = await asyncio.start_server(handle_echo, host, port)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())