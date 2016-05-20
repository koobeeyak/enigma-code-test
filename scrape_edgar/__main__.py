#!/usr/bin/env python
from bs4 import BeautifulSoup

import json
import re
import requests
import sys

BASE_URL = "http://data-interview.enigmalabs.org"

def generate_company_dict(link):
	"""
	Build dictionary with table row id's as key, text as value.
	"""
	# append company name to complete url
	url = BASE_URL + link
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	company_dict = {}
	# each row of table body contains company data
	for row in soup.tbody.find_all(id=True):
		# id is a description of the data that we can use as a key
		field = row['id']
		# the text in the row is the company's data
		data = row.text
		company_dict[field] = data
	return company_dict

def get_links_from_page(page):
	"""
	Return list of all company links on a single page or None if none.
	"""
	links_from_page = []
	# get soup from new page
	url = BASE_URL + "/companies/?page=" + str(page)
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

def main():
	"""
	Builds a list of all company links by iterating through pages.
	Generates JSON from each company page and then writes to 'solution.json'
	"""
	all_links = get_all_links()
	with open('solution.json', 'wb') as outfile:
		# let's create a list of dicts so JSON file will be properly formatted
		dicts = []
		for link in all_links:
			company_dict = generate_company_dict(link)
			dicts.append(company_dict)
		# json.dump() converts list of dicts to JSON and writes to file, optional args sort_keys and indent make output neater
		json.dump(dicts, outfile, sort_keys = True, indent = 4)

if __name__ == "__main__":
	main()
