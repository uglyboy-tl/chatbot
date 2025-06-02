from __future__ import annotations

from collections.abc import Iterator

from llm import LLM
from tts import TTS

llm = LLM()
tts = TTS()
message_history = []

while True:
    user_input = input("You: ")
    message_history.append({"role": "user", "content": user_input})
    response = llm.chat_bot(message_history)
    output = ""
    audio_text = ""
    if isinstance(response, Iterator):
        print("Bot: ", end="", flush=True)
        for chunk in response:
            print(chunk, end="", flush=True)
            output += chunk
            audio_text += chunk
            if "\n" in chunk:
                tts.play(audio_text.strip())
                audio_text = ""
        print()
        if audio_text.strip():
            tts.play(audio_text.strip())
    else:
        output = response.split("</thinking>")[-1]
    message_history.append({"role": "assistant", "content": output})
