import numpy as np
import os, argparse
import sys
import matplotlib.pyplot as plt

from world_builder.dataTypes.ClothoidRoadState import ClothoidRoadState
from world_builder.spec_translator import json_spec_to_waypoints
from world_builder.utils.logging import create_logger

_logger = create_logger()

def parse_args():
  """
  Parse input arguments
  """
  parser = argparse.ArgumentParser(description='Create trajectory for fast lanelet creation in Vector Map Builder')
  parser.add_argument('-f', '--spec_file', help='Path of json file to use to build out the map', type=str)
  parser.add_argument('-i', '--interactive', action='store_true', help='Launch the script in interactive (text) mode')
  parser.add_argument('-c', '--close', action='store_true', help='Automatically closes the trajectroy through G2 Hermite interpolation.')
  parser.add_argument('-x0', default=0, help='Trajectory starting point x-coordinate. Default is 0.')
  parser.add_argument('-y0', default=0, help='Trajectory starting point y-coordinate. Default is 0.')
  parser.add_argument('-p', '--plot', action='store_true', help='Plot resulting trajectory')
  parser.add_argument('-s','--save', help='Save the resulting trajectory to a csv file. Default is false.', action='store_true')
  filepath = os.path.join( os.getcwd(), "results", 'spec_file_trajectory.csv')
  parser.add_argument('-sf','--save_file', help='Name of the csv file to store generated trajectory into. Default is "spec_file"_trajectory.csv', default=filepath, type=str)

  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

  args = parser.parse_args()
  return args

if __name__ == '__main__':
  args = parse_args()
  if(args.interactive):
    raise NotImplementedError()
  elif(args.spec_file):
    initial_state = ClothoidRoadState(float(args.x0), float(args.y0), 0)
    waypoints_arr = json_spec_to_waypoints(args.spec_file, initial_state, args.close)
    if args.plot:
      plt.plot(waypoints_arr[:, 0], waypoints_arr[:, 1])
      plt.title(f'Generated trajectory form spec file {os.path.basename(args.spec_file)}')
      plt.xlabel('X (m)')
      plt.ylabel('Y (m)')
      plt.show()
    if args.save:
      # Insert column of all zeros for z
      waypoints_arr = np.insert(waypoints_arr, 2, 0, axis=1)

      # check if results directory exists
      if not os.path.exists(os.path.join( os.getcwd(), "results")):
        os.makedirs(os.path.join( os.getcwd(), "results"))
      # save trajectory as json
      save_path = os.path.join( f'{os.path.split(__file__)[0]}', "results", f'{os.path.basename(args.spec_file).split(".")[0]}_trajectory.csv')

      np.savetxt(save_path, waypoints_arr, delimiter=",", header="x,y,z,yaw", comments="")

      _logger.info(f'Trajectory saved to {save_path} successfully.')
  else:
    raise NotImplementedError()