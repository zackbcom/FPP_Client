# pylint: disable=W0621
"""Asynchronous Python client for FPP."""

import asyncio

from fppclient import FPP


async def main() -> None:
    """Show example on controlling your FPP device."""
    async with FPP("192.168.2.60") as fpp:
        device = await fpp.update()
        print(device.system_status.advancedView.LocalGitVersion)
        print(device.system_status)

        # if device.state.on:
        #     print("Turning off FPP....")
        #     await fpp.master(on=False)
        # else:
        #     print("Turning on FPP....")
        #     await fpp.master(on=True)

        device = await fpp.update()
        print(device.system_status)


if __name__ == "__main__":
    asyncio.run(main())
