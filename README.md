# 糗事百科爬虫

## 项目介绍
    该项目是基于Scrapy框架的爬取糗事百科段子的爬虫, 爬取后的数据存在关系型数据库MySQL中
    

## 项目环境
* 操作系统：Windows10
* Python版本: 3.6.8
* Scrapy版本: 2.0.0
* MySQL版本: 8.0.12
* IDE: PyCharm2020.1.4
## 使用方法
1. 克隆代码到本地并解压打开项目(环境在[requirements.txt](requirements.txt))
    ~~~ 
    clone git@github.com:huangsiyuan924/qsbk_spider.git
    ~~~
2. MySQL创建数据库test(可自行在文件[MysqlUtil.py](demo1/MysqlUtil.py)中更改数据库名)<br>
   数据表可在爬虫执行时自动创建<br>
   title 段子标题<br>
   author 段子作者<br>
   content 段子内容<br>
   stats_time 发布时间<br>
   heat 段子热度<br>
   good_comments_list 该段子神评<br>
   comments_list 段子所有评论<br>
   ~~~sql
   CREATE TABLE IF NOT EXISTS qsbk(
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        title VARCHAR(150) NOT NULL,
                        author VARCHAR(30) NOT NULL,
                        content TEXT NOT NULL,
                        stats_time DATETIME NOT NULL,
                        heat INT NOT NULL,
                        good_comments_list BLOB,
                        comments_list BLOB
                        )
   ~~~
3. 运行[run_qsbk.py](demo1/run_qsbk.py)即可爬取数据到MySQL当中
