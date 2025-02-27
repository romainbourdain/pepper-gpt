import os
import qi
import paramiko
import time

channels = [0, 0, 1, 0]
sample_rate = 16000
recording_time = 5

class PepperInterface:
    def __init__(self):
        self.app = qi.Application(["GetAudio", f"--qi-url=tcp://{os.getenv('PEPPER_IP')}:{os.getenv('PEPPER_PORT')}"])
        self.app.start()
        self.session = self.app.session

        self.audio_recorder = self.session.service("ALAudioRecorder")
        self.tts = self.session.service("ALTextToSpeech")

    def record_audio(self, audio_path: str):
        self.audio_recorder.stopMicrophonesRecording()

        print("recording audio...")
        self.audio_recorder.startMicrophonesRecording(audio_path, "wav", sample_rate, channels)
        time.sleep(recording_time)
        self.audio_recorder.stopMicrophonesRecording()
        print("audio recording complete")

    def download_audio(self, remote_audio_path: str, local_audio_path: str):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            client.connect(hostname=os.getenv("PEPPER_IP"), username=os.getenv("PEPPER_USERNAME"), password=os.getenv("PEPPER_PASSWORD"))
            sftp = client.open_sftp()
            sftp.get(remote_audio_path, local_audio_path)
            sftp.close()
            print(f"📥 Fichier récupéré avec succès !")
        except Exception as e:
            print(f"❌ Erreur lors du transfert : {e}")
        finally:
            client.close()

    def say(self, text: str):
        self.tts.say(text)