import json

# 读取原始JSON文件
with open(r'G:\Desktop\python项目\uuDemo\dataHistory\filtered_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
# 定义 Exterior 排序规则
exterior_order = {
    "崭新出厂": 1,
    "略有磨损": 2,
    "久经沙场": 3,
    "破损不堪": 4,
    "战痕累累": 5
}
# 自定义排序函数，按照 "CommodityName" 的名称部分排序，然后按后半段的元素排序
def custom_sort(item):
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
    print(front_part)
    print(exterior)
    return (front_part,  exterior_order.get(exterior, 0))

# 对数据进行排序
sorted_data = sorted(data, key=custom_sort)

# 保存排序后的数据到新的JSON文件
with open(r'G:\Desktop\python项目\uuDemo\dataHistory\filtered_data.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_data, f, ensure_ascii=False, indent=4)
