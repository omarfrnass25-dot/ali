from simulation.fdm_exec import FDMExec
from output.data_logger import DataLogger
from output.plotter import TrajectoryPlotter
from math.vector3 import Vector3

if __name__ == "__main__":
    fdm = FDMExec('config/rockets/simple_rocket.dat')
    logger = DataLogger('results/flight_data.csv')
    duration = 10.0
    while fdm.time < duration:
        fdm.step()
        logger.log(fdm.state, Vector3(0, 0, fdm.engine.thrust), fdm.atmosphere, fdm.time)
        fdm.time += fdm.dt
    logger.save()
    plotter = TrajectoryPlotter(logger.data)
    plotter.plot_2d()