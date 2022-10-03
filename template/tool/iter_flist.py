import re
from datetime import datetime


# This is used to deal with some tough circumstances
# When we have to parse a list of files to get the latest version.
# Init flist object before iteration, and use update() to update
# time and version. They are not required to be valid, thus a lot
# of validations can be unnecessary.

class Flist:
    def __init__(
        self,
        file_regex: str,
        time_type: str,
    ) -> None:
        self.min_time = datetime.min
        self.min_ver = ""
        self.time_type = time_type
        self.regex_obj = re.compile(file_regex)
        self.cache_time = datetime.min
        self.cache_ver = ""

    def update(self, file_name: str, time_str: str) -> None:
        self.update_time(time_str)
        self.process()
        self.update_ver(file_name)
        self.process()

    def update_time(self, time_str: str) -> None:
        try:
            self.cache_time = datetime.strptime(time_str.strip(), self.time_type)
        except:
            pass

    def update_ver(self, file_name: str) -> None:
        try:
            finding = self.regex_obj.findall(file_name)
            version = finding[0]
            if type(version) is tuple:
                version = version[0]
            self.cache_ver = version
        except:
            pass

    # When the time object and version are both valid,
    # compare, save and remove cache
    def process(self) -> None:
        if self.cache_ver and self.cache_time != datetime.min:
            if self.cache_time > self.min_time:
                self.min_time = self.cache_time
                self.min_ver = self.cache_ver
            self.cache_ver = ""
            self.cache_time = datetime.min

    def read(self) -> str:
        return self.min_ver
