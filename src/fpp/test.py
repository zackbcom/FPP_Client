
from .fpp import FPP
host = "192.168.2.60"

async with FPP(host) as led:
    device = await led.update()