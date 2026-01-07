import csv

class DataLogger:
    OUTPUT_VARS = [
        'time', 'x', 'y', 'z', 'altitude', 'range',
        'Vx', 'Vy', 'Vz', 'Vt', 'mach',
        'phi', 'theta', 'psi', 'alpha', 'beta',
        'p', 'q', 'r',
        'ax', 'ay', 'az', 'Nz',
        'thrust', 'fuel_mass', 'drag',
        'density', 'dynamic_pressure'
    ]
    
    def __init__(self, filename: str, format: str = 'csv'):
        self.filename = filename
        self.format = format
        self.data = []
    
    def log(self, state, forces, atmosphere, time):
        row = {
            'time': time,
            'x': state.position.x, 'y': state.position.y, 'z': state.position.z,
            'altitude': state.position.z,
            'range': (state.position.x**2 + state.position.y**2)**0.5,
            'Vt': state.velocity.magnitude(),
            'theta': state.orientation.to_euler()[1],
            'thrust': forces.z,  # assume
            'fuel_mass': state.fuel_mass,
            # ... add more
        }
        self.data.append(row)
    
    def save(self):
        if self.format == 'csv':
            self._save_csv()
        else:
            self._save_dat()
    
    def _save_csv(self):
        with open(self.filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.data[0].keys())
            writer.writeheader()
            writer.writerows(self.data)