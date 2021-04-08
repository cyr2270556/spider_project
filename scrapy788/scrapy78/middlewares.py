# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from Func.get_ip import *
from scrapy import signals
import json
# useful for handling different item types with a single interface



class Scrapy78SpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class Scrapy78DownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class ProxyMiddleware(object):
    def __init__(self):
        self.p = ProxyPool()
        self.col = ProxyPool().client

    def process_request(self, request, spider):
        # 获取可用ip
        ip = self.p.pop()
        #https的网页要改这个地方
        request.meta['proxy'] = "https://" + ip["ip_parmas"]
        print('IP_PROXY:' + request.meta['proxy'])
        # request.meta['proxy'] = "http://" + ip["ip_parmas"]

    def process_response(self,request,response,spider):
        if response.status !=200:

            ip = request.meta['proxy'].split('https://')[1]
            print('需要更改的ip',ip)
            self.col.find_one_and_update({"ip_parmas": ip}, {"$set": {"flag": "0"}})
            request.meta['proxy'] = "https://" + self.p.pop()["ip_parmas"]
            print('跟换ip')
            return request
        else:
            return response

    def process_exception(self, request, exception, spider):
        # 如果ip不可用改变flag为0
        # 重新发起请求
        # if response.status != 200:
            # 改变ip为不可用
        ip = request.meta['proxy'].split('https://')[1]
        print('更改ip',ip)
        self.col.find_one_and_update({"ip_parmas": ip}, {"$set": {"flag": "0"}})
        request.meta['proxy'] = "https://" + self.p.pop()["ip_parmas"]
        # request.meta['proxy'] = "http://" + self.p.pop()["ip_parmas"]
        return request

