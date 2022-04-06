"""

"""

# Importing python libraries for required processing
from ai2thor.controller import Controller
from ai2thor.platform import CloudRendering


controller = Controller(platform=CloudRendering)
event = controller.step("MoveAhead")
event.frame
