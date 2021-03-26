import scrapy

from scrapy.loader import ItemLoader

from ..items import FvcbankItem
from itemloaders.processors import TakeFirst


class FvcbankSpider(scrapy.Spider):
	name = 'fvcbank'
	start_urls = ['https://www.fvcbank.com/category/press-releases/',
	              'https://www.fvcbank.com/blog/',
	              'https://www.fvcbank.com/category/announcements/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="entry-title-link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//li[@class="pagination-next"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="entry-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//time/text()').get()

		item = ItemLoader(item=FvcbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
