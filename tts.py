from __future__ import annotations

import json
import subprocess
import time
from collections.abc import Iterator
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path

import requests
from config import minimax_api_key, minimax_group_id

TONE: list[str] = ["处理/(chu3)(li3)", "危险/dangerous"]


@dataclass
class TTS:
    model: str = field(default="speech-02-turbo")
    voice_id: str = field(default="uglyboy_voice")
    file_format: str = field(default="mp3")  # 支持 mp3/pcm/flac
    url: str = field(default="https://api.minimax.chat/v1/t2a_v2?GroupId=" + minimax_group_id)
    audio_saved: bool = False

    @cached_property
    def headers(self) -> dict:
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "authorization": "Bearer " + minimax_api_key,
        }
        return headers

    def build_tts_stream_body(self, text: str) -> str:
        body = json.dumps(
            {
                "model": self.model,
                "text": text,
                "stream": True,
                "voice_setting": {"voice_id": self.voice_id, "speed": 1.0, "vol": 1.0, "pitch": 0},
                "pronunciation_dict": {"tone": TONE},
                "audio_setting": {"sample_rate": 32000, "bitrate": 128000, "format": "mp3", "channel": 1},
            }
        )
        return body

    @cached_property
    def player(self) -> subprocess.Popen:
        mpv_command = ["mpv", "--no-cache", "--no-terminal", "--", "fd://0"]
        return subprocess.Popen(
            mpv_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def call_tts_stream(self, text: str) -> Iterator[bytes]:
        tts_url = self.url
        tts_body = self.build_tts_stream_body(text)

        response = requests.request("POST", tts_url, stream=True, headers=self.headers, data=tts_body)
        for chunk in response.raw:
            if chunk:
                if chunk[:5] == b"data:":
                    data = json.loads(chunk[5:])
                    if "data" in data and "extra_info" not in data:
                        if "audio" in data["data"]:
                            audio = data["data"]["audio"]
                            yield audio

    def audio_play(self, audio_stream: Iterator[bytes]) -> bytes:
        audio = b""
        for chunk in audio_stream:
            if chunk is not None and chunk != "\n":
                decoded_hex = bytes.fromhex(str(chunk))
                self.player.stdin.write(decoded_hex)  # type: ignore
                self.player.stdin.flush()
                audio += decoded_hex

        return audio

    def save(self, audio, file_name: str | None = None):
        if not self.audio_saved:
            return
        if not file_name:
            timestamp = int(time.time())
            file_name = f"output_total_{timestamp}.{self.file_format}"
        with Path(file_name).open("wb") as file:
            file.write(audio)

    def play(self, text: str):
        audio = self.audio_play(self.call_tts_stream(text))
        self.save(audio)


if __name__ == "__main__":
    tts = TTS()
    # tts.play("真正的危险不是计算机开始像人一样思考，而是人开始像计算机一样思考。计算机只是可以帮我们处理一些简单事务。")
    tts.play("本示例以流式形式调用本接口，并流式播放；最终将保存完整音频文件。")
