import os
import re
import pandas as pd

# 文件夹路径
folder_path = r'G:\Desktop\python项目\uuDemo\dataExcel'  # 修改为你的文件夹路径
output_file = r'G:\Desktop\python项目\uuDemo\csgo_uu求购利润率.xlsx'  # 修改为你的输出文件路径
target_string1 = "悠悠有品近1个月"
target_string2 = "Buff近1个月"
count = 0
pattern = r'\(\d+\)\.xlsx$'

# 创建一个空的DataFrame来存储合并后的数据
merged_data = pd.DataFrame(columns=["武器名", "时间", "价格", "求购最高价格", "在售数量", "利润率"])

# 创建一个列表来记录需要删除的文件
files_to_delete = []

# 遍历文件夹中的每个Excel表格文件
for file_name in os.listdir(folder_path):
    count = count + 1
    print("正在进行：", count, "/", len(os.listdir(folder_path)))
    if file_name.endswith('.xlsx'):
        file_path = os.path.join(folder_path, file_name)

        # 使用正则表达式来判断文件名是否以 (数字).xlsx 结尾
        if re.search(pattern, file_name):
            # 记录需要删除的文件
            files_to_delete.append(file_path)
            print("记录删除文件", file_name)
            continue

        # 检查文件是否存在
        if os.path.exists(file_path):
            # 读取Excel文件
            excel_data = pd.read_excel(file_path, skiprows=6)

            # 检查文件名是否包含目标字符串
            if target_string1 in file_name or target_string2 in file_name:
                # 检查是否包含 "价格" 和 "求购最高价" 列
                if "价格" in excel_data.columns and "求购最高价" in excel_data.columns:
                    # 获取最后一行数据
                    last_row = excel_data.iloc[-1]

                    # 计算利润率
                    profit_margin = (last_row['价格'] - last_row['求购最高价']) / last_row['价格']

                    sale_count = 0
                    if "在售数量" in excel_data.columns:
                        sale_count = last_row['在售数量']
                    # 添加数据到merged_data
                    merged_data = merged_data._append({
                        "武器名": file_name[file_name.find('【')+1:file_name.find('】')],
                        "时间": last_row['时间'],
                        "价格": last_row['价格'],
                        "求购最高价格": last_row['求购最高价'],
                        "在售数量": sale_count,
                        "利润率": profit_margin
                    }, ignore_index=True)
                else:
                    # 如果缺少所需的列，打印文件名
                    print(f"文件 '{file_name}' 缺少所需的列，将被跳过。")
                    # 记录需要删除的文件
                    files_to_delete.append(file_path)
                    print("记录删除文件", file_name)
            else:
                # 记录需要删除的文件
                files_to_delete.append(file_path)
                print("记录删除文件", file_name)

# 根据利润率对merged_data进行排序
merged_data = merged_data.sort_values(by="利润率", ascending=False)

# 将合并后的数据保存为一个新的Excel文件
merged_data.to_excel(output_file, index=False)

# 遍历需要删除的文件列表并删除这些文件
for file_to_delete in files_to_delete:
    os.remove(file_to_delete)
    print("删除文件", file_to_delete)
