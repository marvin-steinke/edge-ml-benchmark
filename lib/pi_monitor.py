from lib import SDL_Pi_SunControl as sdl
import psutil
from cpufreq import cpuFreq

class PiMonitor():
    def __init__(self) -> None:
        # init SunControl
        self.sc = sdl.SDL_Pi_SunControl(
                INA3221Address = 0x40,
                USBControlEnable = 26,
                USBControlControl = 21,
                WatchDog_Done = 13,
                WatchDog_Wake = 16
        )
        self.cpu = cpuFreq()
        self.available_frequencies = self.cpu.available_frequencies

    # returns current in mA
    def current(self) -> float:
        return round(self.sc.readChannelCurrentmA(sdl.SunControl_OUTPUT_CHANNEL), 2)

    # returns voltage in V
    def voltage(self) -> float:
        return round(self.sc.readChannelVoltageV(sdl.SunControl_OUTPUT_CHANNEL), 2)

    # returns power in W
    def power(self) -> float:
        return round(self.voltage() * (self.current() / 1000), 2)

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
