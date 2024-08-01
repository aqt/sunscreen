import logging
import time
from hardware_interface import HardwareInterface
from config import Config


class SunScreen:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.config = Config("config.ini")

        logging.basicConfig(
            level=getattr(logging, self.config.log_level),
            format="%(asctime)s [%(levelname)-8s] %(name)s.%(funcName)s:%(lineno)d - %(message)s",
            datefmt="%H:%M:%S",
        )

        self.hardware = HardwareInterface(self.config.serial_port)

        self.last_adjustment_time = time.time()
        self.current_lumi = 0

    def run(self):
        self.hardware.open_serial()
        self.__set_initial_brightness()

        while True:
            time.sleep(self.config.adjustment_interval)

            lumi = self.hardware.collect_samples(
                self.current_lumi,
                self.config.samples,
                self.config.sampling_interval,
            )

            force_update = self.__is_adjustment_stale()
            passed_threshold = self.__is_lumi_past_threshold(lumi)

            if force_update:
                self.logger.debug("Previous adjustment is stale, focing update")
            elif not passed_threshold:
                self.logger.debug(
                    f"Not different enough ({self.current_lumi} to {lumi})"
                )

            if force_update or passed_threshold:
                self.last_adjustment_time = time.time()
                previous_brightness = self.__map_brightness(self.current_lumi)
                self.current_lumi = lumi
                new_brightness = self.__map_brightness(lumi)

                self.logger.info(
                    f"Adjusting brightness: {previous_brightness} -> {new_brightness}"
                )

                if self.config.fade_interval > 0:
                    self.hardware.fade_to_brightness(
                        previous_brightness,
                        new_brightness,
                        self.config.fade_step_size,
                        self.config.fade_interval,
                    )
                else:
                    self.hardware.set_brightness(new_brightness)

    def __map_brightness(self, lumi):
        # TODO: Map in config somehow
        return int(min(lumi * self.config.brightness_multiplier, 100))

    def __set_initial_brightness(self):
        self.current_lumi = self.hardware.read_lumi()

        self.logger.info(f"Initial luminosity set to {self.current_lumi}")

        self.hardware.set_brightness(self.__map_brightness(self.current_lumi))

    def __is_adjustment_stale(self):
        delay = self.config.forced_adjustment_delay
        return delay > 0 and (time.time() - self.last_adjustment_time) > delay

    def __is_lumi_past_threshold(self, lumi):
        return abs(lumi - self.current_lumi) >= self.config.minimum_lumi_step
