import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class TrajectoryPlotter:
    def __init__(self, data: list):
        self.data = data
    
    def plot_2d(self, save_path=None):
        ranges = [d['range']/1000 for d in self.data]
        altitudes = [d['altitude']/1000 for d in self.data]
        
        plt.figure(figsize=(10, 6))
        plt.plot(ranges, altitudes, 'b-', linewidth=2)
        plt.xlabel('المدى (km)')
        plt.ylabel('الارتفاع (km)')
        plt.title('مسار الصاروخ')
        plt.grid(True)
        if save_path:
            plt.savefig(save_path, dpi=150)
        plt.show()
    
    def plot_3d(self, save_path=None):
        x = [d['x']/1000 for d in self.data]
        y = [d['y']/1000 for d in self.data]
        z = [d['altitude']/1000 for d in self.data]
        
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(x, y, z, 'r-', linewidth=2)
        ax.set_xlabel('X (km)')
        ax.set_ylabel('Y (km)')
        ax.set_zlabel('الارتفاع (km)')
        ax.set_title('المسار ثلاثي الأبعاد')
        if save_path:
            plt.savefig(save_path, dpi=150)
        plt.show()
    
    def plot_time_series(self, variables: list, save_path=None):
        time = [d['time'] for d in self.data]
        
        fig, axes = plt.subplots(len(variables), 1, figsize=(10, 3*len(variables)))
        for i, var in enumerate(variables):
            values = [d[var] for d in self.data]
            axes[i].plot(time, values)
            axes[i].set_ylabel(var)
            axes[i].grid(True)
        axes[-1].set_xlabel('الزمن (s)')
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=150)
        plt.show()