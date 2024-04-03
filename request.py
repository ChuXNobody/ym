import requests

def convert_text_to_audio(text, voice="zh-CN-YunyangNeural", server_url="http://192.168.31.199:8000"):
    endpoint = server_url + "/convert/"
    data = {"text": text, "voice": voice}
    try:
        response = requests.post(endpoint, json=data)
        if response.status_code == 200:
            result = response.json()
            print("Audio conversion successful!")
            print("Output audio file:", result["output_file"])
            print("Output feature file:", result["output_feature_file"])
        else:
            print("Error:", response.status_code, response.text)
    except Exception as e:
        print("Error occurred:", e)

if __name__ == "__main__":
    text_input = input("Enter the text you want to convert to audio: ")
    convert_text_to_audio(text_input)
