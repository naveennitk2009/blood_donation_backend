import bs4, sys
from elasticsearch import Elasticsearch
from dateutil import parser
from mappings import *
from selenium import webdriver
import time
import traceback

es_client = Elasticsearch('localhost:9200')

def get_attributes(coupon):
	attributes = {}
	attributes['discount'] = coupon.select('div .pctgcell')[0].getText().strip()
	attributes['merchant'] = coupon.select('div .mer-co-sec')[0].getText().strip().split()[0]
	attributes['short_description'] = coupon.select('.ofr-descptxt')[0].getText().strip()
	attributes['description'] = coupon.select('div .hdtxt > span')[0].getText().strip()
	tag_string = coupon.select('div .cat-tags')
	attributes['tags'] = []
	if len(tag_string) != 0:
		tags = tag_string[0].getText().split('-')[1].strip().split(',')
		for tag in tags:
			attributes['tags'].append(tag.strip())
	attributes['code'] = 'No Code Required'
	if len(coupon.select('div .offr-lnks div .parent input')) != 0:
		attributes['code'] = coupon.select('div .offr-lnks div .parent input')[0].get('value')
	attributes['validity'] = parser.parse(" ".join(coupon.select('div .grdcpnsmllnks ul li')[2].getText().split()[2:]))
	return attributes


def function(file):
	soup = bs4.BeautifulSoup(file, "html.parser")
	block = soup.select('div #rpt_coupondata')[0]
	coupons = block.select('.nw-merbrdrdbx')
	for coupon in coupons:
		data = get_attributes(coupon)
		print data['merchant']
		insert_into_es(data)

coupons_index = "coupons_index"


def create_coupons_index():
	es_client.indices.create(coupons_index)
	es_client.indices.put_mapping(doc_type="coupon", index=coupons_index, body=get_coupon_mapping())


def insert_into_es(data):
	es_client.create(coupons_index, doc_type= "coupon", body= data)

driver = webdriver.Chrome()
def selenium_auto(url):
	driver.get(url)
	count = 0
	presence = True
	ids_set = set()
	while presence:
		block = driver.find_element_by_id('rpt_coupondata')
		coupons = block.find_elements_by_class_name("nw-merbrdrdbx")
		for cou in coupons:
			coupon = bs4.BeautifulSoup(cou.get_attribute('innerHTML'), "html.parser")
			id = cou.get_attribute('id')
			if id not in ids_set:
				ids_set.add(id)
				data = get_attributes(coupon)
				count += 1
				insert_into_es(data)
		try:
			button = driver.find_element_by_id('div_loadmore')
			button.click()
			time.sleep(5)
		except Exception as e:
			traceback.print_exc()
			presence = False
			print e
			print count

create_coupons_index()
for argv in sys.argv[1:]:
	base_url = 'http://www.couponraja.in/'
	url = base_url + argv
	selenium_auto(url)

