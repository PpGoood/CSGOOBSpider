import os
import pandas as pd

# 定义文件夹路径和目标字符串
folder_path = r'G:\Desktop\python项目\uuDemo\dataExcel'
target_string = "悠悠有品近6个月"

# 获取文件夹中所有Excel文件的列表
excel_files = [file for file in os.listdir(folder_path) if file.endswith('.xlsx')]

# 遍历所有Excel文件，检查文件名并删除不需要的文件
for file in excel_files:
    file_path = os.path.join(folder_path, file)
    print("正在检查文件",file)
    # 检查文件名是否包含目标字符串
    if target_string not in file:
        os.remove(file_path)
        # 检查是否包含 "求购最高价" 列
    # 读取Excel文件
    df = pd.read_excel(file_path,skiprows=6)
    if "求购最高价" not in df.columns:
        os.remove(file_path)  # 如果没有该列，删除文件
        print('删除文件',file)