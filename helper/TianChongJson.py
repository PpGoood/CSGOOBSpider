import json

# 读取原始JSON文件
with open(r'G:\Desktop\python项目\uuDemo\dataHistory\sorted_merged.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

exterior_order = {
    "崭新出厂": 1,
    "略有磨损": 2,
    "久经沙场": 3,
    "破损不堪": 4,
    "战痕累累": 5
}

# 创建一个字典来记录前半段出现的次数
front_part_count = {}

# 创建一个字典来记录前半段对应的后半段集合
front_part_to_exterior = {}

# 创建一个集合来记录所有商品名称
all_commodity_names = set()

# 遍历数据
for item in data:
    commodity_name = item.get('CommodityName', '')

    # 找到括号的位置
    start_index = commodity_name.rfind('(')
    end_index = commodity_name.rfind(')')

    if start_index != -1 and end_index != -1:
        # 提取前半段和后半段
        front_part = commodity_name[:start_index].strip()
        exterior = commodity_name[start_index + 1:end_index]
    else:
        front_part = commodity_name
        exterior = ''

    # 检查前半段是否已经记录
    if front_part in front_part_count:
        # 更新后半段集合
        front_part_to_exterior[front_part].add(exterior)
    else:
        # 记录前半段并创建后半段集合
        front_part_count[front_part] = 1
        front_part_to_exterior[front_part] = {exterior}

    # 记录商品名称
    all_commodity_names.add(commodity_name)

# 遍历记录，查找缺失的后半段
missing_items = []
for front_part, ext_set in front_part_to_exterior.items():
    missing_ext = set(exterior_order.keys()) - ext_set
    if missing_ext:
        for ext in missing_ext:
            missing_items.append(f"{front_part} ({ext})")

# 输出缺失的项
for commodity_name in all_commodity_names:
    if commodity_name not in front_part_to_exterior:
        missing_items.append(commodity_name)

# 在此处添加您要创建的新项
for missing_item in missing_items:
    new_item = {
        "stickersIsSort": False,
        "subsidyPurchase": 0,
        "stickers": {},
        "label": None,
        "minLeaseDeposit": None,
        "Id": 43790,  # 设置一个新的ID，或者根据需要进行更改
        "IsFavorite": None,
        "GameId": "补充",  # 补充GameId
        "GameName": "CS:GO",
        "GameIcon": "https://youpin.img898.com/logo/csgo.png",
        "CommodityName": missing_item,  # 使用缺失的商品名称
        "CommodityHashName": "AK-47 | Jungle Spray (Field-Tested)",  # 补充商品HashName
        "IconUrl": "https://youpin.img898.com/economy/image/90da136a60aa11ec86c8dca9049909c3",
        "IconUrlLarge": "https://youpin.img898.com/economy/image/3b0a6d16614711ecb073acde48001122",
        "OnSaleCount": 133,  # 补充其他属性
        "OnLeaseCount": 38,
        "LeaseUnitPrice": "0.1",
        "LongLeaseUnitPrice": "0.12",
        "LeaseDeposit": "60",
        "Price": "54.5",
        "SteamPrice": "54.6",
        "SteamUSDPrice": "6.72",
        "TypeName": "步枪",
        "Exterior": "破损不堪",  # 使用缺失的外观
        "ExteriorColor": "F0AD4E",
        "Rarity": "工业级",
        "RarityColor": "5E98D9",
        "Quality": "普通",
        "QualityColor": "B2B2B2",
        "SortId": 43790,  # 设置新的SortId
        "HaveLease": 1,
        "Rent": "0.1"
    }

    # 将新项添加到数据中
    data.append(new_item)

# 保存更新后的数据到JSON文件
with open(r'G:\Desktop\python项目\uuDemo\dataHistory\sorted_merged.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
