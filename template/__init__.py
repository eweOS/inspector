from __future__ import annotations
import json, requests
from bs4 import BeautifulSoup
import logging
import re
from pyalpm import vercmp


class NewInfo:
    def __init__(self) -> None:
        self.json = json
        self.requests = requests
        self.bfsoup = BeautifulSoup
        self.re = re
        self.vercmp = vercmp
        self.init_templates()

    def init_templates(self) -> None:
        from importlib import import_module
        from pathlib import Path

        self.__template = {}
        for f in Path(__file__).parent.glob("*.py"):
            if "__" not in f.stem:
                try:
                    m = import_module(f".{f.stem}", __package__)
                    if m.enabled:
                        self.__template[f.stem] = m.get
                    else:
                        logging.info(f"template {f.stem} disabled.")
                except:
                    logging.warning(f"template {f.stem} import failed.")
        del import_module, Path

    def use_template(self, info: dict) -> dict[str, str]:
        return self.__template[info.pop("function")](**info)
