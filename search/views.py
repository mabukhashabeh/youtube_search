from django.shortcuts import render, redirect
from django.conf import settings
from isodate import parse_duration
import requests


def search(request):
    context = {}
    # step 1 --> get video id from first api
    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        params = {
            'part': 'snippet',
            'q': request.POST.get('search'),  # query
            'maxResults': 9,
            'key': settings.YOUTUBE_DATA_API_KEY,
            'type': 'video'
        }

        res = requests.get(search_url, params=params) # response
        results = res.json()['items']
        videos_id = []

        for result in results:
            videos_id.append(result['id']['videoId'])

        if request.POST.get('submit') :
            return redirect(f'https://www.youtube.com/watch?v={videos_id[0]}')

        # step 2 --> get all video details
        videos_params = {
            'part': 'snippet, contentDetails',
            'key': settings.YOUTUBE_DATA_API_KEY,
            'id': ','.join(videos_id)  # videos id should be separated by comma
        }
        videos_response = requests.get(video_url, params=videos_params)
        videos_results = videos_response.json()['items']
        videos = []

        for video in videos_results:
            video_content = {
                'title': video['snippet']['title'],
                'id': video['id'],
                'duration': parse_duration(video['contentDetails']['duration']),
                'thumbnail': video['snippet']['thumbnails']['high']['url']
            }
            videos.append(video_content)

        context = {
            'videos': videos
        }

    return render(request, 'search.html', context)