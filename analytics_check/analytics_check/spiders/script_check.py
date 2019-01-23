from datetime import datetime
import os
import pkgutil
from typing import Dict, List, Optional

from analytics_check.items import ScriptCheckItem
import scrapy # type: ignore
import scrapy_splash # type: ignore
from scrapy.loader import ItemLoader # type: ignore


class ScriptSpider(scrapy.Spider):
    name:str = "script_check"

    # scraping hub can't find env variables in the spider
    # so it must pass as an argument
    # scrapy crawl script_check -a http_user=abc123
    try:
        http_user:str = self.http_user
    except:
        http_user:str = os.getenv("http_user")

    try:
        data_bytes:Optional[bytes] = pkgutil.get_data("analytics_check", "resources/data.csv")
        data_string:str = data_bytes.decode("utf-8")
        lst:List[str] = data_string.split("\r")
        data:List[tuple] = [tuple(i.split(",")) for i in lst]
        urls:List[tuple] = []
        for tup in data:
            (a,b,c) = tup
            urls.append((a.strip(),b,c))
    except Exception as e:
        print(f"Error with csv file: {e}")

    def start_requests(self):
        for channel, url, script in self.urls:
            yield scrapy.Request(url, self.parse, meta={
                'channel': channel,
                'script': script,
                'splash': {
                    'args': {
                        'html': 1,
                        'png': 0,
                        'wait': 2
                    },
                }
            })

    def parse(self, response):
        script_exists:bool = False
        script:str = response.meta['script']
        channel:str = response.meta['channel']
        script_selector:str = f"script[src='{script}']"
        script_element = response.css(script_selector)
        script_src:str = ""

        try:
            if script_element:
                script_src = script_element[0].xpath("@src").extract()[0]
            if script_src == script:
                script_exists = True
        except Exception as e:
            pass

        data:dict = {
            "channel": channel,
            "url": response.url,
            "script_exists": script_exists,
            "script": script,
            "last_checked": datetime.now().strftime('%c')
        }

        item = ItemLoader(item=ScriptCheckItem(data), response=response)
        return item.load_item()
