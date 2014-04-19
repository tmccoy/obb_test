from optparse import OptionParser
from bs4 import BeautifulSoup
import urllib2

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

print table

print "______________"
entity = table.find_all('td')

print entity