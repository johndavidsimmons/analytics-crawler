import os
from datetime import datetime
from typing import Dict, List
import pkgutil

from analytics_check.items import ScriptCheckItem # type: ignore
import scrapy # type: ignore
import scrapy_splash # type: ignore
from scrapy.loader import ItemLoader
from scrapy.utils.project import get_project_settings


class ScriptSpider(scrapy.Spider):
    name: str = "script_check"
    # http_user = "0deb8211a13e4260a3fc5eba4616ade5"
    try:
        http_user = self.http_user
    except:
        http_user = ""


    try:
        data_bytes = pkgutil.get_data("analytics_check", "resources/data.csv")
        data_string = data_bytes.decode("utf-8")
        lst = data_string.split("\r")
        data = [tuple(i.split(",")) for i in lst]
        urls = [] 
        for tup in data:
            (a,b,c) = tup
            urls.append((a.strip(),b,c))
    except Exception as e:
        print("*****************")
        print(e)
        print("*****************")

    def start_requests(self):
        for channel, url, script in self.urls:
            yield scrapy.Request(url, self.parse, meta={
                'channel': channel,
                'script': script,
                'splash': {
                    'args': {
                        'html': 1,
                        'png': 0,
                        'wait': 1
                    },
                }
            })

    def parse(self, response):
        script_exists: bool = False
        script = response.meta['script']
        channel = response.meta['channel']
        script_selector: str = f"script[src='{script}']"
        script_element = response.css(script_selector)
        script_src: str = ""

        try:
            if script_element:
                script_src = script_element[0].xpath("@src").extract()[0]
            if script_src == script:
                script_exists = True
        except Exception as e:
            pass

        data: dict = {
            "channel": channel,
            "url": response.url,
            "script_exists": script_exists,
            "script": script,
            "last_checked": datetime.now().strftime('%c')
        }

        item = ItemLoader(item=ScriptCheckItem(data), response=response)
        return item.load_item()

