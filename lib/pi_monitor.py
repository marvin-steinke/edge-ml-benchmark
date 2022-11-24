import psutil
from cpufreq import cpuFreq
try:
    from lib import SDL_Pi_SunControl as sdl
except ImportError:
    pass
try:
    from ina219 import INA219
except ImportError:
    pass

class PiMonitor():
    def __init__(self) -> None:
        # support either SunControl or ina219 sensors
        self.sc_loaded = True
        try:
            self.sc = sdl.SDL_Pi_SunControl(
                    INA3221Address = 0x40,
                    USBControlEnable = 26,
                    USBControlControl = 21,
                    WatchDog_Done = 13,
                    WatchDog_Wake = 16
            )
        except:
            self.sc_loaded = False
            self.ina = INA219(0.1, address=0x45)
            self.ina.configure()
        self.cpu = cpuFreq()
        self.available_frequencies = self.cpu.available_frequencies

    # returns current in mA
    def current(self) -> float:
        current = (self.sc.readChannelCurrentmA(sdl.SunControl_OUTPUT_CHANNEL)
                   if self.sc_loaded else self.ina.current())
        return round(current, 2)

    # returns voltage in V
    def voltage(self) -> float:
        voltage = (self.sc.readChannelVoltageV(sdl.SunControl_OUTPUT_CHANNEL)
                   if self.sc_loaded else self.ina.voltage())
        return round(voltage, 2)

    # returns power in W
    def power(self) -> float:
        power = (self.voltage() * (self.current() / 1000) if self.sc_loaded
                 else self.ina.power() / 1000)
        return round(power, 2)

    # returns frequency in kHz
    def frequency(self) -> int:
        return self.cpu.get_frequencies()[0]

    # returns the index of self.frequency() from self.available_frequencies
    def frequency_index(self) -> int:
        return self.available_frequencies.index(self.frequency())

    # sets maximum frequency in kHz
    def set_max_frequency(self, frequency) -> None:
        self.cpu.set_max_frequencies(frequency)

    # return the cpu utilization measured over 1 second
    def cpu_util(self) -> float:
        return psutil.cpu_percent(1)
