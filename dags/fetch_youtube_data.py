import os
import json
import logging
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv("dags/.env")
api_key = os.environ.get("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=api_key)

def fetch_function():
    data_folder = "/opt/airflow/data"
    topic_file_path = os.path.join(data_folder, "topics.txt")
    json_folder = os.path.join(data_folder, "json_files")
    os.makedirs(json_folder, exist_ok=True)
    
    check_file = os.path.exists(topic_file_path)
    if check_file:
        topic_lst = []
        with open(topic_file_path, 'r') as file:
            line = file.readline()
            while line:
                topic_lst.append(line.strip())
                line = file.readline()
        
        logging.info("Successfully read topics from topic.txt")        

        # I want to define a function to fetch data from youtube for each topic
        for topic in topic_lst:
            videos = fetch_topic_youtube_data(topic)
            video_info = fetch_video_details(videos)

            json_file_path = os.path.join(json_folder, f'{topic}.json')
            with open(json_file_path, 'w') as file:
                json.dump(video_info, file)
            print(f"Data for {topic} has been fetched and saved to {json_file_path}")

    else:
        logging.error("File not found")

def fetch_topic_youtube_data(topic,max_results=100):

    # Fetch videos until max_results is reached or there are no more results
    video_ids = []
    next_page_token = ""
    total_results_fetched = 0

    while total_results_fetched < max_results:
        logging.info(f"Fetching data for {topic} with {total_results_fetched} results fetched so far")
        
        request = youtube.search().list(
            part="snippet",
            q=topic,
            type='video',
            maxResults=50,
            pageToken=next_page_token or None,
        )
        response = request.execute()

        for item in response.get("items", []):
            video_id = item["id"].get("videoId")
            if video_id:
                video_ids.append(video_id)
                total_results_fetched += 1

                if total_results_fetched >= max_results:
                    break

        next_page_token = response.get("nextPageToken")

        if not next_page_token:  # Stop if there are no more pages
            break
    logging.info(f"Finished fetching data for {topic}: {len(video_ids)} videos")
    return video_ids

def fetch_video_details(videos, length=100):

    next_page_token = ""
    video_details = []
    video_ids = videos
    
    # Extract all the keys in the dictionary into a list
    request_limit = 50

    logging.info(f"Fetching video details for {len(video_ids)} videos")

    details = {'snippet': ['title', 'description','publishedAt'],
                'statistics': ['viewCount', 'likeCount', 'commentCount']
    }

    for i in range(0, len(video_ids), request_limit):
        call = video_ids[i:i+request_limit]
        logging.info(f"Processing batch {i // request_limit + 1}: {len(call)} videos")

        video_request = youtube.videos().list(
                part="snippet,statistics",
                id=','.join(call),
                maxResults=request_limit,  # Ensures only 50 videos per request
            )

        video_list_response = video_request.execute()

        for item in video_list_response.get('items', []):
            video_data = {}
            
            for part, keys in details.items():
                for key in keys:
                    value = item.get(part, {}).get(key, '')
                    video_data[key] = value

            video_data['video_id'] = item.get('id', '')
            video_data['url'] = f"https://www.youtube.com/watch?v={item.get('id', '')}"
            
            # Add the video data to the result list
            video_details.append(video_data)

    logging.info(f"Finished fetching details for {len(video_details)} videos")

    return {
        'items': video_details
    }