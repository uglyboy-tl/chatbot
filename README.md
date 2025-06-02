chat.py 是入口文件，命令行可以聊天（如果系统中安装了 mpv，可以实时语音播放，需要注意 mpv 的位置，在 linux 下进行过测试）
使用时需要通过环境变量设置 OpenAI 的 baseurl 和 api_key (因为大部分模型都兼容 openai sdk，所以可以通过 baseurl 来调整使用的模型，记得修改 LLM 实例化时的模型名)
llm.py 是 模型类，根据需求修改 system prompt
tts.py 使用 MiniMax 的语音接口，需要在环境变量中设置 MINIMAX_GROUPID 和 MINIMAX_APIKEY，实例化时按需求调整调用的语音（例如克隆的语音）
clone.py 是 MiniMax 的语音克隆接口，每次调用价格为 9.9 元。这个模块我没做详尽的测试（因为测试需要花比较多的钱，哈哈）
list_voice.py 可以查看当前已经克隆的声音列表。
asr.py 是语音识别模型，这个按照调用的服务商或本地搭建的环境来修改，我这里未对其进行功能实现。