# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'analytics_check',
    version      = '1.0',
    packages     = find_packages(),
    package_data = {
        'analytics_check' : ['resources/*.csv']
    },
    entry_points = {
        'scrapy': 
            ['settings = analytics_check.settings']
    },
)
