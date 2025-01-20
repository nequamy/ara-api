from lib.AppliedRoboticsAviaAPI import AppliedRoboticsAviaAPI
import time
import asyncio


def main():
    api = AppliedRoboticsAviaAPI()

    async def run():
        await api.takeoff(1.5)
        await asyncio.sleep(3)

        await api.move_by_speed(1, 0, 1)
        await asyncio.sleep(3)
        await api.move_by_speed(0, 1, 1)
        await asyncio.sleep(3)
        await api.move_by_speed(-1, 0, 1)
        await asyncio.sleep(3)
        await api.move_by_speed(0, -1, 1)
        await asyncio.sleep(3)

        await api.land()

    asyncio.run(run())

if __name__ == "__main__":
    main()