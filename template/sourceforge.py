from __future__ import annotations
import requests
import re


def get(
    name: str = "",
    platform_release: str = "linux",
    force_platform: bool = False,
    version_regex: str = "[0-9]+(\.[0-9]+)*",
    extension_regex: str = "\.tar\.((xz)|(gz)|(lz4)|(zst)|(bz4))",
    file_regex: str = "",
):
    api_url = f"https://sourceforge.net/projects/{name}/best_release.json"

    if not file_regex:
        file_regex = f"{name}-({version_regex}){extension_regex}"

    result = requests.get(api_url).json()

    try:
        file_path = result["platform_releases"][platform_release]["filename"]
    except KeyError:
        if force_platform:
            raise Exception("No specified platform")
        file_path = result["release"]["filename"]

    version = re.findall(file_regex, file_path)[0]
    if type(version) is tuple:
        version = version[0]
    return {"version": version}


if __name__ == "__main__":
    print(get(name="e2fsprogs"))
