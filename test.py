import os
import sys
import pyaudio
import threading
import dashscope
from dashscope.audio.asr import *
from dashscope.common.error import InvalidParameter  # 确保正确导入

mic = None
stream = None
stop_flag = False  # 终止信号
recognition = None  # 识别对象

# 录音参数
sample_rate = 16000
block_size = 3200
format_pcm = 'pcm'


def init_dashscope_api_key():
    """设置 DashScope API Key"""
    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ['DASHSCOPE_API_KEY']
    else:
        dashscope.api_key = 'sk-fa5d1a77deb04894aa7f1b6984589214'


# 语音识别回调
class Callback(RecognitionCallback):
    def on_open(self) -> None:
        global mic, stream
        print('Recognition started.')
        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=block_size)

    def on_close(self) -> None:
        global mic, stream
        print('Recognition stopped.')
        if stream:
            stream.stop_stream()
            stream.close()
        if mic:
            mic.terminate()
        stream, mic = None, None

    def on_complete(self) -> None:
        print('Recognition complete.')

    def on_error(self, message) -> None:
        print('Error:', message.message)
        global stop_flag
        stop_flag = True  # 发生错误时终止程序

    def on_event(self, result: RecognitionResult) -> None:
        global stop_flag
        sentence = result.get_sentence()
        if 'text' in sentence:
            text = sentence['text']
            print('Recognized:', text)

            # 终止条件：检测到"再见"
            if "再见" in text:
                print("Detected '再见', stopping recognition...")
                stop_flag = True
                threading.Thread(target=self.stop_recognition).start()  # 在新线程中调用 stop()

    def stop_recognition(self):
        """在单独线程中安全地停止 recognition"""
        global recognition
        if recognition:
            try:
                recognition.stop()
                print("Recognition service stopped.")
            except Exception as e:
                print(f"Error while stopping recognition: {e}")


# 录音线程
def audio_capture():
    """持续录音并发送到 DashScope"""
    global stream, stop_flag
    while not stop_flag:
        if stream is not None:
            try:
                data = stream.read(block_size, exception_on_overflow=False)
                if not stop_flag:  # 确保在 stop 之后不会继续发送
                    recognition.send_audio_frame(data)
            except (InvalidParameter, OSError):
                print("Audio stream stopped due to recognition stop.")
                break  # 避免在服务关闭后继续发送数据
    print("Audio capture thread exiting...")


# 主程序
if __name__ == '__main__':
    init_dashscope_api_key()
    print('Initializing...')

    callback = Callback()
    recognition = Recognition(
        model='paraformer-realtime-v2',
        format=format_pcm,
        sample_rate=sample_rate,
        semantic_punctuation_enabled=False,
        callback=callback
    )

    recognition.start()
    print("Say '再见' to stop recording and translation...")

    # 启动录音线程
    audio_thread = threading.Thread(target=audio_capture)
    audio_thread.start()

    # 等待终止信号
    while not stop_flag:
        pass

    print("Stopping program...")

    # 确保所有资源释放
    recognition.stop()
    audio_thread.join()

    print("Program exited successfully.")
    sys.exit(0)  # 确保程序完全退出
