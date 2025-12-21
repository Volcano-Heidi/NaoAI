import os
import sys
import paramiko

SDK_PATH = os.environ.get('PYNAOQI_PATH', '/Users/heidi/Downloads/pynaoqi-python2.7-2.8.6.23-mac64-20191127_144231')
sys.path.insert(0, os.path.join(SDK_PATH, 'lib', 'python2.7', 'site-packages'))
from naoqi import ALProxy

# Replace these with your robot's IP address and port
robot_ip = os.environ.get('NAO_IP', "10.1.95.105")
robot_port = int(os.environ.get('NAO_PORT', '9559'))
robot_user = os.environ.get('NAO_USER', 'nao')
robot_pass = os.environ.get('NAO_PASS', 'nao')

# Create a proxy to ALPhotoCapture
try:
    photoCaptureProxy = ALProxy("ALPhotoCapture", robot_ip, robot_port)
except Exception as e:
    print "Error when creating ALPhotoCapture proxy:"
    print str(e)
    sys.exit(0)

# Set the camera resolution and picture format
photoCaptureProxy.setResolution(2)  # 2 corresponds to VGA resolution
photoCaptureProxy.setPictureFormat("jpg")

# Specify the folder and file name for the captured picture
folder_path = "/home/nao/recordings/cameras/"
file_name = "captured_image.jpg"

# Take a picture and save it to the specified folder (single shot)
try:
    # Prefer single-shot API; falls back silently if not available
    if hasattr(photoCaptureProxy, 'takePicture'):
        photoCaptureProxy.takePicture(folder_path, file_name)
    else:
        photoCaptureProxy.takePictures(1, folder_path, file_name)
except Exception as e:
    print "Error taking picture:"
    print str(e)
    sys.exit(0)

print "Picture taken and saved to {}{}".format(folder_path, file_name)

def send_to_pc():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    except Exception:
        pass
    try:
        ssh.connect(robot_ip, username=robot_user, password=robot_pass)
        sftp = ssh.open_sftp()
        remote_path=  "/home/nao/recordings/cameras/captured_image.jpg"
        local_path = r'./image.jpg'
        sftp.get(remote_path,local_path)
        sftp.close()
        ssh.close()
    except Exception as e:
        print "Error transferring file via SFTP:"
        print str(e)

send_to_pc()