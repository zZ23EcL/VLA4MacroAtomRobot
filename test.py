import pyaudio

p = pyaudio.PyAudio()

print("可用音频设备列表：")
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"设备索引: {i}, 名称: {info['name']}, 输入通道: {info['maxInputChannels']}")

p.terminate()
