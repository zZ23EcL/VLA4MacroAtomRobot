import os
import sys
from openai import OpenAI
import threading
import pyaudio
import dashscope
from dashscope.audio.asr import *
import signal  # for keyboard events handling (press "Ctrl+C" to terminate recording and translation)
from text2speech import    synthesis_text_to_speech_and_play_by_streaming_mode
from text2action import    Text2Aciton
mic = None
stream = None
stream_on = False

# Set recording parameters
sample_rate = 16000  # sampling rate (Hz)
channels = 1  # mono channel
dtype = 'int16'  # data type
format_pcm = 'pcm'  # the format of the audio data
block_size = 3200  # number of frames per buffer

#文本模型
myLLM=Text2Aciton()

# 全局状态
State=0
def init_dashscope_api_key():
    """
        Set your DashScope API-key. More information:
        https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """

    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ[
            'DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        dashscope.api_key = 'sk-fa5d1a77deb04894aa7f1b6984589214'  # set API-key manually


#这里是speech2text的callback
#在on_event中对完整的句子中的text处理，并且调用text2action以及text2speech
class Callback(RecognitionCallback):
    def on_open(self) -> None:
        global mic
        global stream
        print('RecognitionCallback open.')
        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16,
                          channels=1,
                          rate=16000,
                          input=True)

    def on_close(self) -> None:
        global mic
        global stream
        global stream_on
        print('RecognitionCallback close.')
        stream.stop_stream()
        stream.close()
        mic.terminate()
        stream = None
        mic = None
        stream_on = False

    def on_complete(self) -> None:
        print('RecognitionCallback completed.')  # translation completed

    def on_error(self, message) -> None:
        print('RecognitionCallback task_id: ', message.request_id)
        print('RecognitionCallback error: ', message.message)
        # Stop and close the audio stream if it is running
        if 'stream' in globals() and stream.active:
            stream.stop()
            stream.close()
        # Forcefully exit the program
        sys.exit(1)
    def on_event(self, result: RecognitionResult) -> None:
        global stream
        global State
        sentence = result.get_sentence()
        if 'text' in sentence:
            # print('RecognitionCallback text: ', sentence['text'])
            if RecognitionResult.is_sentence_end(sentence):
                # print(
                #     'RecognitionCallback sentence end, request_id:%s, usage:%s'
                #     % (result.get_request_id(), result.get_usage(sentence)))
                myLLM.user_input(sentence['text'])
                assistant_output = myLLM.get_response().choices[0].message.content
                myLLM.assistant_input(assistant_output)
                # 系统外放的时候需要关闭麦，不然会将外放的声音再输入
                # if stream.is_active():
                #     stream.stop_stream()  # 先检查是否活跃再停止
                # stream.stop_stream()  # 先检查是否活跃再停止
                synthesis_text_to_speech_and_play_by_streaming_mode(text=assistant_output)
                # stream.start_stream()
                # print(assistant_output)
                if "状态1" in assistant_output:
                    State=1
                if "状态2" in assistant_output:
                    State=2
                if "状态3" in assistant_output:
                    State=3
                if "状态4" in assistant_output:
                    State=4
                if "再见" in assistant_output:
                    self.on_close()
                assistant_output=[]
                # if "再见" in sentence['text']:
                #     stream_on = False
                #     self.on_close()
# 这里是model是一个speech2text，然后再text中调用text2text和text2speech
class speech2action():
    def __init__(self):
        init_dashscope_api_key()
        print('Initializing...')
        self.callback = Callback()
        self.recognition = Recognition(
        model='paraformer-realtime-8k-v2',
        # 'paraformer-realtime-v1'、'paraformer-realtime-8k-v1'
        format=format_pcm,
        # 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you can check the supported formats in the document
        sample_rate=sample_rate,
        # support 8000, 16000
        semantic_punctuation_enabled=False,
        callback=self.callback)
        # Start translation
        self.recognition.start()

    # def signal_handler(self,sig, frame):
    #     print('Ctrl+C pressed, stop translation ...')
    #     # Stop translation
    #     self.recognition.stop()
    #     print('Translation stopped.')
    #     print(
    #         '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
    #         .format(
    #             self.recognition.get_last_request_id(),
    #             self.recognition.get_first_package_delay(),
    #             self.recognition.get_last_package_delay(),
    #         ))
    #     # Forcefully exit the program
    #     sys.exit(0)

    def go(self):

        def run():
            while True:
                if stream:
                    data = stream.read(3200, exception_on_overflow=True)
                    self.recognition.send_audio_frame(data)
                else:
                    break
            self.recognition.stop()
            print('end')

        thread = threading.Thread(target=run)
        thread.start()


if __name__ == "__main__":
    myS2A = speech2action()
    myS2A.go()



