import numpy as np
from pyclothoids import Clothoid

def clothoid_to_waypoints_array(clothoid:Clothoid, num_points:int, arclength:float):
  points_idx = np.linspace(0, arclength, num_points) # Returns both points, has to be filtered by generator
  points = None
  for idx in points_idx:
    x_m = clothoid.X(idx)
    y_m = clothoid.Y(idx)
    t_m = clothoid.Theta(idx)
    new_point = np.array([[x_m, y_m, t_m]])
    if points is None:
      points = new_point.copy()
    else:
      points = np.vstack((points, new_point))
  return points
