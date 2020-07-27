# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import copy

from itemadapter import ItemAdapter

from demo1.MysqlUtil import MysqlHelper

helper = MysqlHelper()
class Demo1Pipeline:
    def process_item(self, item, spider):
        copy_item = copy.deepcopy(item)
        title = copy_item['title']
        author = copy_item['author']
        content = copy_item['content']
        stats_time = copy_item['stats_time']
        heat = copy_item['heat']
        good_comments_list = copy_item['good_comments_list']
        comments_list = copy_item['comments_list']
        helper.insert_qsbk(title, author, content, stats_time,heat, good_comments_list, comments_list)
        return item