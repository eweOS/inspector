from __future__ import annotations
from bs4 import BeautifulSoup
import requests
import re

enabled = True


def get(name="", version_regex="[0-9]+(\.[0-9]+)*"):

    url = f"https://www.netfilter.org/projects/{name}/downloads.html"
    content = requests.get(url).text
    soup = BeautifulSoup(content, "html.parser")
    update_name = (
        soup.body.find_all("div", class_="webpage")[0]
        .table.tr.find_all("td", class_="main")[0]
        .div.find_all("div", class_="section")[0]
        .div.div.div.h3.a["name"]
        .strip()
    )
    version = re.findall(f"{name}-({version_regex})", update_name)[0]
    if type(version) is tuple:
        version = version[0]
    return {"version": version}


if __name__ == "__main__":
    print(get(name="libmnl"))
