from optparse import OptionParser
from bs4 import BeautifulSoup
import urllib2
import json
import datetime

usage = "usage: ./obb_take_home.py -s [string] "
parser = OptionParser(usage)
parser.add_option("-s", action="store", dest="search_string", help="string to narrow search results")
(options, args) = parser.parse_args()

if options.search_string is not None:
	search_string = options.search_string
else:
	search_string = "A"

def get_html(search_string):
	url = "http://www.secretary.state.nc.us/corporations/searchresults.aspx?onlyactive=ON&Words=STARTING&searchstr="
	url_with_search_string = url + search_string
	page = urllib2.urlopen(url_with_search_string)
	page_html = page.read()
	html_obj = BeautifulSoup(page_html)

	return html_obj

def find_table(html_obj):
	table = html_obj.find('table', {'id': "SosContent_SosContent_dgCorps"})
	return table

def build_string_list(table):
	string_list = []
	for string in table.strings:
		if string == 'File Report':
			continue
		if "\n" not in string:
			string_list.append(string)

	return string_list

def build_link_list(table):
	link_list = []
	for link in table.find_all('a'):

		link = unicode(link)
		if 'statusdef.aspx?' in link or 'ARReportsList.aspx?' in link:
			continue
		
		link_list.append(link)

	return link_list

def build_header_list(string_list):
	header_list = string_list[1:5]

	return header_list

def build_data_list(string_list):
	data_list = string_list[6:]

	return data_list

def generate_itemid_dict(link_list):
	itemid_dict = {}
	for link in link_list:
		# use some random characters for delimination
		qmar_index = link.find("?")
		greater_than_index = link.find('>')
		id_string = link[qmar_index:greater_than_index]
		equals_index = id_string.find("=")
		quote_index = id_string.find('"')
		itemid = id_string[equals_index+1:quote_index]

		entity_string = link[qmar_index:]
		greater_than_index = entity_string.find(">")
		less_than_index = entity_string.find("<")
		entity = entity_string[greater_than_index+1:less_than_index]
		
		itemid_dict[(entity)] = itemid

	return itemid_dict

def group_entities(data_list):
	grouped_data_list = []
	for i in range(0, len(data_list),4):
		entity = data_list[i:i+4]
		if len(entity) == 4:
			 grouped_data_list.append(tuple(entity))

	return grouped_data_list

def build_entity_dict(grouped_list, itemid_dict):
	entity_dict = {}

	for i in grouped_list:
		entity = {}
		name = i[0]
		bus_type = i[1]
		status = i[2]
		formed = i[3]

		try:
			itemid = itemid_dict[name]
		except KeyError:
			continue

		url = 'http://www.secretary.state.nc.us/corporations/Corp.aspx?PitemId=' + str(itemid)
		if name not in entity_dict:
			entity_dict[name] = {}

		entity['name'] = name
		entity['bus_type'] = bus_type
		entity['status'] = status
		entity['formed'] = formed
		entity['url'] = url
		entity_dict[name] = entity 

	return entity_dict

def encode_json(entity_dict):
	encoded = json.dumps(entity_dict)
	return encoded

def write_to_file(encoded_entities):
	ds = str(datetime.datetime.now())
	with open("nc.json"+ "_" + ds, "a") as f:
		f.write(encoded_entities)



html_obj = get_html(search_string)
table = find_table(html_obj)
string_list = build_string_list(table)
link_list = build_link_list(table)
header_list = build_header_list(string_list)
data_list = build_data_list(string_list)
itemid_dict = generate_itemid_dict(link_list)
grouped_list = group_entities(data_list)
entity_dict = build_entity_dict(grouped_list,itemid_dict)
encoded_entities = encode_json(entity_dict)
write_to_file(encoded_entities)
