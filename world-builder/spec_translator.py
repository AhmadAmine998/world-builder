
from utils.logging import create_logger, WBLogLevel
from utils.clothoid_utils import clothoid_to_waypoints_array

from dataTypes.ClothoidRoadState import ClothoidRoadState
from dataTypes.RoadTypes import RoadTypes

from pyclothoids import Clothoid
import numpy as np

# create logger for this file, but make it private
_logger = create_logger(WBLogLevel.DEBUG)

def _gen_straight_from_spec(spec, last_segment_state:ClothoidRoadState):
  clothoid = Clothoid.StandardParams(last_segment_state.x, last_segment_state.y, last_segment_state.t, 0, 0, spec["arc_length"])
  waypoints_arr = clothoid_to_waypoints_array(clothoid, 2, spec["arc_length"])
  return waypoints_arr, ClothoidRoadState(*waypoints_arr[-1].copy())

def _gen_left_from_spec(spec, last_segment_state:ClothoidRoadState, type=1):
  if("variant" not in spec):
    _logger.error(f'Expected left-turn spec to have variant key! Got {spec}')
    raise KeyError(f'Expected left-turn spec to have variant key! Got {spec}')
  else:
    if spec["variant"] == 1:
      s = spec["arc_length"]

      # If a curvature rate is not defined
      # Rate defaults such that an exact
      # left turn is made (i.e final tangent is pi/2)
      if "curvature_rate" in spec: 
        k0 = spec["curvature_rate"]
      else:
        k0 = np.pi/(2*s)

      clothoid = Clothoid.StandardParams(last_segment_state.x, last_segment_state.y, last_segment_state.t, k0, 0, s)
      waypoints_arr = clothoid_to_waypoints_array(clothoid, max(int(s*4), 10), s)
      return waypoints_arr, ClothoidRoadState(*waypoints_arr[-1].copy())
    elif spec["variant"] == 2:
      raise NotImplementedError("Type-2 left-turns not yet implemented :(")
    else:
      _logger.error(f'Expected left-turn spec variant to be either 1 or 2! Got {spec["variant"]}')
      raise NotImplementedError(f'Expected left-turn spec variant to be either 1 or 2! Got {spec["variant"]}')

def _gen_right_from_spec(spec, last_segment_state:ClothoidRoadState, type=1):
  if("variant" not in spec):
    _logger.error(f'Expected right-turn spec to have variant key! Got {spec}')
    raise KeyError(f'Expected right-turn spec to have variant key! Got {spec}')
  else:
    if spec["variant"] == 1:
      s = spec["arc_length"]

      # If a curvature rate is not defined
      # Rate defaults such that an exact
      # right turn is made (i.e final tangent is -pi/2)
      if "curvature_rate" in spec: 
        k0 = spec["curvature_rate"]
      else:
        k0 = -np.pi/(2*s)

      clothoid = Clothoid.StandardParams(last_segment_state.x, last_segment_state.y, last_segment_state.t, k0, 0, s)
      waypoints_arr = clothoid_to_waypoints_array(clothoid, max(int(s*4), 10), s)
      return waypoints_arr, ClothoidRoadState(*waypoints_arr[-1].copy())
    elif spec["variant"] == 2:
      raise NotImplementedError("Type-2 right-turns not yet implemented :(")
    else:
      _logger.error(f'Expected right-turn spec variant to be either 1 or 2! Got {spec["variant"]}')
      raise NotImplementedError(f'Expected right-turn spec variant to be either 1 or 2! Got {spec["variant"]}')

def clothoid_from_spec(road_segment, last_segment_state:ClothoidRoadState):
  if("spec" not in road_segment):
    _logger.error(f'Expected road segment at index {road_segment["index"]} to have spec! Got {road_segment}')
    raise KeyError(f'Expected road segment at index {road_segment["index"]} to have spec! Got {road_segment}')
  else:
    if RoadTypes[road_segment["spec"]["type"]] == RoadTypes.STRAIGHT:
      return _gen_straight_from_spec(road_segment["spec"], last_segment_state)
    elif RoadTypes[road_segment["spec"]["type"]] == RoadTypes.LEFT:
      return _gen_left_from_spec(road_segment["spec"], last_segment_state)
    elif RoadTypes[road_segment["spec"]["type"]] == RoadTypes.RIGHT:
      return _gen_right_from_spec(road_segment["spec"], last_segment_state)
    else:
      _logger.error(f'Road segment at index {road_segment["index"]} of type {road_segment["spec"]["type"]} is not yet implemented')
      raise NotImplementedError(f'Expected road_segment to have spec! Got {road_segment}')
