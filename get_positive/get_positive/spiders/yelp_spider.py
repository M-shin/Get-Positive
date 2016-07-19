import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ter_scrape import items
from datetime import datetime, timedelta
import os
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

HOME = os.environ['HOME']
os.chdir(HOME + "/Desktop/github/hackathon/get_positive/get_positive") 

# Method that gets today's date
def date_today(dtnow):
	now = dtnow
	weekdays = ['Mon. ','Tue. ','Wed. ','Thu. ','Fri. ','Sat. ','Sun. ']
	months = ['Jan. ','Feb. ','Mar. ','Apr. ','May. ', 'Jun. ','Jul. ','Aug. ','Sep. ','Oct. ','Nov. ','Dec. ']
	backpage_date = weekdays[now.weekday()] + months[now.month-1] + str(now.day)
	return backpage_date

# Method that gets yesterday's date
def date_yesterday(dtnow):
	now = dtnow - timedelta(days=1)
	weekdays = ['Mon. ','Tue. ','Wed. ','Thu. ','Fri. ','Sat. ','Sun. ']
	months = ['Jan. ','Feb. ','Mar. ','Apr. ','May. ', 'Jun. ','Jul. ','Aug. ','Sep. ','Oct. ','Nov. ','Dec. ']
	backpage_date = weekdays[now.weekday()] + months[now.month-1] + str(now.day)
	return backpage_date

# Open file which contains input urls
# with open("test_urls.txt","rU") as infile:
# 	urls = [row.strip("\n") for row in infile]

class yelp_spider(CrawlSpider):
	name = 'yelp_spider'
	allowed_domains = ['yelp.com']

	def __init__(self, *args, **kwargs): 
		super(TERSpider, self).__init__(*args, **kwargs) 

		self.start_url = kwargs.get('start_url')
		self.static_now = kwargs.get('today')
		all_months = ['Jan. ','Feb. ','Mar. ','Apr. ','May. ', 'Jun. ','Jul. ','Aug. ','Sep. ','Oct. ','Nov. ','Dec. ']
		all_weekdays = ['Mon. ','Tue. ','Wed. ','Thu. ','Fri. ','Sat. ','Sun. ']
		now_day = self.static_now.weekday
		now_month = self.static_now.month
		self.all_dates = []
		for day in all_weekdays:
			for month in all_months:
				if (day != now_day) and (month != now_month):
					self.all_dates.append(day + month)

	def login(self, response):
		return [FormRequest.from_response(response,
				formdata={'USERNAME': 'mprice09', 'PASSWORD': 'Ar@chn1d'},
				callback=self.go_to_search)]

	def go_to_search(self, response):
		return Request(url="https://www.theeroticreview.com/reviews/index.asp",
					callback=self.search)

	def search(self, response):
		return [FormRequest.from_response(response,
				formdata={},
				callback=self.parse)]

	def parse(self,response):

		# Log in at beginning of scraping
		hxs = HtmlXPathSelector(response)
		if hxs.select("//form[@id='USERNAME']"):
			return self.login(response)

		if response.status < 600:
			todays_links = []
			
			date = date_today(self.static_now)
			yesterday_date = date_yesterday(self.static_now)

			if date in response.body:
				
				if any(date in response.body for date in self.all_dates):
					# Get all URLs as long as we are on the last page for today
					todays_links = response.xpath("//div[@class='date'][1]/following-sibling::div[@class='date'][1]/preceding-sibling::div[preceding-sibling::div[@class='date']][contains(@class, 'cat')]/a/@href").extract()
				
				if len(todays_links) == 0:
					# Page is entirely today's links, get all links until end of current page's listings
					todays_links = response.xpath("//div[@class='date'][1]/following-sibling::div[@class='secondPaginationFooter'][1]/preceding-sibling::div[preceding-sibling::div[@class='date']][contains(@class, 'cat')]/a/@href").extract()

				for url in todays_links: 			
				# Iterate through an ad		
					yield scrapy.Request(url,callback=self.parse_ad_into_content)

				if len(todays_links) == 300:
					for url in set(response.xpath('//a[@class="pagination next"]/@href').extract()):
					# End of page, crawl next page
						yield scrapy.Request(url,callback=self.parse)

		else:
			time.sleep(10)
			yield scrapy.Request(response.url,callback=self.parse)

	# Parse page
	def parse_ad_into_content(self,response):

		item = items.TERScrapeItem(url=response.url,
			backpage_id=response.url.split('.')[0].split('/')[2].encode('utf-8'),
			text = response.body,
			posting_body= response.xpath("//div[@class='postingBody']").extract()[0].encode('utf-8'),
			date = str(datetime.utcnow()-timedelta(hours=6)),
			posted_date = response.xpath("//div[@class='adInfo']/text()").extract()[0].encode('utf-8'),
			posted_age = response.xpath("//p[@class='metaInfoDisplay']/text()").extract()[0].encode('utf-8'),
			posted_title = response.xpath("//div[@id='postingTitle']//h1/text()").extract()[0].encode('utf-8')
			)
		return item