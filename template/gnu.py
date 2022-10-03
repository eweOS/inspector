from __future__ import annotations
from bs4 import BeautifulSoup
import requests
from .tool.iter_flist import Flist

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

    flist = Flist(
        f"{name}-({version_regex}{includes_regex}){extension_regex}",
        r"%Y-%m-%d %H:%M",
    )

    content = requests.get(url).text
    soup = BeautifulSoup(content, "html.parser")
    for tr in soup.body.table.find_all("tr"):
        for td in tr.find_all("td"):
            a = td.find("a")
            filename = ""
            if a is not None:
                filename = a["href"]
            flist.update(filename, td.text)
    min_ver = flist.read()
    return {"version": min_ver.replace("-", "_")}


if __name__ == "__main__":
    print(get(name="bison"))
