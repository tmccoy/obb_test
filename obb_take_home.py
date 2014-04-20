from optparse import OptionParser
from bs4 import BeautifulSoup
import urllib2
from HTMLParser import HTMLParser

usage = "usage: ./obb_take_home.py  [-v verbose] -s [string] "
parser = OptionParser(usage)
parser.add_option("-s", action="store", dest="search_string", help="string to narrow search results")
parser.add_option("-v", action="store_true", dest="verbose", help="run in verbose mode")

url = "http://www.secretary.state.nc.us/corporations/searchresults.aspx?onlyactive=ON&Words=STARTING&searchstr="
search_string = "AAAAA"
url_with_search_string = url + search_string

page = urllib2.urlopen(url_with_search_string)
page_html = page.read()
parse = BeautifulSoup(page_html)

table = parse.find('table', {'id': "SosContent_SosContent_dgCorps"})

string_list = []
for string in table.strings:
	if string == 'File Report':
		continue
	if "\n" not in string:
		string_list.append(string)
	

header_list = string_list[1:5]
data_list = string_list[6:]
print header_list
print data_list
