from scrapy import Request
import re

from sumaq.spiders import BaseSpider
from sumaq.items import PostItem


class ForosPeruSpider(BaseSpider):
    name = "forosperu"
    base_url = "https://www.forosperu.net"
    max_section_pagination = 1
    max_forum_pagination = 1
    paginated_url_pattern = "https://www.forosperu.net/{relative_url}/pagina-{page}"
    base_url_pattern = "https://www.forosperu.net/{relative_url}"

    def parse(self, response, *args, **kwargs):
        sections = response.css("div.forumNodeInfo h3.nodeTitle a")
        for section in sections:
            relative_url = section.css("::attr(href)").get().strip("/")
            yield Request(
                self.paginated_url_pattern.format(relative_url=relative_url, page=1),
                callback=self.parse_section,
                meta={
                    "section_url": relative_url,
                    "page": 1,
                },
            )

    def parse_section(self, response, **kwargs):
        current_page = response.css("div.PageNav::attr(data-page)").get()
        if current_page and int(current_page) != response.meta.get("page", 1):
            return

        for forum in response.css("li.discussionListItem h3.title a"):
            relative_url = forum.css("::attr(href)").get().strip("/")
            yield Request(
                self.base_url_pattern.format(relative_url=relative_url),
                callback=self.parse_forum,
                meta={
                    "forum_url": relative_url,
                },
            )

        if not current_page:
            return

        next_page = int(current_page) + 1
        if next_page > self.max_section_pagination:
            return

        section_url = response.meta["section_url"]
        yield Request(
            self.paginated_url_pattern.format(relative_url=section_url, page=next_page),
            callback=self.parse_section,
            meta={
                "section_url": section_url,
                "page": next_page,
            },
        )

    def parse_forum(self, response, **kwargs):
        last_page = response.meta.get(
            "page", response.css("div.PageNav::attr(data-last)").get()
        )
        if last_page:
            yield Request(
                self.paginated_url_pattern.format(
                    relative_url=response.meta["forum_url"], page=last_page
                ),
                callback=self.parse_forum_posts,
                meta={
                    "page": int(last_page),
                    "forum_url": response.meta["forum_url"],
                },
            )
        else:
            yield Request(
                self.base_url_pattern.format(
                    relative_url=response.meta["forum_url"], page=last_page
                ),
                callback=self.parse_forum_posts,
                meta={
                    "forum_url": response.meta["forum_url"],
                },
            )

    def parse_forum_posts(self, response, *args, **kwargs):
        depth = response.meta.get("depth", 1)
        page = response.meta.get("page", 1)
        for message in response.css("li.message"):
            item = PostItem()
            item["id"] = message.css("::attr(id)").get()
            item["post_body"] = " ".join(
                message.css("div.messageContent ::text").getall()
            )
            item["post_body"] = " ".join(
                re.sub("[^A-Za-z0-9\s]+", "", item["post_body"]).split()
            )
            item["mention"] = message.css("a.AttributionLink::attr(href)").get()
            yield item

        depth += 1
        page -= 1

        if depth > self.max_forum_pagination or page < 1:
            return

        yield Request(
            self.paginated_url_pattern.format(
                relative_url=response.meta["forum_url"], page=page
            ),
            callback=self.parse_forum_posts,
            meta={
                "page": page,
                "depth": depth,
                "forum_url": response.meta["forum_url"],
            },
        )
