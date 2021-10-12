# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import boto3


class SumaqPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        """Pass settings to constructor."""
        return cls(crawler.settings)

    def __init__(self, settings):
        self.settings = settings
        self.s3 = boto3.resource(
            "s3",
            region_name=settings["AWS_REGION_NAME"],
            aws_access_key_id=settings["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=settings["AWS_SECRET_ACCESS_KEY"],
        )
        self.mentions = dict()

    def process_item(self, item, _):
        if item["mention"]:
            item["mention"] = item["mention"].split("#")[1]
            mentions = self.mentions.get(item["mention"], [])
            self.mentions[item["mention"]] = mentions + [item["mention"]]
        else:
            item["mention"] = ""
        item["post_body"] = "{} Comments Referenced: {}".format(
            item["post_body"], item["mention"]
        )
        self.s3.Object(
            self.settings["AWS_S3_BUCKET"], "docs/{}".format(item["id"])
        ).put(Body=item["post_body"])
        return item

    def close_spider(self, _):
        content = ""
        for parent, sons in self.mentions.items():
            content += "{} {}\n".format(parent, ",".join(sons))
        self.s3.Object(self.settings["AWS_S3_BUCKET"], "page_rank/input").put(
            Body=content
        )
