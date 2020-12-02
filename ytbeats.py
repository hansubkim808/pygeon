import httplib2
import os
import random
import time
import socket
import apiclient.http

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

def _upload_to_request(request, progress_callback):
    """Upload a video to a Youtube request. Return video ID."""
    while 1:
        status, response = request.next_chunk()
        if status and progress_callback:
            progress_callback(status.total_size, status.resumable_progress)
        if response:
            if "id" in response:
                return response['id']
            else:
                raise KeyError("Expected field 'id' not found in response")

def yt_beats(video, thumbnail, metadata):
    CLIENT_SECRET_FILE = 'client_secrets.json'
    API_NAME = 'youtube'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    credentials = flow.run_console()
    youtube_object = build(API_NAME, API_VERSION, credentials = credentials)

    #service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    
    md = open(metadata, 'r')
    data = md.readlines()

    request_body = {
        'snippet': {
            'categoryId': 10,
            'title': data[0],
            'description': data[1],
            'tags': data[2].split(",")
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False, 
        },
        'notifySubscribers': False
    }

    mediaFile = MediaFileUpload(video)
    try:
        response_upload = youtube_object.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=mediaFile
        ).execute()

        youtube_object.thumbnails().set(
            videoId=response_upload.get('id'),
            media_body=MediaFileUpload(thumbnail)
        ).execute()
        upload_fun = lambda: _upload_to_request(request, progress_callback)
    except e:
        print(e.resp.status, e.content)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--video", help=".mp4 file to upload to YouTube")
    parser.add_argument("-tn", "--thumbnail", help=".jpg or .png file for video thumbnail")
    parser.add_argument("-md", "--metadata", help="title, description, tags, etc. for YouTube video")
    args = parser.parse_args()
    yt_beats(video=args.video, thumbnail=args.thumbnail, metadata=args.metadata)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print("Successfully uploaded video!")
