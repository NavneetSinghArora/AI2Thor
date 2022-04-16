"""

"""

# Importing python libraries for required processing
import ai2thor.server
from ai2thor.controller import Controller
from ai2thor.platform import CloudRendering
import numpy as np
from typing import Tuple, List
import matplotlib.pyplot as plt


class Environment:
    """
    This class is used to initialize all the basic environment for the simulation in AI2Thor which will be applicable to the entire project.
    """

    __instance = None
    __instance_created = False
    __controller: Controller = None

    def __init__(self, simulator_properties):
        """
        This method makes sure that the properties are initialized only once in lifetime of this object.
        """

        self.simulator_properties = simulator_properties
        self.number_of_agents = int(self.simulator_properties['number_of_agents'])
        self.render_depth_image = bool(self.simulator_properties['render_depth_image'])

        self._started = False

        if not self.__instance_created:
            __controller = Controller(platform=CloudRendering,

                                      agentCount=self.number_of_agents,
                                      agentMode=self.simulator_properties['agent_mode'],
                                      visibilityDistance=float(self.simulator_properties['visibility_distance']),
                                      scene="FloorPlan212",

                                      gridSize=float(self.simulator_properties['grid_size']),
                                      snapToGrid=True,
                                      rotateStepDegrees=90,

                                      renderDepthImage=self.render_depth_image,
                                      renderInstanceSegmentation=bool(self.simulator_properties['render_image_segmentation']),

                                      width=300,
                                      height=300,
                                      fieldOfView=int(self.simulator_properties['field_of_view']))

            self.__instance_created = True

    def __new__(cls, *args, **kwargs):
        """
        This is a class method.
        This method makes sure that the class follows Singleton Pattern.
        """
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)

        return cls.__instance

    def get_controller(self):
        return self.__controller

    @property
    def scene_name(self) -> str:
        return self.__controller.last_event.metadata["sceneName"]

    @property
    def current_frame(self) -> np.ndarray:
        return self.__controller.last_event.frame

    @property
    def current_frames(self) -> Tuple[np.ndarray, ...]:
        return tuple(
            self.__controller.last_event.events[i].frame for i in range(self.number_of_agents)
        )

    @property
    def current_depth_frames(self) -> Tuple[np.ndarray, ...]:
        if not self.render_depth_image:
            raise Exception(
                "Depth frames are not available, "
                "Must set render_depth_image to true before initializing."
            )
        return tuple(
            self.__controller.last_event.events[i].depth_frame
            for i in range(self.number_of_agents)
        )

    @property
    def last_event(self) -> ai2thor.server.Event:
        return self.__controller.last_event

    @property
    def started(self) -> bool:
        return self._started

    def start(self) -> None:
        self.__controller.start()
        self._started = True

    def stop(self) -> None:
        self.__controller.stop()
        self._started = False

    def reset(self):
        return self.__controller.reset()
