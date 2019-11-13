import youtube_dl
import discord
import urllib.request
import urllib.parse
import re
import os

ydl_opts = {  # Settings for the downloader
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


def rename(ctx):  # renames file to song.mp3
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")
    return name  # returns original file name


def search(query):  # Takes user entered string and outputs a youtube URL
    search_q = urllib.parse.urlencode({"search_query" : query})
    html = urllib.request.urlopen("http://www.youtube.com/results?" + search_q)
    results = re.findall(r'href=\"\/watch\?v=(.{11})', html.read().decode())
    url = "http://www.youtube.com/watch?v=" + results[0]
    return url

