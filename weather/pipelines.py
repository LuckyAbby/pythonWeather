# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests
import json
import codecs
import pymysql

class WeatherPipeline(object):
    def process_item(self, item, spider):
        base_dir = os.getcwd()
        fiename = base_dir + '/data/weather.txt'
        try:
            with open(fiename, 'a') as f:
                f.write(item['date'] + '\n')
                f.write(item['week'] + '\n')
                f.write(item['temp'] + '\n')
                f.write(item['air'] + '\n')
                f.write(item['wind'] + '\n\n')

            with open(base_dir + '/data/' + item['date'] + '.png', 'wb') as f:
                f.write(requests.get(item['img']).content)
        except:
            print('写文件txt失败')
            return 'error'

        return item

class W2Json(object):
    def process_item(self, item, spider):
        base_dir = os.getcwd()
        filename = base_dir + '/data/weather.json'
        with codecs.open(filename, 'a') as f:
            line = json.dumps(dict(item), ensure_ascii = False) + '\n'
            f.write(line)
        return item

class W2Mysql(object):
    def process_item(self, item, spider):
        date = item['date']
        week = item['week']
        img = item['img']
        air = item['air']
        wind = item['wind']
        temp = item['temp']
        config = {
          'host':'127.0.0.1',
          'user':'root',
          'password':'root',
          'db':'pyWeather',
          'charset':'utf8mb4',
          'cursorclass':pymysql.cursors.DictCursor,
          }

        connection = pymysql.connect(**config)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO WEATHER(date, week, img, temp, air, wind)VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (date, week, img, temp, air, wind))
            connection.commit()
        finally:
            connection.close()
        return item
