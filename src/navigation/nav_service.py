import asyncio
import grpc
from navigation.utils.nav_drone_config import Drone, ARA_mini
from navigation.planners.nav_multirotor_planner import MultirotorPlanner
from navigation.planners.nav_planner import NavPlanner

import protos.api_pb2 as api_pb2
import protos.api_pb2_grpc as api_pb2_grpc

# TODO: оснастить NAV_SERVICE модулем логирования данных

class NavigationManagerGRPC(api_pb2_grpc.NavigationManagerServicer):
    NavigationFlags = {
        'takeoff': 1 << 1,
        'land': 1 << 2,
        'set_velocity': 1 << 3,
        'move': 1 << 4,
    }

    def __init__(self):
        self.planner = MultirotorPlanner(ARA_mini)
        self.state = 0

    async def TakeOFF(self, request, context):
        self.state |= NavigationManagerGRPC.NavigationFlags['takeoff']

        await self.stream_to_msp_service(
            action='TakeOFF',
            method=self.planner.takeoff,
            check_method=self.planner.check_desired_altitude
        )

        return api_pb2.TakeOFFResponse(success=True)

    async def Land(self, request, context):
        self.state |= NavigationManagerGRPC.NavigationFlags['land']

        await self.stream_to_msp_service(
            action='Land',
            method=self.planner.land,
            check_method=self.planner.check_desired_altitude
        )

        return api_pb2.LandResponse(success=True)

    async def Move(self, request, context):
        self.state |= NavigationManagerGRPC.NavigationFlags['move']

        await self.stream_to_msp_service(
            action='Move',
            method=lambda: self.planner.move(request.x, request.y, request.z),
            check_method=self.planner.check_desired_position
        )

        return api_pb2.MoveResponse(success=True)

    async def SetVelocity(self, request, context):
        self.state |= NavigationManagerGRPC.NavigationFlags['set_velocity']


        await self.stream_to_msp_service(
            action='SetVelocity',
            method= lambda: self.planner.set_velocity(request.vx, request.vy, request.vz),
            check_method=self.planner.check_desired_position
        )

        return api_pb2.SetVelocityResponse(success=True)

    async def SetSettings(self, request, context):
        # TODO: реализовать метод установки настроек
        pass
        # result = await self.planner.set_settings(request.settings)
        #
        # await self.stream_to_msp_service(
        #     action='SetSettings',
        #     method=result,
        #     check_method=lambda: True
        # )
        #
        # return api_pb2.SetSettingsResponse(success=result)

    async def stream_to_msp_service(self, action, method, check_method):
        async with grpc.aio.insecure_channel('localhost:50051') as channel:
            stub = api_pb2_grpc.MSPServiceStub(channel)
            while not check_method():
                data = method()
                await stub.StreamData(api_pb2.StreamRequest(action=action, data=data))
                await asyncio.sleep(0.1)  # Adjust the sleep time as needed


def serve():
    server = grpc.aio.server()
    api_pb2_grpc.add_NavigationManagerServicer_to_server(NavigationManagerGRPC(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())