#coding=UTF-8

from pytube import YouTube
from pytube import Playlist
import urllib.request
import os
import uuid

getcwd = os.getcwd()
def mkdir(path):
	folder = os.path.exists(path)
	if not folder:
		os.makedirs(path)

def urllib_download(url, path):
	f = urllib.request.urlopen(url)
	data = f.read()
	with open(path, 'wb') as code:
		code.write(data)

def get_mac_address():
	node = uuid.getnode()
	mac = uuid.UUID(int = node).hex[-12:]
	return mac
def main():

	# if not(get_mac_address() == "0c9d921693d5" or get_mac_address() == "00ffe28630d5"):
	# 	return
	videoPath = input("Please input file name\n")
	urlStr = input("Please input the url\n")
	print("Loading...")
	pl = Playlist("https://www.youtube.com/" + urlStr)
	playlist_urls = pl.parse_all_links()
	failed = []

	print("-----------------------------------------")
	print("Video downloads")
	print(len(playlist_urls))
	print("-----------------------------------------")
	print("Start download")
	for i in range(len(playlist_urls)):
		print("")
		print("")
		print("-----------------------------------------")
		playlist_url = playlist_urls[i].split()[0][:-1]
		URL = "https://www.youtube.com"+playlist_url
		try:
			you = YouTube(URL);
			print(i)
			print(you.title)
			path = getcwd + "/" + videoPath + "/" + you.title
			mkdir(path)
			url = "https://i.ytimg.com/vi/" + playlist_url.replace("/watch?v=","") + "/maxresdefault.jpg"
			print(path)
			you.streams.first().download(path)
			urllib_download(url, path + "/image.jpg")

		except:
			failed.append(playlist_url)


	print("")
	print("Download complete, failed video link")
	print(failed)

	print("")
	print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
	print("++++                                           ++++")
	print("++++    Recursive download of failed video     ++++")
	print("++++         Download hqdefault image          ++++")
	print("++++                                           ++++")
	print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
	print("")

	for playlist_url in failed:
		print("")
		print("")
		print("-----------------------------------------")
		URL = "https://www.youtube.com"+playlist_url
		try:
			you = YouTube(URL);
			print(you.title)
			path = getcwd + "/" + videoPath + "/" + you.title
			mkdir(path)
			url = "https://i.ytimg.com/vi/" + playlist_url.replace("/watch?v=","") + "/hqdefault.jpg"
			print(path)
			urllib_download(url, path + "/image.jpg")
			you.streams.first().download(path)
			failed.remove(playlist_url)
		except:
			print("")

	print("Download complete, failed video link")
	print(failed)
	input("OK")


if __name__ == "__main__":
    main()
