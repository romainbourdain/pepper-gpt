import os
import time

import paramiko
import qi

channels = [0, 0, 1, 0]
sample_rate = 16000
recording_time = 5


class PepperInterface:
    def __init__(self) -> None:
        try:
            self.app = qi.Application(
                [
                    "GetAudio",
                    f"--qi-url=tcp://{os.getenv('PEPPER_IP')}:{os.getenv('PEPPER_PORT')}",
                ]
            )
            self.app.start()
            self.session = self.app.session

            self.audio_recorder = self.session.service("ALAudioRecorder")
            self.tts = self.session.service("ALTextToSpeech")
        except Exception as e:
            print(f"❌ Erreur lors de la connexion à Pepper : {e}")

    def record_audio(self, audio_path: str):
        try:
            self.audio_recorder.stopMicrophonesRecording()

            print("recording audio...")
            self.audio_recorder.startMicrophonesRecording(
                audio_path, "wav", sample_rate, channels
            )
            time.sleep(recording_time)
            self.audio_recorder.stopMicrophonesRecording()
            print("audio recording complete")
        except Exception as e:
            print(f"❌ Erreur lors de l'enregistrement audio : {e}")

    def download_audio(self, remote_audio_path: str, local_audio_path: str):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            client.connect(
                hostname=os.getenv("PEPPER_IP"),
                username=os.getenv("PEPPER_USERNAME"),
                password=os.getenv("PEPPER_PASSWORD"),
            )
            sftp = client.open_sftp()
            sftp.get(remote_audio_path, local_audio_path)
            sftp.close()
            print("📥 Fichier récupéré avec succès !")
        except Exception as e:
            print(f"❌ Erreur lors du transfert : {e}")
        finally:
            client.close()

    def say(self, text: str):
        try:
            self.tts.say(text)
        except Exception as e:
            print(f"❌ Erreur lors de la lecture du texte : {e}")
