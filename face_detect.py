import os
import sys
SDK_PATH = os.environ.get('PYNAOQI_PATH', '/Users/heidi/Downloads/pynaoqi-python2.7-2.8.6.23-mac64-20191127_144231')
sys.path.insert(0, os.path.join(SDK_PATH, 'lib', 'python2.7', 'site-packages'))
from naoqi import ALProxy

# Replace 'YourRobotIP' with the actual IP address of your NAO robot
robot_ip = os.environ.get('NAO_IP', "10.1.94.38")
port = int(os.environ.get('NAO_PORT', '9559'))  # Default port for NAOqi

# Create a proxy to ALFaceCharacteristics
face_characteristics_proxy = ALProxy("ALFaceCharacteristics", robot_ip, port)

# Example: Analyzing face characteristics of a person with ID 1
person_id = 1

# Perform face analysis on the given person using the ID
analysis_success = face_characteristics_proxy.analyzeFaceCharacteristics(person_id)

# if analysis_success:
print "Face analysis succeeded for person ID:", person_id

# Get smiling threshold
smiling_threshold = face_characteristics_proxy.getSmilingThreshold()
print "Current Smiling Threshold:", smiling_threshold

# Set a new smiling threshold (replace 0.8 with your desired value)
new_threshold = 0.8
face_characteristics_proxy.setSmilingThreshold(new_threshold)
print "Smiling Threshold set to:", new_threshold

# Listen for the event "FaceCharacteristics/PersonSmiling"
def on_person_smiling(event_name, value, message):
    person_id = value[0]
    print "Person", person_id, "is smiling!"

# Subscribe to the event
subscriber_identifier = "subscriber_identifier"
face_characteristics_proxy.subscribe("FaceCharacteristics/PersonSmiling", subscriber_identifier, "")

# Now, whenever a person smiles, the callback function will be invoked
# You can add your own logic in the callback function

# Unsubscribe when done (optional)
face_characteristics_proxy.unsubscribe("FaceCharacteristics/PersonSmiling", subscriber_identifier)

# else:
#     print "Face analysis failed for person ID:", person_id
