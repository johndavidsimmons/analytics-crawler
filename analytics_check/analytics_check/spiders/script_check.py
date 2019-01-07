from datetime import datetime
import os
import pkgutil
from typing import Dict, List, Optional

from analytics_check.items import ScriptCheckItem
import scrapy # type: ignore
import scrapy_splash # type: ignore
from scrapy.loader import ItemLoader # type: ignore

def script_exists(response, script):
    exists:bool = False
    selector:str = f"script[src='{script}']"
    element = response.css(selector)
    src:str = ""

    if element:
        src = element[0].xpath("@src").extract()[0]
        if src == script:
            exists = True
    return exists

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
        data_bytes:Optional[bytes] = pkgutil.get_data("analytics_check", "resources/mpart.csv")
        data_string:str = data_bytes.decode("utf-8")
        lst:List[str] = data_string.split("\r")
        data:List[tuple] = [tuple(i.split(",")) for i in lst]
        urls:List[tuple] = []
        for tup in data:
            (common_name, prop, url, mparticle, dtm) = tup
            scripts = [mparticle, dtm]
            urls.append((common_name.strip(),prop,url,scripts))
    except Exception as e:
        print(f"Error with csv file: {e}")

    def start_requests(self):
        for common_name, prop, url, scripts in self.urls:
            yield scrapy.Request(url, self.parse, meta={
                'prop': prop,
                'common_name': common_name,
                'scripts': scripts,
                'splash': {
                    'args': {
                        'html': 1,
                        'png': 0,
                        'wait': 1
                    },
                }
            })


    def parse(self, response):
        # scripts = response.meta['scripts']
        mpart_script, dtm_script = response.meta['scripts']
        # for s in scripts:
            # print(s, " | ", script_exists(response, s))


        data:dict = {
            "common_name": response.meta['common_name'],
            "prop": response.meta['prop'],
            "url": response.url,
            "mparticle_exists": script_exists(response, mpart_script),
            "dtm_exists": script_exists(response, dtm_script),
            "last_checked": datetime.now().strftime('%c')
        }

        item = ItemLoader(item=ScriptCheckItem(data), response=response)
        return item.load_item()
