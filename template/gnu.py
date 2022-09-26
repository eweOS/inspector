from __future__ import annotations
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime

enabled = True

def get(
    name: str = "",
    extension_regex="\.tar\.[a-z]+",
    included: str = "",
    version_regex="[0-9]+(\.[0-9]+)*",
) -> dict[str, str]:
    url = f"https://ftp.gnu.org/gnu/{name}/"

    includes = ["alpha", "beta", "rc"]
    try:
        includes = includes[includes.index(included) :]
        includes = [f"({include})" for include in includes]
        includes_regex = "-(" + "|".join(includes) + ")[1-9]*"
    except:
        includes_regex = ""

    file_regex = re.compile(
        f"{name}-({version_regex}{includes_regex}){extension_regex}"
    )

    min_time = datetime.min
    min_ver = ""

    content = requests.get(url).text
    soup = BeautifulSoup(content, "html.parser")
    for tr in soup.body.table.find_all("tr"):
        time_obj = min_time
        filename = ""
        for td in tr.find_all("td"):
            a = td.find("a")
            if a is not None:
                filename = a["href"]
            if re.match(r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}", td.text):
                time = td.text.strip()
                time_obj = datetime.strptime(time, r"%Y-%m-%d %H:%M")
            if time_obj >= min_time and file_regex.match(filename):
                min_ver = file_regex.findall(filename)[0]
                if type(min_ver) is tuple:
                    min_ver = min_ver[0]
    return {"version": min_ver.replace("-", "_")}


if __name__ == "__main__":
    print(get(name="bison"))
