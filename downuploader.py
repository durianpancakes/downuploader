from pytube import YouTube
from googleapiclient.http import MediaFileUpload
from datetime import datetime

import googleapiclient.discovery
import googleapiclient.errors
import os
import google_auth_oauthlib.flow

dir_path = os.getcwd()
CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

print("Welcome to downuploader!")
print(50 * "=")

urls_list = []
failed_processing_list = []
success_counter = 0
current_time = datetime.now()
current_timestamp = str(current_time.year) + str(current_time.month) + str(current_time.day) + '_' + str(current_time.hour) + str(current_time.minute) + str(current_time.second)

def main():
    # Checking for url_inputs.txt
    try:
        print("Looking for url_inputs.txt in", dir_path)
        with open('url_inputs.txt') as file:
            print("url_inputs.txt found")
            urls_list = file.readlines()
            print("Found", len(urls_list), "entries")
    except (FileNotFoundError):
        print("ERROR: url_inputs.txt not found.")
        print("Please ensure that url_inputs.txt is in the same directory as downuploader!")
        return

    # Initializing Google OAuth 2.0
    print("Looking for client_secret.json")
    if (os.path.isfile('client_secret.json')):
        print("client_secret.json exists")
    else:
        print("client_secret.json does not exist, please place your client_secret.json in the same directory as downuploader!")
        return 

    print("Initializing authentication")
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        API_NAME, API_VERSION, credentials = credentials
    )
    print("Authentication completed")
    
    # Process the list of urls
    for i in range(len(urls_list)):
        print("Processing", i+1, "out of", len(urls_list))
        url = urls_list[i]
        video = download_video(url)

        if (video != None):
            try:
                upload_video(youtube, video)
                print("Upload successful")
                success_counter += 1
                delete_local_video()
            except (AttributeError):
                print("Upload failed. The url will be written to failed_urls", current_timestamp, ".txt in", dir_path)
                failed_processing_list.append(url)
        else:
            print("Download failed. The url will be written to failed_urls", current_timestamp, ".txt in", dir_path)
            failed_processing_list.append(url)

    num_failures = len(failed_processing_list)
    if (num_failures > 0):
        with open("failed_urls", current_timestamp, ".txt", 'w') as file:
            for url in failed_processing_list:
                file.write("%s\n" & url)

    # Print summary
    print(success_counter, "out of", len(urls_list))
    
    if (num_failures > 0):
        print("There were", num_failures, "failures. Find the failures at failed_urls", current_timestamp, ".txt in", dir_path)
    else:
        print("All urls successfully processed!")
    
    print(50 * '=')
    
def delete_local_video():
    print("Deleting file...")
    os.remove(dir_path + "/tmp.mp4")
    print("File deleted")

def upload_video(youtube_api, video):
    print("Uploading video...")
    request = youtube_api.videos().insert(
        part='snippet, status',
        body={
            'snippet': {
                'title':video.title,
                'description': video.description
            },
            'status':{
                'privacyStatus': 'public'
            }
        },
        media_body = MediaFileUpload(dir_path + "/tmp.mp4")
    )
    response = request.execute()

def download_video(video_url:str):
    youtube = YouTube(video_url)
    downloaded = False

    print("Attempting to download", youtube.title, "by", youtube.author, "in 1080p")
    if (downloaded == False):
        try:
            youtube.streams.filter(progressive=False, file_extension='mp4', res='1080p').first().download(output_path=dir_path, filename="tmp")
            downloaded = True
        except AttributeError:
            print("No 1080p options found")
    
    if (downloaded == False):
        try:
            youtube.streams.filter(progressive=False, file_extension='mp4', res='720p').first().download(output_path=dir_path, filename="tmp")
            downloaded = True
        except AttributeError:
            print("No 720p options found")

    if (downloaded == True):
        print("Downloaded", youtube.title, "by", youtube.author, "successfully")
        return youtube
    else:
        return None

if __name__ == "__main__":
    main()
