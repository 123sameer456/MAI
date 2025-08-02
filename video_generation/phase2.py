# face posting


# API ka response return karega



# //////////////////////////

import requests
import time

def upload_facebook_video_with_thumbnail(page_access_token, page_id, video_path, title, description, thumbnail_path, delay_minutes=10):
    """
    Facebook page pe video upload aur thumbnail set karne ke liye function.
    
    :param page_access_token: (str) Facebook Page Access Token
    :param page_id: (str) Facebook Page ID
    :param video_path: (str) Path to video file
    :param title: (str) Video title
    :param description: (str) Video description
    :param thumbnail_path: (str) Path to thumbnail image
    :param delay_minutes: (int) Kitne minutes baad schedule karna hai (default: 10 minutes)
    :return: API response as JSON
    """
    scheduled_time = int(time.time()) + (delay_minutes * 60)

    # **Step 1: Upload Video**
    url = f"https://graph.facebook.com/v18.0/{page_id}/videos"
    data = {
        "access_token": page_access_token,
        "title": title,
        "description": description,
        "published": "false",
        "scheduled_publish_time": scheduled_time
    }
    files = {"source": open(video_path, "rb")}

    response = requests.post(url, data=data, files=files)
    video_response = response.json()

    if "id" not in video_response:
        print("Error uploading video:", video_response)
        return video_response

    video_id = video_response["id"]
    print(f"✅ Video Uploaded! Video ID: {video_id}")

    # **Step 2: Upload Thumbnail**
    thumbnail_url = f"https://graph.facebook.com/v18.0/{video_id}/thumbnails"
    thumb_files = {"source": open(thumbnail_path, "rb")}
    thumb_data = {"access_token": page_access_token}

    thumb_response = requests.post(thumbnail_url, data=thumb_data, files=thumb_files)
    print("✅ Thumbnail Uploaded:", thumb_response.json())

    return video_response  # Return the main video response

# ✅ **🔥 Function Call Example**
PAGE_ACCESS_TOKEN = "EAAJjyT5QkOYBO4OfHiiLEoOXK5ybhKjggrPmEHs2aRyl5fdkKtCewLGoEtPMm7yjVO6wkF6owU6OYnbCOFDFKVv41O4x4RKqA41JGykDqnnphhrYIK66qt3NLSdWQIYhdLrbmBf0fTId0SLIy5ZAdmd53OzboGQV8yDQjRQBp6anIk6NjDdmjvA7WAVS2pvrwnvcbcQOEzZAbSDsOQld5dws54p08ZD"
VIDEO_PATH = "2.mp4"
PAGE_ID = "115318481173537"
THUMBNAIL_PATH = "thumbnail_3.jpg"
TITLE = " sam-1 Video with Custom Thumbnail"
DESCRIPTION = "Tsame-1 his video has a custom thumbnail."
DELAY_MINUTES = 15  # Schedule after 15 minutes



response = upload_facebook_video_with_thumbnail(PAGE_ACCESS_TOKEN, PAGE_ID, VIDEO_PATH, TITLE, DESCRIPTION, THUMBNAIL_PATH, DELAY_MINUTES)
print(response)




# =============================================================================
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# =============================================================================


# import requests
# import time  # Timestamp ke liye


# PAGE_ACCESS_TOKEN = "EAAJjyT5QkOYBOx5osZABnoqWrWQp6sMIzbAKDSb0oPu4Jqb8ZBR3N7D1RAKwDavvAQXuZBCsAMWZCi5ZBTpddqMcfMZBuvOCv88iMhux4t7XLQGZARzfDwGVKPMT3HXxIBjeKDoA2MrBXSsyKRS3xKxW7bMkQZBQTPZCrSz49boKjUp1ZBZCWcHLwAKXzKN258ZC1eoeqf7b5HDdOmazvUZA2zrvrmrtVo6ZAu9mdU"
# VIDEO_PATH = "1.mp4"
# PAGE_ID = "115318481173537"

# # 🔥 At least 10 minutes (600 seconds) ahead in UTC time
# scheduled_time = int(time.time()) + 600  # (Current Time + 600 seconds = 10 min later)

# url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/videos"
# data = {
#     "access_token": PAGE_ACCESS_TOKEN,
#     "title": "Scheduled Video Title",
#     "description": "This video is scheduled for later.",
#     "published": "false",  # Scheduling ke liye false rakhna zaroori hai
#     "scheduled_publish_time": scheduled_time  # UNIX timestamp (UTC format)
# }
# files = {"source": open(VIDEO_PATH, "rb")}

# response = requests.post(url, data=data, files=files)
# print(response.json())


# # ap id : 1176312600888501
# # ap secret : fb22d4ab396fc61db0bc7b2bea6cdfb1 
# access token : 
# 