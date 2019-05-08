#coding=UTF-8

from pytube import YouTube
from pytube import Playlist
import urllib.request
import os

getcwd = os.getcwd()
def mkdir(path):
	os.makedirs(path)

def urllib_download(url, path):
	f = urllib.request.urlopen(url)
	data = f.read()
	with open(path, 'wb') as code:
		code.write(data)

def main():
	urlStr = input("Please input the url\n");
	print("Loading...")
	pl = Playlist(urlStr)
	playlist_url = pl.parse_links()
	failed = []

	print("-----------------------------------------")
	print("Video downloads")
	print(len(playlist_url))
	print("-----------------------------------------")
	print("Start download")
	for i in range(len(playlist_url)):
		URL = "https://www.youtube.com"+playlist_url[i]
		try:
			you = YouTube(URL)
			print(i)
			print(you.title)
			path = getcwd + "/video/" + you.title
			mkdir(path)
			url = "https://i.ytimg.com/vi/" + playlist_url[i].replace("/watch?v=","") + "/maxresdefault.jpg"
			print(path)
			urllib_download(url,path + "/image.jpg")
			you.streams.first().download(path)

		except:
			failed.append(i)

	print("Download complete, failed video link")
	print(failed)
	input("OK")


if __name__ == "__main__":
    main()
