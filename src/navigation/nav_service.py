import asyncio
import grpc
from navigation.utils.nav_drone_config import Drone, ARA_mini
from navigation.planners.nav_multirotor_planner import NavigationMultirotorPlanner
from navigation.planners.nav_planner import NavPlanner

import protos.api_pb2 as api_pb2
import protos.api_pb2_grpc as api_pb2_grpc


class NavigationManagerGRPC(api_pb2_grpc.NavigationManagerServicer):
    """
    gRPC server for managing navigation commands for a multirotor drone.
    """

    NavigationFlags = {
        'takeoff': 1 << 1,
        'land': 1 << 2,
        'set_velocity': 1 << 3,
        'move': 1 << 4,
    }

    def __init__(self):
        """
        Initialize the NavigationManagerGRPC with a multirotor planner and initial state.
        """
        self.planner = NavigationMultirotorPlanner(ARA_mini)
        self.state = 0

    async def TakeOFF(self, request, context):
        """
        Handle the TakeOFF gRPC request.

        Args:
            request: The gRPC request containing the takeoff command.
            context: The gRPC context.

        Returns:
            api_pb2.TakeOFFResponse: The response indicating success.
        """
        self.state |= NavigationManagerGRPC.NavigationFlags['takeoff']

        await self.msg_to_msp_service(
            action='TakeOFF',
            method=self.planner.takeoff,
            check_method=self.planner.check_desired_altitude
        )

        return api_pb2.StatusData(success="OK")

    async def Land(self, request, context):
        """
        Handle the Land gRPC request.

        Args:
            request: The gRPC request containing the land command.
            context: The gRPC context.

        Returns:
            api_pb2.LandResponse: The response indicating success.
        """
        self.state |= NavigationManagerGRPC.NavigationFlags['land']

        await self.msg_to_msp_service(
            action='Land',
            method=self.planner.land,
            check_method=self.planner.check_desired_altitude
        )

        return api_pb2.StatusData(success="OK")

    async def Move(self, request, context):
        """
        Handle the Move gRPC request.

        Args:
            request: The gRPC request containing the move command.
            context: The gRPC context.

        Returns:
            api_pb2.MoveResponse: The response indicating success.
        """
        self.state |= NavigationManagerGRPC.NavigationFlags['move']

        self.planner.set_point_to_move(request.x, request.y, request.z)
        await self.msg_to_msp_service(
            action='Move',
            method=lambda: self.planner.move(),
            check_method=self.planner.check_desired_position
        )

        return api_pb2.StatusData(success="OK")

    async def SetVelocity(self, request, context):
        """
        Handle the SetVelocity gRPC request.

        Args:
            request: The gRPC request containing the set velocity command.
            context: The gRPC context.

        Returns:
            api_pb2.SetVelocityResponse: The response indicating success.
        """
        self.state |= NavigationManagerGRPC.NavigationFlags['set_velocity']

        await self.msg_to_msp_service(
            action='SetVelocity',
            method=lambda: self.planner.set_velocity(request.vx, request.vy, request.vz),
            check_method=self.planner.check_desired_position
        )

        return api_pb2.StatusData(success="OK")

    async def SetSettings(self, request, context):
        """
        Handle the SetSettings gRPC request.

        Args:
            request: The gRPC request containing the set settings command.
            context: The gRPC context.

        Returns:
            None
        """
        # TODO: Implement the method to set settings
        pass

    async def msg_to_msp_service(self, action, method, check_method):
        """
        Stream data to the MSP service.

        Args:
            action: The action being performed.
            method: The method to execute the action.
            check_method: The method to check the desired state.

        Returns:
            None
        """
        async with grpc.aio.insecure_channel('localhost:50051') as channel:
            stub = api_pb2_grpc.MSPServiceStub(channel)
            while not check_method():
                data = method()
                await stub.StreamData(api_pb2.StreamRequest(action=action, data=data))
                await asyncio.sleep(0.1)  # Adjust the sleep time as needed


def serve():
    """
    Start the gRPC server to handle navigation commands.
    """
    server = grpc.aio.server()
    api_pb2_grpc.add_NavigationManagerServicer_to_server(NavigationManagerGRPC(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())