import json

# 读取原始JSON文件
with open(r'G:\Desktop\python项目\uuDemo\dataHistory\filtered_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 创建一个集合来存储已经出现过的 CommodityName 值
commodity_names = set()

# 创建一个新的列表，用于存储过滤后的数据
filtered_data = []

# 遍历 JSON 数据
for item in data:
    commodity_name = item.get('CommodityName', '')
    game_id = item.get('GameId', '')

    # 检查是否存在重复的 CommodityName 值，且 GameId 为 "补充"，以及不包含 "纪念品"
    if (
        commodity_name in commodity_names
        and game_id == "补充"
        or "纪念品"  in commodity_name
    ):
        # 如果满足条件，则跳过该项
        continue

    # 将 CommodityName 添加到集合中
    commodity_names.add(commodity_name)

    # 添加项到过滤后的数据列表
    filtered_data.append(item)

# 输出过滤后的数据到新的 JSON 文件
with open(r'G:\Desktop\python项目\uuDemo\dataHistory\filtered_data.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=4)
