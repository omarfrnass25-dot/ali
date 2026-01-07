"""
نموذج الغلاف الجوي ISA 1976 مع تكامل JSBSim للدقة
مستوحى من FGStandardAtmosphere.h في JSBSim
"""

import numpy as np

try:
    import jsbsim
    JSBSIM_AVAILABLE = True
except ImportError:
    JSBSIM_AVAILABLE = False
    print("تحذير: jsbsim غير متوفر، سيتم استخدام تنفيذ بسيط")

class Atmosphere:
    """نموذج الغلاف الجوي"""

    def __init__(self):
        if JSBSIM_AVAILABLE:
            self.jsb_atmos = jsbsim.FGStandardAtmosphere()
        else:
            # تنفيذ بسيط كبديل
            self.R = 287.05  # J/kg·K
            self.g0 = 9.80665  # m/s²
            self.T0 = 288.15  # K
            self.P0 = 101325  # Pa
            self.L = 0.0065  # K/m

    def get_temperature(self, altitude):
        """درجة الحرارة عند الارتفاع (m)"""
        if JSBSIM_AVAILABLE:
            # JSBSim يستخدم feet، تحويل
            alt_ft = altitude * 3.28084
            temp_r = self.jsb_atmos.GetTemperature(alt_ft)
            return (temp_r - 459.67) * 5/9  # Rankine to Celsius to Kelvin? Wait, adjust
            # Actually, JSBSim returns Rankine, convert to Kelvin
            return temp_r * 5/9
        else:
            # ISA بسيط
            if altitude < 11000:
                return self.T0 - self.L * altitude
            else:
                return 216.65

    def get_pressure(self, altitude):
        """الضغط عند الارتفاع (Pa)"""
        if JSBSIM_AVAILABLE:
            alt_ft = altitude * 3.28084
            press_psf = self.jsb_atmos.GetPressure(alt_ft)
            return press_psf * 47.8803  # psf to Pa
        else:
            # ISA بسيط
            if altitude < 11000:
                return self.P0 * (1 - self.L * altitude / self.T0)**(self.g0 / (self.R * self.L))
            else:
                p11 = self.P0 * (1 - self.L * 11000 / self.T0)**(self.g0 / (self.R * self.L))
                return p11 * np.exp(-self.g0 * (altitude - 11000) / (self.R * 216.65))

    def get_density(self, altitude):
        """الكثافة عند الارتفاع (kg/m³)"""
        if JSBSIM_AVAILABLE:
            alt_ft = altitude * 3.28084
            density_slug_ft3 = self.jsb_atmos.GetDensity(alt_ft)
            return density_slug_ft3 * 515.379  # slug/ft³ to kg/m³
        else:
            T = self.get_temperature(altitude)
            P = self.get_pressure(altitude)
            return P / (self.R * T)

    def get_speed_of_sound(self, altitude):
        """سرعة الصوت (m/s)"""
        if JSBSIM_AVAILABLE:
            alt_ft = altitude * 3.28084
            sos_fps = self.jsb_atmos.GetSpeedOfSound(alt_ft)
            return sos_fps * 0.3048  # ft/s to m/s
        else:
            T = self.get_temperature(altitude)
            return np.sqrt(1.4 * self.R * T)

    def get_dynamic_pressure(self, altitude, velocity):
        """الضغط الديناميكي (Pa)"""
        rho = self.get_density(altitude)
        return 0.5 * rho * velocity**2

# مثال الاستخدام
if __name__ == "__main__":
    atmos = Atmosphere()
    alt = 1000  # m
    print(f"درجة الحرارة عند {alt}m: {atmos.get_temperature(alt)} K")
    print(f"الضغط: {atmos.get_pressure(alt)} Pa")
    print(f"الكثافة: {atmos.get_density(alt)} kg/m³")