""""Reads user preferences"""

import configparser


class Config:
    def __init__(self, file_path):
        self.__config = configparser.ConfigParser()
        self.__config.read(file_path)

        GENERAL = "general"
        SAMPLING = "sampling"
        ADJUSTMENT = "adjustment"

        self.log_level = self.__get_str(GENERAL, "log_level")
        self.serial_port = self.__get_str(GENERAL, "serial_port")

        self.samples = self.__get_int(SAMPLING, "samples")
        self.sampling_interval = self.__get_int(SAMPLING, "sampling_interval") / 1e3

        self.adjustment_interval = self.__get_int(ADJUSTMENT, "adjustment_interval")
        self.brightness_multiplier = self.__get_float(ADJUSTMENT, "brightness_multiplier")
        self.forced_adjustment_delay = self.__get_int(
            ADJUSTMENT, "forced_adjustment_delay"
        )
        self.fade_interval = self.__get_int(ADJUSTMENT, "fade_interval") / 1e3
        self.fade_step_size = self.__get_int(ADJUSTMENT, "fade_step_size")
        self.minimum_lumi_step = self.__get_int(ADJUSTMENT, "minimum_lumi_step")

    def __get_str(self, section, key):
        return self.__config[section][key]

    def __get_int(self, section, key):
        return int(self.__config[section][key])

    def __get_float(self, section, key):
        return float(self.__config[section][key])
