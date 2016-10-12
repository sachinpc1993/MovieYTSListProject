#!/usr/bin/python

from lxml import html
import requests
import time
import urllib2

def check_internet():
    try:
        header = {"pragma" : "no-cache"} # Tells the server to send fresh copy
        req = urllib2.Request("http://www.google.com", headers=header)
        response=urllib2.urlopen(req,timeout=2) # Connected to the Internet
        return True
    except urllib2.URLError as err:
        return False #Not connected to the Internet
	
if (True == check_internet()): # Sanity Check for Internet Connectivity
	page = requests.get('https://yts.ag/browse-movies')
	tree = html.fromstring(page.content)

	figureList = []

	for element in tree.iter():
		if(element.tag == 'figure'):
			figureList.append(element) # figureList used to scrap through the contents of <figure>

	MovieDictionary = {}
	rating = ''
	movieName = ''

	for element in figureList:
		for figureElement in element.iter():
			if ((figureElement.tag == 'h4') and (figureElement.attrib.get('class') == 'rating')):
				rating = figureElement.text
				#print rating
			if (figureElement.tag == 'img'):
				movieName = figureElement.attrib.get('alt')
				movieName = movieName.replace(' download','')
				#print movieName
			MovieDictionary.update({ movieName : rating})

	#print MovieDictionary
	#print len(MovieDictionary)

	#Writing the collected data to the file
	filename = 'YTSMovie.txt'
	Target = open(filename, 'w')

	#Writing the Date and Time of data extraction
	Time = time.strftime("%H:%M:%S")
	#print Time
	Date = time.strftime("%d/%m/%Y")
	#print Date
	Target.write('Date : ')
	Target.write(Date)
	Target.write('\n')
	Target.write('Time : ')
	Target.write(Time)
	Target.write('\n\n\n')


	for movie in MovieDictionary:
		if (movie is not ''): # To remove the first empty element of the movie dictionary
			Target.write(movie)
			Target.write('\t')
			Target.write('[')
			Target.write(MovieDictionary.get(movie))
			Target.write(']')
			Target.write('\n')
			Target.write('---------------------------------------------------------------------\n')
