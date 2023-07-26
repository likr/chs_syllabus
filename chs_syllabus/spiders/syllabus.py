import scrapy


class SyllabusSpider(scrapy.Spider):
    name = 'syllabus'
    allowed_domains = ['syllabus.chs.nihon-u.ac.jp']
    start_urls = [
        # 全学共通教育科目
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_40.html',
        # 総合教育科目
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_1.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_2.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_3.html',
        # 基礎教育科目
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_4.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_5.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_6.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_7.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_8.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_9.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_10.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_11.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_12.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_13.html',
        # コース科目
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_14.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_15.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_16.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_17.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_18.html',
        # 学科専門科目 人文系
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_22.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_23.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_24.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_25.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_26.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_27.html',
        # 学科専門科目 社会系
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_28.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_29.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_30.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_31.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_32.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_33.html',
        # 学科専門科目 理学系
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_34.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_35.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_36.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_37.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_38.html',
        'https://syllabus.chs.nihon-u.ac.jp/op/list1_39.html',
    ]

    def parse(self, response):
        for href in response.css('#Main > div.Contents.br_clear > div > table > tbody > tr > td:nth-child(1) > a::attr(href)'):
            url = 'https://syllabus.chs.nihon-u.ac.jp/' + href.get()[3:]
            yield scrapy.Request(url, callback=self.parse_item)

    def parse_item(self, response):
        record = {}
        fields = zip(
            response.css('.table_1 th, table:nth-child(4) td.norm'),
            response.css('.table_1 td, table:nth-child(4) td.norm + td')
        )
        for key, value in fields:
            key = ' '.join(key.css('*::text').get().strip().split())
            value = ' '.join(value.css('*::text').get().strip().split())
            record[key] = value
        record['授業計画'] = []
        for value in response.css('table:nth-child(3) td.number + td'):
            value = ' '.join(value.css('*::text').get().strip().split())
            record['授業計画'].append(value)
        yield record
