import asyncio
import logging
import os

import pytest
from dotenv import load_dotenv

from hikconnect.api import HikConnect

pytestmark = [pytest.mark.asyncio, pytest.mark.manual]


async def test_main():
    username = os.getenv("HIKCONNECT_USERNAME")
    password = os.getenv("HIKCONNECT_PASSWORD")
    channel_number = int(os.getenv("HIKCONNECT_CHANNEL_NUMBER", "1"))

    async with HikConnect() as api:
        await api.login(username, password)
        print(f"{api.is_refresh_login_needed()=}")

        devices = [device async for device in api.get_devices()]
        for device in devices:
            print(await api.get_call_status(device["serial"]))
            async for camera in api.get_cameras(device["serial"]):
                print(device, camera)

        await asyncio.sleep(1)
        await api.refresh_login()

        # BEWARE: actually unlocks door!
        print(f"api.unlock({devices[0]['serial']=}, {channel_number=})")
        # await api.unlock(devices[0]["serial"], channel_number)

        # BEWARE: answers an active call!
        print(f"api.answer_call({devices[0]['serial']=})")
        # await api.answer_call(devices[0]["serial"])

        # BEWARE: cancels an active call!
        print(f"api.cancel_call({devices[0]['serial']=})")
        # await api.cancel_call(devices[0]["serial"])

        # BEWARE: hangs up an active call!
        print(f"api.hangup_call({devices[0]['serial']=})")
        # await api.hangup_call(devices[0]["serial"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    load_dotenv()
    asyncio.run(test_main())
