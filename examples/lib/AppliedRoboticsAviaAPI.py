import asyncio
from navigation.nav_service import NavigationManagerGRPC
from driver.msp_service import MSPServiceClient

class AppliedRoboticsAviaAPI:
    """
    Provides an interface to call RPC services sequentially.
    """

    def __init__(self):
        """
        Initializes the AppliedRoboticsAviaAPI.
        """
        self.nav_client = NavigationManagerGRPC()
        self.msp_client = MSPServiceClient()

    async def takeoff(self, altitude):
        """
        Calls the takeoff service.
        """
        response = await self.nav_client.Takeoff(altitude)
        print(f"Takeoff response: {response}")

    async def move_by_point(self, x, y, z):
        """
        Calls the move_by_point service.
        """
        response = await self.nav_client.MoveByPoint(x, y, z)
        print(f"Move by point response: {response}")

    async def land(self):
        """
        Calls the land service.
        """
        response = await self.nav_client.Land()
        print(f"Land response: {response}")

    def __getattr__(self, name):
        """
        Dynamically handles method calls.
        """
        async def method(*args, **kwargs):
            if name in self.__class__.__dict__:
                await self.__class__.__dict__[name](self, *args, **kwargs)
            else:
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        return method
