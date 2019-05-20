#coding=UTF-8

from pytube import YouTube
from pytube import Playlist
from pytube import request
import urllib.request
from collections import OrderedDict
import re
import json
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


def parse_all_links(Playlist):

	url = Playlist.construct_playlist_url()
	req = request.get(url)

	# split the page source by line and process each line
	content = [x for x in req.split('\n') if 'yt-uix-sessionlink yt-uix-tile-link' in x]
	link_list = [x.split('href="', 1)[1].split('&', 1)[0] for x in content]

	# The above only returns 100 or fewer links
	# Simulating a browser request for the load more link
	load_more_url = Playlist._load_more_url(req)
	while len(load_more_url):  # there is an url found
		req = request.get(load_more_url)
		load_more = json.loads(req)
		videos = re.findall(
			r'href=\"(/watch\?v=[\w-]*)',
			load_more['content_html'],
		)
		# remove duplicates
		link_list.extend(list(OrderedDict.fromkeys(videos)))
		load_more_url = Playlist._load_more_url(
			load_more['load_more_widget_html'],
		)

	return link_list


def main():

	computer = ["00e05b680642","00e02c680a18","00ff44ba15eb","00e05b68070b","bc5ff4bbe314"];
	#if not(get_mac_address() in computer):
	#	return

	videoPath = input("Please input file name\n")
	urlStr = input("Please input the url\n")
	print("Loading...")
	pl = Playlist("https://www.youtube.com/" + urlStr)
	playlist_urls = parse_all_links(pl)
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
		if "\"" in playlist_urls[i].split()[0]:
			playlist_url = playlist_urls[i].split()[0][:-1]
		else:
			playlist_url = playlist_urls[i].split()[0]
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
