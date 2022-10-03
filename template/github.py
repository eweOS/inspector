from __future__ import annotations
import requests

enabled = True


def get(repo: str = "", type: str = "release", flags: list[str] = []) -> dict[str, str]:
    api_url = f"https://api.github.com/repos/{repo}"
    if type == "tag":
        tags = requests.get(f"{api_url}/tags").json()
        version = tags[0]["name"].lstrip("v")
    elif type == "release":
        releases = requests.get(f"{api_url}/releases").json()
        for release in releases:
            if (release["draft"] and "no_draft" in flags) or (
                release["prerelease"] and "no_prerelease" in flags
            ):
                continue
            version = release["tag_name"].lstrip("v")
    return {"version": version}


if __name__ == "__main__":
    print(get(repo="ivmai/bdwgc"))
