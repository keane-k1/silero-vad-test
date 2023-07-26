import os

def add_wav_header_to_pcm_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".pcm"):
                pcm_file_path = os.path.join(root, file)
                wav_file_path = pcm_file_path[:-3] + "wav"
                with open(pcm_file_path, 'rb') as pcm_file:
                    pcm_data = pcm_file.read()
                with open(wav_file_path, 'wb') as wav_file:
                    wav_file.write(b'RIFF')
                    wav_file.write((len(pcm_data) + 36).to_bytes(4, byteorder='little'))
                    wav_file.write(b'WAVE')
                    wav_file.write(b'fmt ')
                    wav_file.write((16).to_bytes(4, byteorder='little'))
                    wav_file.write((1).to_bytes(2, byteorder='little'))
                    wav_file.write((1).to_bytes(2, byteorder='little'))
                    wav_file.write((16000).to_bytes(4, byteorder='little'))
                    wav_file.write((32000).to_bytes(4, byteorder='little'))
                    wav_file.write((2).to_bytes(2, byteorder='little'))
                    wav_file.write((16).to_bytes(2, byteorder='little'))
                    wav_file.write(b'data')
                    wav_file.write((len(pcm_data)).to_bytes(4, byteorder='little'))
                    wav_file.write(pcm_data)


add_wav_header_to_pcm_files("./samples")