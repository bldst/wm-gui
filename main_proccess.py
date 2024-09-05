import json
from datetime import datetime, timedelta

import requests


class RivenOrdersProcess:

    def __init__(self, weapon_url, days, count_orders):
        self.days = days
        self.weapon_url = weapon_url
        self.count_orders = count_orders
        self.orders_json = []


    #查找价格
    def get_riven_price_(self, weapon_url):
        try:
            RivenOrders = requests.get(
                url=f'https://api.warframe.market/v1/auctions/search?type=riven&weapon_url_name={weapon_url}&sort_by=price_asc')
            return RivenOrders.json()
        except requests.RequestException as e:

            return None

    # 对订单主要信息提取(默认保留days天内的前15个售卖订单)
    def extract_and_filter_orders(self, orders_json, count_orders, days=30):
        """
               提取并筛选订单数据。

               根据给定的时间范围和订单数量限制，从JSON订单数据中提取并筛选出符合条件的订单。
               该函数主要关注在指定天数内创建的直接购买订单（排除拍卖订单）。

               参数:
               orders_json : dict
                   包含订单数据的JSON格式字典。
               count_orders : int
                   需要返回的订单数量限制。
               days : int, optional
                   筛选订单的时间范围（以天为单位，默认为30天）。

               返回:
               list
                   筛选后的订单列表。
               """
        if orders_json is None:
            return []
        orders = orders_json['payload']['auctions']
        # 获取当前日期时间
        now = datetime.now()
        # 计算一个月前的日期
        one_month_ago = now - timedelta(days=days)
        #保存符合条件的订单列表
        filter_orders_res = []
        #订单计数器
        count = 0

        # 提取一个月内的售卖订单
        for order in orders:
            #如果是拍卖订单直接跳过
            if order['starting_price'] != order['buyout_price']:
                continue
            create_time = datetime.fromisoformat(order['created'].replace("T", " ").replace("+00:00", ""))
            #如果订单在指定天数内，就保存该订单
            if one_month_ago <= create_time:
                filter_orders_res.append(order)

            #订单保留数量
            if count >= count_orders:
                break
            count += 1
        return filter_orders_res

    #分析订单，提取重要项目
    def analysis_orders(self, orders):

        return
