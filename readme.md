# 宏原子机器人 speech2action 说明

## 环境
python环境参考requirements.txt 版本太旧dashscope不支持，实测3.9不行，也可以3.12环境下安装 openai dashscope pyaudio
 pyserial pyqt5 即可   
注意：电脑需要安装ffmpeg！！

## api
只充值了20元，用完了请联系本人或自行更换，LLM请使用Qwen-plus，因为充了10元的的token大礼包

## 报错
pyaudio在windows环境上有一个stream.start/stop的OS报错，后面有时间修复

## 使用流程
点击LLM，说“我现在很开心/生气/难过/平静” 对应四种状态
