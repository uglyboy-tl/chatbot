from __future__ import annotations

import json
import uuid
from pathlib import Path

import requests
from config import minimax_api_key, minimax_group_id


def upload_audio_file(file_path: str) -> str:
    # 复刻音频上传
    url = f"https://api.minimax.chat/v1/files/upload?GroupId={minimax_group_id}"
    headers = {"authority": "api.minimax.chat", "Authorization": f"Bearer {minimax_api_key}"}
    data = {"purpose": "voice_clone"}
    files = {"file": Path(file_path).open("rb")}
    response = requests.post(url, headers=headers, data=data, files=files)
    file_id = response.json().get("file").get("file_id")
    print(file_id)
    return file_id


def clone_voice(file_path: str, voice_id: str | None = None):
    if not voice_id:
        voice_id = str(uuid.uuid4())
        print(voice_id)
    # 音频复刻
    url = f"https://api.minimax.chat/v1/voice_clone?GroupId={minimax_group_id}"
    payload2 = json.dumps({"file_id": upload_audio_file(file_path), "voice_id": voice_id})
    headers2 = {"Authorization": f"Bearer {minimax_api_key}", "content-type": "application/json"}
    response = requests.request("POST", url, headers=headers2, data=payload2)
    print(response.text)


if __name__ == "__main__":
    clone_voice("test.m4a")
