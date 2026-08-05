import asyncio
import asyncssh

class MySSHServer(asyncssh.SSHServer):
    def connection_made(self, conn):
        print(f"Conexión desde {conn.get_extra_info('peername')}")

async def handle_client(process):
    # Aquí ejecutas el bucle principal de tu TUI redirigiendo E/S
    process.stdout.write("¡Bienvenido a mi TUI por SSH!\n")
    # ... tu lógica de TUI ...
    await process.stdout.drain()

async def main():
    await asyncssh.create_server(
        MySSHServer, '', 2222,
        server_host_keys=['/ruta/a/host_key'],
        process_factory=handle_client
    )

asyncio.run(main())