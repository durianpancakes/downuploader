# downuploader

A tool to upload videos from a list of urls.
The guide below is written for Windows users using Windows Powershell.

## Setting up
downuploader requires Python 3+ to run. Please ensure that your computer has Python 3+ installed.
To verify:
```
python3 --version
```
Expected output:
```
Python 3.9.1
```
You will also require the use of pip. Please ensure that your computer has pip installed.
To verify:
```
pip3 --version
```
Expected output:
```
pip 20.2.3 from C:\... (python 3.9)
```
After ensuring that you have both Python and pip installed, you will need to install the following modules on your computer:
```
git clone https://github.com/durianpancakes/downuploader.git
pip3 install pytube
pip3 install --upgrade google-api-python-client
pip3 install --upgrade google-auth-oauthlib google-auth-httplib2
```
As downuploader calls on Google's YouTube Data API V3, you will require `client_secrets.json` in order for downuploader to make API calls on your behalf. Follow Step 1 in the following link: (https://developers.google.com/youtube/v3/quickstart/python), specifically, "2(b) Create an OAuth 2.0 client ID".

Finally, create a `url_inputs.txt` file in the same directory as downuploader.py. Insert urls in the following form:
```
https://www.youtube.com/watch?v=0PFxuMo0_JM&t=460s
https://www.youtube.com/watch?v=0aDHA2J1APs
```
You are now ready to run downuploader! 

### Using downuploader
Run downuploader with the following command:
```
python3 downuploader.py
```
Sample output:
```
Welcome to downuploader!
==================================================
Looking for url_inputs.txt in C:\Users\Razer\Documents\downuploader
url_inputs.txt found
Found 0 entries
Looking for client_secret.json
client_secret.json exists
Initializing authentication
Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=...
Enter the authorization code:
```
Ensure that you are logging in to a YouTube channel account, if not, the tool will not work. 
Once the authorization code is entered, downuploader will start to process the urls you provided in `url_inputs.txt`. 
downuploader will always attempt to download at 1080p30. However, in the event that the video does not have such an option, it will attempt to download at the next best quality (i.e 720p30). 

downuploader will then upload at the same quality, together with the same title and description as the source video. Uploaded videos are set to be public by default.

### Issues/Suggestions
If there are any issues/suggestions with the application, simply create an issue on the issue tracker and I will try my best to address them as soon as possible.


