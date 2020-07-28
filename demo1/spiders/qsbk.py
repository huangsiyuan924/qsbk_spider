import scrapy
import json
from demo1.items import Demo1Item
base_url = "https://www.qiushibaike.com"


class QsbkSpider(scrapy.Spider):
    name = 'qsbk'
    allowed_domains = ['qiushibaike.com/']
    start_urls = ['https://www.qiushibaike.com/text/page/1/']

    def parse(self, response):
        # 段子的路径url（不包含域名）
        article_list = response.xpath('//a[@class="contentHerf"]/@href').extract()
        for article in article_list:
            # 段子的完整路径url
            article_url = base_url + article
            req = response.follow(url=article_url,
                                  callback=self.parse_article,
                                  dont_filter=True)
            yield req
        # 下一页按钮
        next_page = response.xpath('//ul[@class="pagination"]/li[last()]/a/@href').extract_first()
        if not next_page:
            return
        else:
            yield response.follow(base_url + next_page,
                                  callback=self.parse,
                                  dont_filter=True
                                  )

    def parse_article(self, response):
        # 段子标题
        title = response.xpath('//h1[@class="article-title"]/text()').extract_first().strip()
        # 段子作者
        author = response.xpath('//span[@class="side-user-name"]/text()').extract_first()
        # 段子内容
        content = "".join(response.xpath('//div[@class="content"]/text()').extract()).replace(" ", "")
        # 段子发布时间
        stats_time = response.xpath('//span[@class="stats-time"]/text()').extract_first().strip()
        # 段子热度(好笑度)
        heat = response.xpath('//i[@class="number"]/text()').extract_first().strip()
        # 神评用户
        good_comments_user_list = response.xpath('//div[@id="good-cmt"]//a[@class="userlogin"]/@title').extract()
        # 神评内容
        good_comments_detail_list = response.xpath('//div[@id="good-cmt"]//span[@class="body"]/text()').extract()
        # 神评用户名+内容的列表
        good_comments_list = []
        for i, good_comment_user in enumerate(good_comments_user_list):
            good_comments_list.append([good_comment_user, good_comments_detail_list[i].replace(" ", "")])

        item = Demo1Item()
        item['title'] = title
        item['author'] = author
        item['content'] = content
        item['stats_time'] = stats_time
        item['heat'] = heat
        item['good_comments_list'] = json.dumps(good_comments_list)
        # 文章的所有评论的url, 参数page设为1， count设为99999可获取文章的所有评论
        comments_url = response.url.replace("article", "commentpage") + "?page=1&count=99999"

        yield response.follow(url=comments_url,
                              callback=self.parse_comments,
                              dont_filter=True,
                              meta={'item': item})

    def parse_comments(self, response):
        # https://www.qiushibaike.com/commentpage/123395328?page=1&count=99999
        # 获取返回结果， 转为字典， 解析要用到的数据
        res = json.loads(response.body)['comments']
        # 评论数
        comments_num = res['total']
        # 段子的所有评论
        comments_list = []
        for i in range(comments_num):
            # 将用户名和评论内容拼接起来放入list
            comments_list.append([res['items'][i]['login'], res['items'][i]['content']])


        # 发送给pipline
        item = response.meta['item']
        item['comments_list'] = json.dumps(comments_list, ensure_ascii=False)
        yield item

