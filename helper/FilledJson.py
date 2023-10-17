import json

# 读取原始JSON文件
with open(r'G:\Desktop\python项目\uuDemo\dataHistory\merged.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 初始化一个空列表，用于存储满足条件的item
filtered_data = []

# 遍历JSON中的每个item
for item in data:
    commodity_name = item.get('CommodityName', '').lower()  # 获取CommodityName属性并转换为小写
    price_str = item.get('Price', '0.00')  # 获取Price属性，默认值为'0.00'
    type_name = item.get('TypeName')  # 获取TypeName属性
    gameId = item.get('GameId','')
    if(gameId == '补充'):
        continue
    if type_name is not None:
        type_name = type_name.lower()  # 将TypeName属性转换为小写

    try:
        price = float(price_str)  # 尝试将价格字符串转换为浮点数
    except ValueError:
        price = 0.00  # 转换失败时，默认价格为0.00

    # 检查是否包含关键词并且价格大于等于10，以及TypeName不是匕首或手套
    if ('印花' not in commodity_name and '布章' not in commodity_name) and price >= 30.00 and (type_name is None or type_name not in ['匕首', '手套','其他']):
        filtered_data.append(item)
    else:
        # 打印被删除的item
        print(f"删除的item: {item}")

# 统计剩余item的数量
remaining_count = len(filtered_data)
print(f"剩余的item数量: {remaining_count}")

# 保存满足条件的item到新的JSON文件
with open(r'G:\Desktop\python项目\uuDemo\merged.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=4)
