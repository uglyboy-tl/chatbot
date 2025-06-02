# 本项目是一个语音聊天助手的相关 Demo 代码

- main.py 是入口文件，命令行可以聊天（如果系统中安装了 mpv，可以实时语音播放，需要注意 mpv 的位置，在 linux 下进行过测试），包括文本输入和语音输出。
  - 使用时需要通过环境变量设置 OpenAI 的 baseurl 和 api_key (因为大部分模型都兼容 openai sdk，所以可以通过 baseurl 来调整使用的模型，记得修改 LLM 实例化时的模型名)
- 功能模块：
  - llm.py 是 模型类，根据需求修改 system prompt。支持流式输出，可以让生成内容较长的对话提前进行语音转换。
    - 当前默认支持 QWen 系列模型的联网搜索功能（细节见官方文档）；
    - 如果使用 OpenRouter，可以通过在模型名称后添加 `:online` 支持联网功能（细节见官方文档）；
  - tts.py 使用 MiniMax 的语音接口，需要在环境变量中设置 MINIMAX_GROUPID 和 MINIMAX_APIKEY，实例化时按需求调整调用的语音（例如克隆的语音）
  - clone.py 是 MiniMax 的语音克隆接口，每次调用价格为 9.9 元。这个模块我没做详尽的测试（因为测试需要花比较多的钱，哈哈）
  - list_voice.py 可以查看当前已经克隆的声音列表。
  - example 文件夹（一些可能能用得上的代码）：
    - asr.py 是 Azure 的语音识别模型的实现。还可以尝试本地化的方案：Whisper 或 FunASR，对应代码请自行搜索；
    - edge_tts.py 是使用 edge 的语音接口实现的 TTS 模块，免费，效果不错。如果不需要自定义语音可以尝试这个方案；
    - edge_tts2.py 是另一个 edge 的 TTS 模块，不需要将生成的语音保存为文件，而是可以直接将音频字节流，进行播放，但是每段音频开头都有一个爆破音；

通常语音助手可能还需要一个“唤醒词”模块，开源领域一般使用：picovoice 或 snowboy。其中使用 picovoice 一般是用 picovoice 提供的默认唤醒词。snowboy 会稍微复杂一些。