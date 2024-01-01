import json
import re

# 定义商品名称的后缀列表
suffixes = ["(崭新出厂)", "(略有磨损)", "(久经沙场)", "(战痕累累)", "(破损不堪)"]

# 打开已有的 JSON 文件，如果不存在则创建一个新的商品列表
try:
    with open(r'G:\Desktop\python项目\uuDemo\dataHistory\filtered_data.json', "r", encoding="utf-8") as json_file:
        commodities = json.load(json_file)
except FileNotFoundError:
    commodities = []

# 用户输入商品名称
while True:
    commodity_input = input("请输入商品名称 (输入 'exit' 退出)：")

    # 检查用户是否要退出
    if commodity_input.lower() == 'exit':
        break

    # 使用正则表达式来查找输入中的最后一个带空格的数字
    match = re.search(r'\d+(?=\s*$)', commodity_input)

    if match:
        item_index = int(match.group())
    else:
        item_index = None

    # 商品名称是输入的名称去掉最后一个带空格的数字
    commodity_name = re.sub(r'\d+\s*$', '', commodity_input).strip()

    # 如果用户输入了数字索引，则只创建指定的商品项
    if item_index is not None:
        if 0 <= item_index < len(suffixes):
            suffix = suffixes[item_index]

            # 创建指定的商品项
            item_template = {
                "stickersIsSort": False,
                "subsidyPurchase": 0,
                "stickers": {},
                "label": None,
                "minLeaseDeposit": None,
                "Id": 43790,
                "IsFavorite": None,
                "GameId": "补充",
                "GameName": "CS:GO",
                "GameIcon": "https://youpin.img898.com/logo/csgo.png",
                "CommodityName": commodity_name + " " + suffix,
                "CommodityHashName": "AK-47 | Jungle Spray (Field-Tested)",
                "IconUrl": "https://youpin.img898.com/economy/image/90da136a60aa11ec86c8dca9049909c3",
                "IconUrlLarge": "https://youpin.img898.com/economy/image/3b0a6d16614711ecb073acde48001122",
                "OnSaleCount": 133,
                "OnLeaseCount": 38,
                "LeaseUnitPrice": "0.1",
                "LongLeaseUnitPrice": "0.12",
                "LeaseDeposit": "60",
                "Price": "54.5",
                "SteamPrice": "54.6",
                "SteamUSDPrice": "6.72",
                "TypeName": "步枪",
                "Exterior": "破损不堪",
                "ExteriorColor": "F0AD4E",
                "Rarity": "工业级",
                "RarityColor": "5E98D9",
                "Quality": "普通",
                "QualityColor": "B2B2B2",
                "SortId": 43790,
                "HaveLease": 1,
                "Rent": "0.1"
            }
            commodities.append(item_template)
        else:
            #原封不动创建
            # 创建指定的商品项
            item_template = {
                "stickersIsSort": False,
                "subsidyPurchase": 0,
                "stickers": {},
                "label": None,
                "minLeaseDeposit": None,
                "Id": 43790,
                "IsFavorite": None,
                "GameId": "补充",
                "GameName": "CS:GO",
                "GameIcon": "https://youpin.img898.com/logo/csgo.png",
                "CommodityName": commodity_name,
                "CommodityHashName": "AK-47 | Jungle Spray (Field-Tested)",
                "IconUrl": "https://youpin.img898.com/economy/image/90da136a60aa11ec86c8dca9049909c3",
                "IconUrlLarge": "https://youpin.img898.com/economy/image/3b0a6d16614711ecb073acde48001122",
                "OnSaleCount": 133,
                "OnLeaseCount": 38,
                "LeaseUnitPrice": "0.1",
                "LongLeaseUnitPrice": "0.12",
                "LeaseDeposit": "60",
                "Price": "54.5",
                "SteamPrice": "54.6",
                "SteamUSDPrice": "6.72",
                "TypeName": "步枪",
                "Exterior": "破损不堪",
                "ExteriorColor": "F0AD4E",
                "Rarity": "工业级",
                "RarityColor": "5E98D9",
                "Quality": "普通",
                "QualityColor": "B2B2B2",
                "SortId": 43790,
                "HaveLease": 1,
                "Rent": "0.1"
            }
            commodities.append(item_template)
    else:
        # 用户没有输入数字索引，创建所有商品项
        for suffix in suffixes:
            item_template = {
                "stickersIsSort": False,
                "subsidyPurchase": 0,
                "stickers": {},
                "label": None,
                "minLeaseDeposit": None,
                "Id": 43790,
                "IsFavorite": None,
                "GameId": "补充",
                "GameName": "CS:GO",
                "GameIcon": "https://youpin.img898.com/logo/csgo.png",
                "CommodityName": commodity_name + " " + suffix,
                "CommodityHashName": "AK-47 | Jungle Spray (Field-Tested)",
                "IconUrl": "https://youpin.img898.com/economy/image/90da136a60aa11ec86c8dca9049909c3",
                "IconUrlLarge": "https://youpin.img898.com/economy/image/3b0a6d16614711ecb073acde48001122",
                "OnSaleCount": 133,
                "OnLeaseCount": 38,
                "LeaseUnitPrice": "0.1",
                "LongLeaseUnitPrice": "0.12",
                "LeaseDeposit": "60",
                "Price": "54.5",
                "SteamPrice": "54.6",
                "SteamUSDPrice": "6.72",
                "TypeName": "步枪",
                "Exterior": "破损不堪",
                "ExteriorColor": "F0AD4E",
                "Rarity": "工业级",
                "RarityColor": "5E98D9",
                "Quality": "普通",
                "QualityColor": "B2B2B2",
                "SortId": 43790,
                "HaveLease": 1,
                "Rent": "0.1"
            }
            commodities.append(item_template)

# 将商品列表保存到JSON文件中
with open(r'G:\Desktop\python项目\uuDemo\dataHistory\filtered_data.json', "w", encoding="utf-8") as json_file:
    json.dump(commodities, json_file, ensure_ascii=False, indent=4)

print("商品已成功添加到 filtered_data.json 文件中。")
