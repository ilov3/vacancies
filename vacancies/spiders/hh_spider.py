# coding=utf-8
import logging
import scrapy
from scrapy.exceptions import CloseSpider

from vacancies.items import Vacancy

__author__ = 'ilov3'
logger = logging.getLogger(__name__)


class HHSpider(scrapy.Spider):
    name = 'hh_spider'
    url = 'https://tatarstan.hh.ru/search/vacancy?text={0}&page={1}'

    def __init__(self, search, name=None, **kwargs):
        self.search = search
        super(HHSpider, self).__init__(name, **kwargs)

    def start_requests(self):
        url = self.url.format(self.search, 1)
        yield scrapy.Request(url, callback=self.parse, dont_filter=True, meta={'page': 2})

    def parse(self, response):
        if response.status == 404:
            raise CloseSpider('>>>>>>>>>>>>>>>>>>>>>>>>>>> Finish')
        if response.status in (302,) and 'Location' in response.headers:
            yield scrapy.Request(response.urljoin(response.headers['Location']), callback=self.parse)
        vacancies = response.xpath("//div[div/@class='b-vacancy-list-salary']")
        for vacancy in vacancies:
            title = self.extract(vacancy.xpath("./div[1]/a/text()"))
            salary = self.extract(vacancy.xpath("./div[2]/meta[2]/@content"))
            currency = self.extract(vacancy.xpath("./div[2]/meta[1]/@content"))
            company = self.extract(vacancy.xpath("./div[@class='search-result-item__company']/a/text()"))
            location = self.extract(vacancy.xpath("./div[last()]/span/text()"))
            new_vacancy = Vacancy(title=title, salary=salary, currency=currency, company=company, location=location)
            yield new_vacancy

        page = response.meta['page']
        url = self.url.format(self.search, page)
        yield scrapy.Request(url, callback=self.parse, dont_filter=True, meta={'page': page + 1})

    @staticmethod
    def extract(list_of_selectors):
        try:
            return list_of_selectors[0].extract()
        except IndexError:
            return "Unknown title"
