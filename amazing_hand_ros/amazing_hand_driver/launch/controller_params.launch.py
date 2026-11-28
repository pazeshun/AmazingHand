"""Resolve the controller YAML once for the manager, spawner and Gazebo."""
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import OpaqueFunction, RegisterEventHandler, SetLaunchConfiguration
from launch.event_handlers import OnShutdown
from launch_ros.descriptions import ParameterFile


def resolve_controllers(context):
    share = Path(get_package_share_directory('amazing_hand_driver'))
    params = ParameterFile(share / 'config/ros2_controllers.yaml', allow_substs=True)
    return [
        SetLaunchConfiguration('controllers', str(params.evaluate(context))),
        RegisterEventHandler(OnShutdown(on_shutdown=lambda event, ctx: params.cleanup())),
    ]


def generate_launch_description():
    return LaunchDescription([OpaqueFunction(function=resolve_controllers)])
