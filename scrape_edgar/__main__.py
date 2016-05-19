#!/usr/bin/env python
from bs4 import BeautifulSoup

import re
import requests
import sys

BASE_URL = "http://data-interview.enigmalabs.org/companies/"

def generate_company_json(url):
	pass

def get_links_from_page(page):
	"""
	Return list of all company links on a single page or None if none.
	"""
	links_from_page = []
	# get soup from new page
	url = BASE_URL + "?page=" + str(page)
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	# if blank page were inaccessible, we would be able to check response code for 404
	# in this particular case, blank pages (e.g. page 11) still return 200 "OK"
	# as a work-around, check if page has table body
	if soup.tbody:
		# links are nested in table body
		for link in soup.tbody.find_all('a'):
			company_link = link.get('href')
			links_from_page.append(company_link)
		return links_from_page
	# if no table body do not return a list
	return None

def get_all_links():
	"""
	Iterate through pages of website, starting from page 1.
	Build list of all company list until there are none, then return it.
	"""
	all_links = []
	page = 1
	links_from_page = get_links_from_page(page)
	while links_from_page:
		# there are links on the page to be added
		all_links.extend(links_from_page)
		# try next page
		page = page + 1
		links_from_page = get_links_from_page(page)
	# exited loop, no more links to collect
	return all_links

if __name__ == "__main__":
	all_links = get_all_links()
	print len(all_links)
