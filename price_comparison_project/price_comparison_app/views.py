from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, check_password
from django.contrib.auth.hashers import make_password
from bs4 import BeautifulSoup as bs
from py_bing_search import PyBingWebSearch
from price_comparison_app.forms import *
import requests

def compare_algo(request):
	if request.method == 'POST':
		form = searchForm(request.POST)
		if form.is_valid():
			product_name = form.cleaned_data['search_term']
			API_KEY = "8eFYvQ0mCr06A3YoUZV9XK7867AgLLDeLuBdhILm+3c"
			product_name = input("Enter the Name of the Product:")

			search_term = "buy " + product_name

			bing_web = PyBingWebSearch(API_KEY, search_term, web_only=False)

			first_ten_result= bing_web.search(limit=50, format='json')

			flipkart_urls = []
			flipkart_price_ar = []
			snapdeal_urls = []
			snapdeal_price_ar = []
			min_flipkart = 0
			min_snapdeal = 0

			for result in first_ten_result:
				vendor = result.url.split('.')[1]
				
				if vendor == 'flipkart':
					p = ' '
					
					try:
						p = result.url.split('/')[4]
					except:
						continue

					if(p == 'p'):
						flipkart_urls.append(result.url)
						flipkart_flag = 1

				if vendor == 'snapdeal':
					p = ' '

					try:
					    p = result.url.split('/')[3]
					except:
					    continue

					if(p == 'product'):
						snapdeal_urls.append(result.url)
						snapdeal_flag = 1

			if len(flipkart_urls) == 0 and len(snapdeal_urls) == 0:
				result = 'Search Failed!'
				variables = RequestContext(request, {
					'result': result
				})
				return render_to_response('algo.html', variables)

			else:
				for url in flipkart_urls:
					flipkart_url = url
					flipkart_page = requests.get(flipkart_url)
					flipkart_html = flipkart_page.text
					flipkart_soup = bs(flipkart_html, 'html.parser')
					meta_desc = flipkart_soup.findAll(attrs={"name": "Description"})
					meta_desc_content_split = meta_desc[0]['content'].split(" ")
					for_bool = 0
					For_bool = 0

					try:
						for_index = meta_desc_content_split.index('for')
					except:
						for_bool = 1

					try:
						for_index = meta_desc_content_split.index('For')
					except:
						For_bool = 1

					if for_bool == 0 or For_bool == 0:
						str_price = meta_desc_content_split[for_index + 1]
						if(str_price == 'Rs.'):
							flipkart_price = meta_desc_content_split[for_index + 2]
							flipkart_price_ar.append(flipkart_price)
						else:
							flipkart_price = str_price[3:]
							flipkart_price_ar.append(flipkart_price)

				for url in snapdeal_urls:
					snapdeal_url = url
					snapdeal_page = requests.get(snapdeal_url)
					snapdeal_html = snapdeal_page.text
					snapdeal_soup = bs(snapdeal_html, 'html.parser')
					input_tag = snapdeal_soup.find_all('input', id='productPrice')
					ex = 0
					try:
						str_price = input_tag[0]['value']
					except:
						ex = 1
					if(ex != 1):
						snapdeal_price_ar.append(str_price)

				if(len(flipkart_price_ar)>0):
					min_flipkart = flipkart_price_ar[0]
					for price in flipkart_price_ar:
						if(price>min_flipkart):
							min_flipkart = price

				if(len(snapdeal_price_ar)>0):
					min_snapdeal = snapdeal_price_ar[0]
					for price in snapdeal_price_ar:
						if(price>min_snapdeal):
							min_snapdeal = price

				result = 'Search Succesful!'
				variables = RequestContext(request, {
					'form': form,
					'result': result,
					'flipkart_price': str(min_flipkart),
					'snapdeal_price': str(min_snapdeal)
				})
				return render_to_response('algo.html', variables)
	else:
		form = searchForm()
		variables = RequestContext(request, {
			'form': form,
		})
		return render_to_response('algo.html', variables)
