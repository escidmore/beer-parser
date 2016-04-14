#!/usr/bin/python3
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re

url="http://www.sandiegobrewing.com/our-beer/beers-on-tap"
beers=[]
	
def fetch_url(useragent="Mozilla/5.0",referrer="None"):
	req = Request(url)
	#req.add_header('User-Agent', useragent)
	#req.add_header('Referrer', referrer)
	response = urlopen(req)
	return(response.read())	
	
def get_beers():
	"""Parses HTML contents for the data we're interested in, 
	then returns a list of dictionaries containing the results"""
	
	html_contents=fetch_url()
	beers=[]
	soup = BeautifulSoup(html_contents, 'html.parser')
	beers_html = soup.find_all("td",{"class": "beer-column"})
	for beer_html in beers_html:
		beer_name_header = beer_html.find("a",{"class": "beername"})
		beer_name = beer_name_header.get_text()
		beer_name = re.sub("\s\s+", "", beer_name)
		beer_span = beer_html.find("span",{"class": "style"})
		if beer_span:
			beer_style = beer_span.get_text()
		else:
			beer_style = "None"
		beers.append({"name": beer_name, "style": beer_style})
#		beers.append({"name": beer_name, "style": "test"})
	return(beers)

def non_ipas():
	return(dumps(beers, indent=4, separators=(',', ': '), sort_keys=False))

beers = get_beers()

for beer in beers:
	if "IPA" not in beer['style']:
		if "San Diego Brewing" not in beer['name']:
			print(beer['name'] + "\n" + beer['style'] + "\n")
