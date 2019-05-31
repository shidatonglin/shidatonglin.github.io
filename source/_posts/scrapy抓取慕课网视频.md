---
title: scrapy抓取慕课网视频
copyright: true
date: 2019-05-31 14:03:53
categories: scrapy
tags: scrapy
---

http://www.sohu.com/a/165377822_609569
https://www.jianshu.com/p/1d346aa1e2fa
https://m.imooc.com/article/267477?block_id=tuijian_wz
https://www.cnblogs.com/xiaoafei1991/p/5092853.html


前言
  Scrapy抓取慕课网免费以及实战课程信息，相关环境列举如下：

scrapy v1.5.1
redis
psycopg2 (操作并保存数据到PostgreSQL)

数据表
  完整的爬虫流程大致是这样的：分析页面结构 -> 确定提取信息 -> 设计相应表结构 -> 编写爬虫脚本 -> 数据保存入库；入库可以选择mongo这样的文档数据库，也可以选择mysql这样的关系型数据库。废话不多讲，这里暂且跳过页面分析，现给出如下两张数据表设计：





tb_imooc_course

-- ----------------------------
-- Table structure for tb_imooc_course
-- ----------------------------
DROP TABLE IF EXISTS "public"."tb_imooc_course";
CREATE TABLE "public"."tb_imooc_course" (
  "id" serial4,
  "course_id" int4 NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "difficult" varchar(30) COLLATE "pg_catalog"."default" NOT NULL,
  "student" int4 NOT NULL,
  "desc" varchar(250) COLLATE "pg_catalog"."default" NOT NULL,
  "label" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "image_urls" varchar(250) COLLATE "pg_catalog"."default" NOT NULL,
  "detail" varchar(250) COLLATE "pg_catalog"."default" NOT NULL,
  "duration" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "overall_score" float4,
  "content_score" float4,
  "concise_score" float4,
  "logic_score" float4,
  "summary" varchar(800) COLLATE "pg_catalog"."default",
  "teacher_nickname" varchar(30) COLLATE "pg_catalog"."default",
  "teacher_avatar" varchar(250) COLLATE "pg_catalog"."default",
  "teacher_job" varchar(30) COLLATE "pg_catalog"."default",
  "tip" varchar(500) COLLATE "pg_catalog"."default",
  "can_learn" varchar(500) COLLATE "pg_catalog"."default",
  "update_time" timestamp(6) NOT NULL,
  "create_time" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."tb_imooc_course"."id" IS '自增主键';
COMMENT ON COLUMN "public"."tb_imooc_course"."course_id" IS '课程id';
COMMENT ON COLUMN "public"."tb_imooc_course"."name" IS '课程名称';
COMMENT ON COLUMN "public"."tb_imooc_course"."difficult" IS '难度级别';
COMMENT ON COLUMN "public"."tb_imooc_course"."student" IS '学习人数';
COMMENT ON COLUMN "public"."tb_imooc_course"."desc" IS '课程描述';
COMMENT ON COLUMN "public"."tb_imooc_course"."label" IS '分类标签';
COMMENT ON COLUMN "public"."tb_imooc_course"."image_urls" IS '封面图片';
COMMENT ON COLUMN "public"."tb_imooc_course"."detail" IS '详情地址';
COMMENT ON COLUMN "public"."tb_imooc_course"."duration" IS '课程时长';
COMMENT ON COLUMN "public"."tb_imooc_course"."overall_score" IS '综合评分';
COMMENT ON COLUMN "public"."tb_imooc_course"."content_score" IS '内容实用';
COMMENT ON COLUMN "public"."tb_imooc_course"."concise_score" IS '简洁易懂';
COMMENT ON COLUMN "public"."tb_imooc_course"."logic_score" IS '逻辑清晰';
COMMENT ON COLUMN "public"."tb_imooc_course"."summary" IS '课程简介';
COMMENT ON COLUMN "public"."tb_imooc_course"."teacher_nickname" IS '教师昵称';
COMMENT ON COLUMN "public"."tb_imooc_course"."teacher_avatar" IS '教师头像';
COMMENT ON COLUMN "public"."tb_imooc_course"."teacher_job" IS '教师职位';
COMMENT ON COLUMN "public"."tb_imooc_course"."tip" IS '课程须知';
COMMENT ON COLUMN "public"."tb_imooc_course"."can_learn" IS '能学什么';
COMMENT ON COLUMN "public"."tb_imooc_course"."update_time" IS '更新时间';
COMMENT ON COLUMN "public"."tb_imooc_course"."create_time" IS '入库时间';
COMMENT ON TABLE "public"."tb_imooc_course" IS '免费课程表';

-- ----------------------------
-- Indexes structure for table tb_imooc_course
-- ----------------------------
CREATE UNIQUE INDEX "uni_cid" ON "public"."tb_imooc_course" USING btree (
  "course_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);






tb_imooc_coding

-- ----------------------------
-- Table structure for tb_imooc_coding
-- ----------------------------
DROP TABLE IF EXISTS "public"."tb_imooc_coding";
CREATE TABLE "public"."tb_imooc_coding" (
  "id" serial4,
  "coding_id" int4 NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "difficult" varchar(30) COLLATE "pg_catalog"."default" NOT NULL,
  "student" int4 NOT NULL,
  "desc" varchar(250) COLLATE "pg_catalog"."default" NOT NULL,
  "image_urls" varchar(250) COLLATE "pg_catalog"."default" NOT NULL,
  "price" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "detail" varchar(250) COLLATE "pg_catalog"."default" NOT NULL,
  "overall_score" varchar(20) COLLATE "pg_catalog"."default",
  "teacher_nickname" varchar(30) COLLATE "pg_catalog"."default",
  "teacher_avatar" varchar(250) COLLATE "pg_catalog"."default",
  "duration" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "video" varchar(250) COLLATE "pg_catalog"."default",
  "small_title" varchar(250) COLLATE "pg_catalog"."default",
  "detail_desc" varchar(800) COLLATE "pg_catalog"."default",
  "teacher_job" varchar(50) COLLATE "pg_catalog"."default",
  "suit_crowd" varchar(500) COLLATE "pg_catalog"."default",
  "skill_require" varchar(500) COLLATE "pg_catalog"."default",
  "update_time" timestamp(6) NOT NULL,
  "create_time" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."tb_imooc_coding"."id" IS '自增主键';
COMMENT ON COLUMN "public"."tb_imooc_coding"."coding_id" IS '课程id';
COMMENT ON COLUMN "public"."tb_imooc_coding"."name" IS '课程名称';
COMMENT ON COLUMN "public"."tb_imooc_coding"."difficult" IS '难度级别';
COMMENT ON COLUMN "public"."tb_imooc_coding"."student" IS '学习人数';
COMMENT ON COLUMN "public"."tb_imooc_coding"."desc" IS '课程描述';
COMMENT ON COLUMN "public"."tb_imooc_coding"."image_urls" IS '封面图片';
COMMENT ON COLUMN "public"."tb_imooc_coding"."price" IS '课程价格';
COMMENT ON COLUMN "public"."tb_imooc_coding"."detail" IS '详情地址';
COMMENT ON COLUMN "public"."tb_imooc_coding"."overall_score" IS '评价得分';
COMMENT ON COLUMN "public"."tb_imooc_coding"."teacher_nickname" IS '教师昵称';
COMMENT ON COLUMN "public"."tb_imooc_coding"."teacher_avatar" IS '教师头像';
COMMENT ON COLUMN "public"."tb_imooc_coding"."duration" IS '课程时长';
COMMENT ON COLUMN "public"."tb_imooc_coding"."video" IS '演示视频';
COMMENT ON COLUMN "public"."tb_imooc_coding"."small_title" IS '详情标题';
COMMENT ON COLUMN "public"."tb_imooc_coding"."detail_desc" IS '详情简介';
COMMENT ON COLUMN "public"."tb_imooc_coding"."teacher_job" IS '教师职位';
COMMENT ON COLUMN "public"."tb_imooc_coding"."suit_crowd" IS '适合人群';
COMMENT ON COLUMN "public"."tb_imooc_coding"."skill_require" IS '技术要求';
COMMENT ON COLUMN "public"."tb_imooc_coding"."update_time" IS '更新时间';
COMMENT ON COLUMN "public"."tb_imooc_coding"."create_time" IS '入库时间';
COMMENT ON TABLE "public"."tb_imooc_coding" IS '实战课程表';

-- ----------------------------
-- Indexes structure for table tb_imooc_coding
-- ----------------------------
CREATE UNIQUE INDEX "uni_coding_id" ON "public"."tb_imooc_coding" USING btree (
  "coding_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

新建项目
  创建项目：scrapy startproject imooc，接着在items.py中定义相应的Item：
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader.processors import TakeFirst


# 免费课程
class CourseItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    name = Field()  # 课程名称
    difficult = Field()  # 难度级别
    student = Field()  # 学习人数
    desc = Field()  # 课程描述
    label = Field()  # 分类标签
    image_urls = Field()  # 封面图片
    detail = Field()  # 详情地址
    course_id = Field()  # 课程id
    duration = Field()  # 课程时长
    overall_score = Field()  # 综合评分
    content_score = Field()  # 内容实用
    concise_score = Field()  # 简洁易懂
    logic_score = Field()  # 逻辑清晰
    summary = Field()  # 课程简介
    teacher_nickname = Field()  # 教师昵称
    teacher_avatar = Field()  # 教师头像
    teacher_job = Field()  # 教师职位
    tip = Field()  # 课程须知
    can_learn = Field()  # 能学什么

# 实战课程
class CodingItem(Item):
    name = Field()  # 课程名称
    difficult = Field()  # 难度级别
    student = Field()  # 学习人数
    desc = Field()  # 课程描述
    image_urls = Field()  # 封面图片
    price = Field()  # 课程价格
    detail = Field()  # 详情地址
    coding_id = Field()  # 课程id
    overall_score = Field()  # 评价得分
    teacher_nickname = Field()  # 教师昵称
    teacher_avatar = Field()  # 教师头像
    duration = Field()  # 课程时长
    video = Field()  # 演示视频
    small_title = Field()  # 详情标题
    detail_desc = Field()  # 详情简介
    teacher_job = Field()  # 教师职位
    suit_crowd = Field()  # 适合人群
    skill_require = Field()  # 技术要求

"免费课程"爬虫编写
  下面分析下慕课网免费课程页面的爬虫编写。简单分析下页面情况，以上定义的数据表(tb_imooc_course)信息，分别需要从列表页和课程详情页获取（如下图红框所示）：





免费课程列表页






免费课程详情页

  在项目的spiders目录下创建该爬虫：scrapy genspider course。关于页面数据解析这块强烈建议使用scrapy shell xxx进行调试，以下是这部分内容的代码：
# -*- coding: utf-8 -*-
import re
from urllib import parse

import scrapy
from scrapy.http import Request

from imooc.items import *


class CourseSpider(scrapy.Spider):
    name = 'course'
    allowed_domains = ['www.imooc.com']
    start_urls = ['https://www.imooc.com/course/list/?page=0']
    https = "https:"

    def parse(self, response):
        """抓取课程列表页面"""
        
        url = response.url
        self.logger.info("Response url is %s" % url)

        # 根据Scrapy默认的后入先出(LIFO)深度爬取策略，这里应先提交下一页请求
        next_btn = response.xpath('//a[contains(.//text(),"下一页")]/@href').extract_first()
        if next_btn:
            # 存在下一页按钮，爬取下一页
            next_page = parse.urljoin(url, next_btn)
            yield Request(next_page, callback=self.parse)

        course_list = response.xpath('//div[@class="course-card-container"]')
        for index, course in enumerate(course_list):
            course_item = CourseItem()
            # 课程名称
            course_item['name'] = course.xpath('.//h3[@class="course-card-name"]/text()').extract_first()
            # 课程难度
            course_item['difficult'] = course.xpath(
                './/div[@class="course-card-info"]/span[1]/text()').extract_first()
            # 学习人次
            course_student = course.xpath('.//div[@class="course-card-info"]/span[2]/text()').extract_first()
            course_item['student'] = int(course_student)
            # 课程描述
            course_item['desc'] = course.xpath('.//p[@class="course-card-desc"]/text()').extract_first()
            # 课程分类
            course_label = course.xpath('.//div[@class="course-label"]/label/text()').extract()
            course_item['label'] = ', '.join(course_label)
            # 课程封面
            course_banner = course.xpath('.//div[@class="course-card-top"]/img/@src').extract_first()
            course_item['image_urls'] = ["{0}{1}".format(CourseSpider.https, course_banner)]
            # 详情地址
            course_detail = course.xpath('.//a/@href').extract_first()
            course_item['detail'] = parse.urljoin(url, course_detail)
            # 课程id
            course_id = re.split('/', course_detail)[-1]
            course_item['course_id'] = int(course_id)
            self.log("Item: %s" % course_item)
            # 爬取详情页
            yield Request(course_item['detail'], callback=self.parse_detail, meta={'course_item': course_item})

    def parse_detail(self, response):
        """ 抓取课程详情页面 """
        
        url = response.url
        self.logger.info("Response url is %s" % url)

        course_item = response.meta['course_item']
        meta_value = response.xpath('//span[@class="meta-value"]/text()').extract()
        # 课程时长
        course_item['duration'] = meta_value[1].strip()
        # 综合得分
        course_item['overall_score'] = meta_value[2]
        # 内容实用
        course_item['content_score'] = meta_value[3]
        # 简洁易懂
        course_item['concise_score'] = meta_value[4]
        # 逻辑清晰
        course_item['logic_score'] = meta_value[5]
        # 课程简介
        course_item['summary'] = response.xpath('//div[@class="course-description course-wrap"]/text()') \
            .extract_first().strip()
        # 教师昵称
        course_item['teacher_nickname'] = response.xpath('//span[@class="tit"]/a/text()').extract_first()
        # 教师头像
        avatar = response.xpath('//img[@class="js-usercard-dialog"]/@src').extract_first()
        if avatar:
            course_item['teacher_avatar'] = "{0}{1}".format(CourseSpider.https, avatar)
        # 教师职位
        course_item['teacher_job'] = response.xpath('//span[@class="job"]/text()').extract_first()
        # 课程须知
        course_item['tip'] = response.xpath('//dl[@class="first"]/dd/text()').extract_first()
        # 能学什么
        course_item['can_learn'] = response.xpath(
            '//div[@class="course-info-tip"]/dl[not(@class)]/dd/text()').extract_first()
        yield course_item

  数据的入库在pipelines.py中，后面跟"实战课程"爬虫再一起介绍。
"实战课程"爬虫编写
  继续介绍慕课网实战课程页面的爬虫编写，同样简单分析下页面情况，实战课程定义的数据表(tb_imooc_coding)信息，同样需要从列表页和课程详情页获取（如下图红框所示）：





实战课程列表页






实战课程详情页

  同样在spiders目录下创建该爬虫：scrapy genspider coding。以下是这部分内容的代码：
# -*- coding: utf-8 -*-
import re
from urllib import parse

import scrapy
from scrapy.http import Request

from imooc.items import *


class CodingSpider(scrapy.Spider):
    name = 'coding'
    allowed_domains = ['coding.imooc.com']
    start_urls = ['https://coding.imooc.com/?page=0']
    https = "https:"

    def parse(self, response):
        """抓取课程列表页面"""

        url = response.url
        self.logger.info("Response url is %s" % url)

        next_btn = response.xpath('//a[contains(.//text(),"下一页")]/@href').extract_first()
        if next_btn:
            next_page = parse.urljoin(url, next_btn)
            yield Request(next_page, callback=self.parse)

        coding_list = response.xpath('//div[@class="shizhan-course-wrap l "]')
        for index, coding in enumerate(coding_list):
            coding_item = CodingItem()
            # 课程名称
            coding_item['name'] = coding.xpath('.//p[@class="shizan-name"]/text()').extract_first()
            # 课程难度
            coding_item['difficult'] = coding.xpath('.//span[@class="grade"]/text()').extract_first()
            # 学习人次
            coding_student = coding.xpath('.//div[@class="shizhan-info"]/span[2]/text()').extract_first()
            coding_item['student'] = int(coding_student)
            # 课程描述
            coding_item['desc'] = coding.xpath('.//p[@class="shizan-desc"]/text()').extract_first()
            # 课程封面
            coding_banner = coding.xpath('.//img[@class="shizhan-course-img"]/@src').extract_first()
            coding_item['image_urls'] = ["{0}{1}".format(CodingSpider.https, coding_banner)]
            # 课程价格
            coding_item['price'] = coding.xpath('.//div[@class="course-card-price"]/text()').extract_first()
            # 详情地址
            coding_detail = coding.xpath('.//a/@href').extract_first()
            coding_item['detail'] = parse.urljoin(url, coding_detail)
            # 课程id
            coding_id = re.split('/', coding_detail)[-1].replace('.html', '')
            coding_item['coding_id'] = int(coding_id)
            # 评价得分
            coding_item['overall_score'] = coding.xpath('.//span[@class="r"]/text()').extract_first().replace('评价：', '')
            # 教师昵称
            coding_item['teacher_nickname'] = coding.xpath('.//div[@class="lecturer-info"]/span/text()').extract_first()
            # 教师头像
            avatar = coding.xpath('.//div[@class="lecturer-info"]/img/@src').extract_first()
            coding_item['teacher_avatar'] = "{0}{1}".format(CodingSpider.https, avatar)

            self.log("Item: %s" % coding_item)
            # 爬取详情页
            yield Request(coding_item['detail'], callback=self.parse_detail, meta={'coding_item': coding_item})

    def parse_detail(self, response):
        """ 抓取课程详情页面 """

        url = response.url
        self.logger.info("Response url is %s" % url)

        coding_item = response.meta['coding_item']
        # 课程时长
        coding_item['duration'] = response.xpath(
            '//div[@class="static-item static-time"]/span/strong/text()').extract_first()
        # 演示视频
        video = response.xpath('//div[@id="js-video-content"]/@data-vurl').extract_first()
        coding_item['video'] = parse.urljoin(CodingSpider.https, video)
        # 详情标题
        coding_item['small_title'] = response.xpath('//div[@class="title-box "]/h2/text()').extract_first()
        # 详情简介
        coding_item['detail_desc'] = response.xpath('//div[@class="info-desc"]/text()').extract_first()
        # 教师职位
        coding_item['teacher_job'] = response.xpath('//div[@class="teacher"]/p/text()').extract_first()
        yield coding_item

数据入库
  项目中有用到redis，用来简单判断下数据应该是入库保存还是更新，用mongo这种有版本号的文档数据库可能会更好一些：
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from utils import rds
from utils import pgs
from imooc import items
from datetime import datetime


class ImoocPipeline(object):
    def __init__(self):
        # PostgreSQL和Redis连接应自行更改
        # PostgreSQL
        host = 'localhost'
        port = 12432
        db_name = 'scrapy'
        username = db_name
        password = db_name
        self.postgres = pgs.Pgs(host=host, port=port, db_name=db_name, user=username, password=password)
        # Redis
        self.redis = rds.Rds(host=host, port=12379, db=1, password='redis6379').redis_cli

    def process_item(self, item, spider):
        name = item['name']
        difficult = item['difficult']
        student = item['student']
        desc = item['desc']
        image_urls = item['image_urls'][0]
        detail = item['detail']
        duration = item['duration']
        overall_score = item['overall_score']
        teacher_nickname = item['teacher_nickname']
        teacher_avatar = item.get('teacher_avatar')
        teacher_job = item['teacher_job']
        now = datetime.now()
        str_now = now.strftime('%Y-%m-%d %H:%M:%S')

        if isinstance(item, items.CourseItem):
            # 免费课程
            course_id = item['course_id']
            label = item['label']
            overall_score = float(overall_score)
            content_score = float(item['content_score'])
            concise_score = float(item['concise_score'])
            logic_score = float(item['logic_score'])
            summary = item['summary']
            tip = item['tip']
            can_learn = item['can_learn']

            key = 'imooc:course:{0}'.format(course_id)
            if self.redis.exists(key):
                params = (student, overall_score, content_score, concise_score, logic_score, now, course_id)
                self.postgres.handler(update_course(), params)
            else:
                params = (course_id, name, difficult, student, desc, label, image_urls, detail, duration,
                          overall_score, content_score, concise_score, logic_score, summary, teacher_nickname,
                          teacher_avatar, teacher_job, tip, can_learn, now, now)
                effect_count = self.postgres.handler(add_course(), params)
                if effect_count > 0:
                    self.redis.set(key, str_now)

        if isinstance(item, items.CodingItem):
            # 实战课程
            price = item['price']
            coding_id = item['coding_id']
            video = item['video']
            small_title = item['small_title']
            detail_desc = item['detail_desc']

            key = 'imooc:coding:{0}'.format(coding_id)
            if self.redis.exists(key):
                params = (student, price, overall_score, now, coding_id)
                self.postgres.handler(update_coding(), params)
            else:
                params = (coding_id, name, difficult, student, desc, image_urls, price, detail,
                          overall_score, teacher_nickname, teacher_avatar, duration, video, small_title,
                          detail_desc, teacher_job, now, now)
                effect_count = self.postgres.handler(add_coding(), params)
                if effect_count > 0:
                    self.redis.set(key, str_now)

        return item

    def close_spider(self, spider):
        self.postgres.close()


def add_course():
    sql = 'insert into tb_imooc_course(course_id,"name",difficult,student,"desc",label,image_urls,' \
          'detail,duration,overall_score,content_score,concise_score,logic_score,summary,' \
          'teacher_nickname,teacher_avatar,teacher_job,tip,can_learn,update_time,create_time) ' \
          'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    return sql


def update_course():
    sql = 'update tb_imooc_course set student=%s,overall_score=%s,content_score=%s,concise_score=%s,' \
          'logic_score=%s,update_time=%s where course_id = %s'
    return sql


def add_coding():
    sql = 'insert into tb_imooc_coding(coding_id,"name",difficult,student,"desc",image_urls,price,detail,' \
          'overall_score,teacher_nickname,teacher_avatar,duration,video,small_title,detail_desc,teacher_job,' \
          'update_time,create_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    return sql


def update_coding():
    sql = 'update tb_imooc_coding set student=%s,price=%s,overall_score=%s,update_time=%s where coding_id = %s'
    return sql

  最后，别忘了要在settings.py中手动开启pipelines配置：





配置pipelines

运行爬虫
  启动上述Scrapy爬虫，可分别使用命令scrapy crawl course和scrapy crawl coding运行，如果不想每次都要输入这么麻烦， 可以Scrapy提供的API将启动命令编码到py中，再用python命令运行该脚本即可，具体可参考如下：
from scrapy.cmdline import execute

# 免费课程
execute(['scrapy', 'crawl', 'course'])
# 实战课程
execute('scrapy crawl coding'.split(' '))

数据展示
  实际运行中并没有看到有相关的反爬虫限制，可能是因为整体数据量不大（免费课程有900多，实战课程有100多门），借助Scrapy的多线程能力（setting.py中的CONCURRENT_REQUESTS配置，默认是16）很快也就抓取完了：






