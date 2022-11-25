from lib.pi_monitor import PiMonitor
from time import sleep
from subprocess import run
import sys

monitor = PiMonitor()
batch_sizes = [8, 16, 32, 48, 64]
frequencies = monitor.available_frequencies

for batch_size in batch_sizes:
    for frequency in frequencies:
        monitor.set_max_frequency(frequency)
        run(['python', 'client.py', sys.argv[1], str(batch_size), str(frequency / 1000)])
        sleep(5)
