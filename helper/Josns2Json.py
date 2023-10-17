import json
import os

# 定义一个空列表用于存储所有JSON数据
all_data = []

# 指定包含JSON文件的文件夹路径
folder_path = r'G:\Desktop\python项目\uuDemo\dataHistory'

# 遍历文件夹中的每个JSON文件
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # 迭代每个元素，只将具有 'CommodityName' 属性的元素添加到列表中
            filtered_data = [item for item in data if 'CommodityName' in item]
            all_data.extend(filtered_data)

# 使用一个字典来去除重复元素，以 "Id" 作为键
unique_data_dict = {}
for item in all_data:
    unique_data_dict[item['Id']] = item

# 将字典中的唯一数据转换回列表
unique_data = list(unique_data_dict.values())

# 将去重后的数据写入新的JSON文件
output_file_path = r'G:\Desktop\python项目\uuDemo\merged.json'
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(unique_data, output_file, ensure_ascii=False, indent=4)

print(f'去重后的元素数量: {len(unique_data)}')