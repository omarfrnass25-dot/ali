from ..models.vehicle_state import VehicleState
from ..models.atmosphere import Atmosphere
from ..models.gravity import Gravity
from ..models.rocket_engine import RocketEngine
from ..models.aerodynamics import Aerodynamics
from .propagate import Propagate
from ..models.accelerations import calculate_accelerations
from ..config.rocket_loader import RocketLoader
from ..math.vector3 import Vector3
from ..math.quaternion import Quaternion
from ..math.matrix33 import Matrix33

class FDMExec:
    def __init__(self, config_file, dt=0.01):
        self.dt = dt
        self.time = 0.0
        loader = RocketLoader()
        config = loader.load(config_file)
        # initialize models
        self.atmosphere = Atmosphere()
        self.gravity = Gravity()
        self.engine = RocketEngine(
            isp=config.getfloat('PROPULSION', 'isp'),
            max_thrust=config.getfloat('PROPULSION', 'max_thrust'),
            fuel_mass=config.getfloat('MASS', 'fuel_mass')
        )
        self.aerodynamics = Aerodynamics(config)
        self.state = VehicleState(
            position=Vector3(0, 0, 0),
            velocity=Vector3(0, 0, 0),
            orientation=Quaternion(),
            angular_rates=Vector3(0, 0, 0),
            mass=config.getfloat('MASS', 'empty_mass') + self.engine.fuel_mass,
            inertia=Matrix33()
        )
        self.propagate = Propagate(dt)

    def run(self, duration):
        while self.time < duration:
            self.step()
            self.time += self.dt

    def step(self):
        # calculate environment
        altitude = self.state.position.z
        density = self.atmosphere.get_density(altitude)
        gravity_vec = self.gravity.get_gravity_vector(self.state.position)
        # engine
        thrust, fuel_flow = self.engine.calculate(self.dt)
        forces = Vector3(0, 0, thrust)  # assume along z
        moments = Vector3(0, 0, 0)
        # aerodynamics
        alpha = 0  # simple
        mach = self.state.velocity.magnitude() / self.atmosphere.get_speed_of_sound(altitude)
        aero_forces, aero_moments = self.aerodynamics.calculate(alpha, mach, self.state.velocity.magnitude(), density)
        forces += aero_forces
        moments += aero_moments
        # accelerations
        linear_accel, angular_accel = calculate_accelerations(self.state, forces, moments, gravity_vec)
        # propagate
        self.state = self.propagate.step(self.state, linear_accel, angular_accel)