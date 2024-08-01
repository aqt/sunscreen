"""Interface to hardware (light sensor & monitors)"""

from monitorcontrol import get_monitors
import logging
import serial
import time


class HardwareInterface:
    def __init__(self, serial_port):
        self.logger = logging.getLogger(__name__)
        self.serial = None
        self.port = serial_port

    def open_serial(self):
        self.logger.debug("Connecting to serial")

        while True:
            try:
                self.serial = serial.Serial(self.port, timeout=1)
                break
            except serial.SerialException as e:
                self.logger.warn(e)
                time.sleep(5)

    def read_lumi(self):
        read_command = b"L"
        self.logger.debug("MCU <- " + str(read_command))
        self.serial.write(read_command)
        read = self.serial.readline()
        self.logger.debug(f"MCU -> {read}")
        return int(read)

    def set_brightness(self, brightness):
        self.logger.debug(f"Setting brightness {brightness}")

        for monitor in get_monitors():
            with monitor:
                monitor.set_luminance(brightness)

    def fade_to_brightness(self, start, target, step, interval):
        self.logger.debug(f"Fade from {start} to {target}")

        monitors = get_monitors()

        i = start

        while i != target:
            if i < target:
                i = min(i + step, target)
            else:
                i = max(i - step, target)

            for monitor in monitors:
                with monitor:
                    monitor.set_luminance(i)

            time.sleep(interval)

        self.logger.debug("Fade ended")

    def collect_samples(self, previous_lumi, samples, interval):
        self.logger.debug("Started collecting samples")

        if self.serial is None:
            self.open_serial()

        collected = []

        samples_remaining = samples

        while True:
            try:
                lumi = self.read_lumi()
            except serial.SerialException as e:
                self.logger.warn(e)
                self.open_serial()
                continue

            collected.append(lumi)
            samples_remaining -= 1

            if lumi == previous_lumi:
                self.logger.debug("Sample equals current lumi, ending collection early")
                break

            if samples_remaining <= 0:
                break

            time.sleep(interval)

        avg = round(sum(collected) / len(collected))
        self.logger.debug(f"Average is {avg}")
        return avg
