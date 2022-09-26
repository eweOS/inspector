from __future__ import annotations
import requests

enabled = False


def get(instance: str = "gitlab.com", repo: str = "", type: str = "release"):
    api_url=f"https://{instance}/api/v4/projects/{repo}/repository/"
