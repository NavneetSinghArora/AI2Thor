"""
This File is the staring point of the AI2THOR project.
The file helps initialize the global properties and runs the code for the entire coding and setup.
"""

# Importing python libraries for required processing
from pathlib import Path
from global_variables import GlobalVariables
from src.core.simulator.configuration.simulator_variables import SimulatorVariables


def get_package_root():
    """
    This function fetches the path to the parent directory and returns the path as a string.

    :return: Path to the root directory of the project as a string.
    :rtype: String
    """

    return str(Path(__file__).parent.parent.parent.parent.parent)


def _init(**kwargs):
    """
    Initialize the global system properties.
    TODO: Starting point for logging the package
    """

    # Initializing the parent root directory for path configuration.
    kwargs['package_root'] = get_package_root()

    # Initializing the Global Variables which will be available throughout the project.
    variables = GlobalVariables(**kwargs)
    variables.load_configuration_properties()

    return variables


if __name__ == '__main__':
    # Initializing the project and loading the properties
    global_variables = _init()
    global_properties = global_variables.global_properties

    # Initializing the Simulation Environment
    simulator_variables = SimulatorVariables(global_properties)
    simulator_variables.load_configuration_properties()
    simulator_properties = simulator_variables.simulator_properties
