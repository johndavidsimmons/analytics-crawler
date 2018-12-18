import os

from terminaltables import AsciiTable # type: ignore
from termcolor import colored # type: ignore
from typing import List

rocket:str = u"\U0001F680"

table_data: List = [
    ["Section", 'DTM/Launch Present', 'Timestamp']
]

class PrintTablePipeline(object):

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        table = AsciiTable(table_data)
        print(table.table)

    def process_item(self, item, spider):
        output_color: str = 'green' if item['script_exists'] else 'red'

        table_data.append([
            item['channel'],
            colored(item['script_exists'], output_color),
            item['last_checked']]
        )

        return item


class EmailPipeline(object):

    def __init__(self, **kwargs):
        self.AWS_REGION = kwargs['AWS_REGION']
        self.AWS_SECRET_ACCESS_KEY = kwargs['AWS_SECRET_ACCESS_KEY']
        self.AWS_ACCESS_KEY_ID = kwargs['AWS_ACCESS_KEY_ID']
        self.SENDER = kwargs['SENDER'],
        self.RECIPIENT = kwargs['RECIPIENT']

    # Get AWS credentials from project settings
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            AWS_REGION=crawler.settings.get('AWS_REGION'),
            AWS_SECRET_ACCESS_KEY=crawler.settings.get('AWS_SECRET_ACCESS_KEY'),
            AWS_ACCESS_KEY_ID=crawler.settings.get('AWS_ACCESS_KEY_ID'),
            SENDER=crawler.settings.get("SENDER"),
            RECIPIENT=crawler.settings.get("RECIPIENT")
        )

    def open_spider(self, spider):
        self.false_items: List[str] = []    

    def process_item(self, item, spider):
        if not item['script_exists']:
            self.false_items.append(item)
        return item

    def close_spider(self, spider):

        # If there are items in the list
        if self.false_items:

            # jinja template
            from jinja2 import Template
            template = Template(
                """
                <h1>DTM/Launch Report</h1>
                <p>Rows of data</p>
                <ul>
                    <li>
                    {% for row in data %}
                        {{ row }}
                    {% endfor %}
                    </li>
                </ul>
                """
            )

            body:str = template.render(data=self.false_items)

            import boto3 # type: ignore
            from botocore.exceptions import ClientError # type: ignore

            # auth kwargs here must be lowercase
            client = boto3.client(
                'ses',
                region_name=self.AWS_REGION,
                aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
                aws_access_key_id=self.AWS_ACCESS_KEY_ID,
                verify=False)

            SENDER:str = "Analytics Alert <" + self.SENDER[0] + ">" # Sender is tuple here?
            RECIPIENT:str = self.RECIPIENT
            SUBJECT:str = "Analytics Alert"
            CHARSET:str = "UTF-8"

            try:
                response = client.send_email(
                    Destination={
                        'ToAddresses': [
                            RECIPIENT,
                        ],
                    },
                    Message={
                        'Body': {
                            'Html': {
                                'Charset': CHARSET,
                                'Data': body,
                            }
                        },
                        'Subject': {
                            'Charset': CHARSET,
                            'Data': SUBJECT,
                        },
                    },
                    Source=SENDER,
                )
            except ClientError as e:
                print(e.response['Error']['Message'])
            else:
                print("Email sent! Message ID:"),
                print(response['MessageId'])
