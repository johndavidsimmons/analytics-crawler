# -*- coding: utf-8 -*-

# Scrapy settings for analytics_check project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import os

BOT_NAME = 'analytics_check'

SPIDER_MODULES = ['analytics_check.spiders']
NEWSPIDER_MODULE = 'analytics_check.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

LOG_LEVEl = "WARNING"
# LOG_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   #'pixelcheck.middlewares.PixelcheckSpiderMiddleware': 543,
   'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'pixelcheck.middlewares.PixelcheckDownloaderMiddleware': 543,
   'scrapy_splash.SplashCookiesMiddleware': 723,
   'scrapy_splash.SplashMiddleware': 725,
   'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'analytics_check.pipelines.PrintTablePipeline': 300,
   # 'analytics_check.pipelines.EmailPipeline': 301,
}

# Splash Settings
# https://github.com/scrapy-plugins/scrapy-splash
SPLASH_URL = os.getenv("SPLASH_URL")
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
http_user = os.getenv("http_user")

# AWS Settings
AWS_REGION = os.getenv("AWS_REGION")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
SENDER = os.getenv("SENDER")
RECIPIENT = os.getenv("RECIPIENT")
