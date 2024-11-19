import asyncio
from navigation.utils.nav_drone_config import Drone, ARA_mini
from navigation.planners.nav_multirotor_planner import MultirotorPlanner
from navigation.planners.nav_planner import NavPlanner

import protos.api_pb2 as api_pb2
import protos.api_pb2_grpc as api_pb2_grpc

# TODO: оснастить NAV_SERVICE модулем логирования данных

class NavigationManagerGRPC(api_pb2_grpc.NavigationManagerServicer):
    def __init__(self):
        self.planner = MultirotorPlanner(ARA_mini)

    async def TakeOFF(self, request, context):
        pass

    async def Land(self, request, context):
        pass

    async def Move(self, request, context):
        pass

    async def SetVelocity(self, request, context):
        pass

    async def SetSettings(self, request, context):
        pass


def serve():
    pass

if __name__ == '__main__':
    asyncio.run(serve())