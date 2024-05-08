import asyncio
import os
from asyncio import Semaphore


terminal_info = '[{}] {} {}'


async def ping(sem, address):
    command = ['ping', address, '-n', '5']
    async with sem:
        process = await asyncio.create_subprocess_exec(*command, stdout=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()

        info = stdout.decode('cp866').split('\n')[2:7]
        connect = True
        for row in info:
            if 'TTL' in row:
                connect &= True
            else:
                connect &= False
        if connect:
            print(terminal_info.format('+', address, 'up'))
        else:
            print(terminal_info.format('-', address, 'down'))
    

async def main():
    addresses = [line.strip() for line in open('addresses.txt')]
    semaphore = Semaphore(os.cpu_count())
    tasks = [asyncio.create_task(ping(semaphore, address)) for address in addresses]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())