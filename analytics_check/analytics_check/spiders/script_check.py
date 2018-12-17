import csv
from datetime import datetime
from typing import Dict, List

from analytics_check.items import ScriptCheckItem # type: ignore
import scrapy # type: ignore
import scrapy_splash # type: ignore
from scrapy.loader import ItemLoader

try:
    with open('../data.csv') as f:
        f_csv = csv.reader(f)
        urls: List[tuple] = [tuple(l) for l in list(f_csv)]
except FileNotFoundError:
    urls = []

class ScriptSpider(scrapy.Spider):
    name: str = "script_check"

    def start_requests(self):
        for channel, url, script in urls:
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

