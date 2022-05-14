# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os, re, string
import googleapiclient.discovery
import urllib.parse as urlparse
from pprint import pprint
from VADER_analysis import Label_Data

class YouTubeCommentFile:
    
    def __init__(self, link):
        """
        Parameters
        ----------
        link : str
            the YouTube URL of the video
        """
        self.link = link
        self.video_id = self.parse_url()
        self.desired_maxResults = 100  # Default value for number of comments

        self.main()  # Run necessary functions for parsing YouTube comments

    def main(self):
        """ 
        Runs other functions to parse YouTube comments
        """
        response = self.request_commentThreads()
        comment_list = self.extract_textOriginal(response)
        self.write_to_file(comment_list)

    def parse_url(self):
        """ 
        Returns the videoID from the YouTube URL
        """
        url_data = urlparse.urlparse(self.link)
        query = urlparse.parse_qs(url_data.query)
        return query["v"][0]
    
    def request_commentThreads(self):
        """ Returns JSON formatted list of top relevant comments

        Returns
        -------
        dict
            a dict of the desire video comments
        """

        self.bound_maxResults()

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = "AIzaSyAnV1eECtyMWtfism9bsQQP81a3_gGUYjo"

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey = DEVELOPER_KEY)

        # Get list of top relevant comments
        request = youtube.commentThreads().list(
            part="snippet",
            maxResults=self.desired_maxResults,
            order="relevance",
            videoId=self.video_id,
        )

        response = request.execute()

        return response  # JSON response of top 100 relevant comments

    def bound_maxResults(self):
        """
        Ensures that the desired_maxResults within bounds of the YouTube API
        """
        if self.desired_maxResults <= 0:
            self.desired_maxResults = 1
        elif self.desired_maxResults > 100:
            self.desired_maxResults = 100

    def extract_textOriginal(self, response):
        """ Returns a list of the top 100 relevant comments

        Parameters
        ----------
        response : dict
            a dict of the desire video comments

        Returns
        -------
        list
            a list of the textOriginal comments
        """
        textOriginal_list = []
        comment_list = response['items']

        for com in comment_list:
            comment = com['snippet']['topLevelComment']['snippet']['textOriginal']
            textOriginal_list.append(comment)

        return textOriginal_list

    def write_to_file(self, comment_list):
        """
        Writes the list of comments to a file
        """
        with open(f'Data\Videos\YouTubeCommentList{self.video_id}.txt', mode='w', encoding='utf-8') as comment_file:
            for comment in comment_list:
                comment = re.sub('\s+', ' ', comment)
                comment_file.write('%s\n' % comment)

if __name__ == "__main__":
    #YouTubeCommentFile("https://www.youtube.com/watch?v=5Hxr9k5Vdc4")
    #YouTubeCommentFile("https://www.youtube.com/watch?v=YbJOTdZBX1g")
    YouTubeCommentFile("https://www.youtube.com/watch?v=aR3cw7jGRvI")