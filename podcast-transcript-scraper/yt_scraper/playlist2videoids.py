import requests
import csv
import os
import boto3
import logging
from dotenv import load_dotenv

load_dotenv()

YT_API_KEY = "AIzaSyBL84kZikSPm_vZ6l13RuUYriuRP47peGM"
# PLAYLIST_ID = "PLrAXtmErZgOdP_8GztsuKi9nrraNbKKp4"

logging.getLogger().setLevel(logging.INFO)


# Uploads folder files to S3 Bucket
def upload_file(file_path, filename):
    logging.info("S3 Put: {} {}".format(file_path, filename))
    session = boto3.Session(
        aws_access_key_id=os.getenv('AWS_SECRET_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION_NAME')
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket('podcast-transscripts')

    bucket.upload_file(file_path, filename)


def retrieve_videoids_from_playlist(playlist_id, folder_path):
    has_next_page = True
    next_page_token = ""
    videos = []

    logging.info("New playlist id: {}".format(playlist_id))
    logging.info("--------------------------")

    while has_next_page:
        url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2C+id&playlistId={}&key={}&maxResults=50".format(
            playlist_id, YT_API_KEY)
        if next_page_token:
            url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2C+id&playlistId={}&key={}&pageToken={}&maxResults=50".format(
                playlist_id, YT_API_KEY, next_page_token)

        # Retrieve request
        r = requests.get(url)
        res = r.json()

        if "nextPageToken" in res:
            next_page_token = res["nextPageToken"]
        else:
            has_next_page = False

        items = res["items"]

        for item in items:
            snippet = item["snippet"]
            logging.info("New video added: {}".format(
                snippet["resourceId"]["videoId"]))
            video_id = snippet["resourceId"]["videoId"]
            title = snippet["title"]
            published_at = snippet["publishedAt"]
            # description = snippet["description"]
            # thumbnail_url = snippet["thumbnail"]["url"]
            channel_title = snippet["channelTitle"]
            # defaultLanguage = snippet["defaultLanguage"]
            channel_id = snippet["channelId"]
            videos.append([video_id, title, published_at,
                           channel_title, channel_id])
    print(videos)
    return videos
