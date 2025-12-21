import os
import sys
# Inject NAOqi SDK path before importing naoqi (Python 2)
SDK_PATH = os.environ.get('PYNAOQI_PATH', '/Users/heidi/Downloads/pynaoqi-python2.7-2.8.6.23-mac64-20191127_144231')
sys.path.insert(0, os.path.join(SDK_PATH, 'lib', 'python2.7', 'site-packages'))
from naoqi import ALProxy
import time
import io

# Set the IP address and port of your NAO robot
nao_ip = "10.1.95.105"
nao_port = 9559

# Create an ALTextToSpeech proxy
try:
    # Create an ALTextToSpeech proxy
    tts = ALProxy("ALTextToSpeech", nao_ip, nao_port)
except Exception as e:
    print("Error initializing ALTextToSpeech proxy: %s" % e)
file_content=""
# Set the text content you want NAO to say
file_path="./output_text.txt"
try:
    with io.open(file_path, 'r', encoding='utf-8-sig') as file:
        file_content = file.read().strip()
except Exception as e:
    print("Error reading file: %s" % e)
    

try:
    text_u = file_content if isinstance(file_content, unicode) else unicode(file_content, 'utf-8', 'ignore')
except Exception:
    text_u = unicode(file_content)
try:
    has_non_ascii = any(ord(c) > 127 for c in text_u)
    if has_non_ascii:
        tts.setLanguage('Chinese')
    else:
        tts.setLanguage('English')
except Exception:
    pass
tts.say(text_u)

# Wait for the speech to finish
time.sleep(5)  # Adjust the sleep duration based on the length of the speech

# Release the proxy
