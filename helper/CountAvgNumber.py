import os
import pandas as pd

# 指定包含Excel文件的文件夹路径
folder_path = r"G:\Desktop\python项目\uuDemo\dataExcel"

# 获取文件夹中所有的Excel文件
excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# 创建一个空的DataFrame用于存储所有数据
all_data = pd.DataFrame()

# 创建一个空的DataFrame用于存储统计结果
all_stats = pd.DataFrame(columns=['文件名', '平均天数'])

# 循环读取每个Excel文件并将数据添加到all_data中
for i, excel_file in enumerate(excel_files, start=1):
    file_path = os.path.join(folder_path, excel_file)
    print(f"正在处理文件 {i}/{len(excel_files)}: {excel_file}")
    df = pd.read_excel(file_path, skiprows=6)  # 跳过前6行无关信息
    all_data = all_data._append(df, ignore_index=True)

    # 提取文件名（去掉文件扩展名）
    file_name = os.path.splitext(excel_file)[0]

    # 计算平均天数
    df['时间'] = pd.to_datetime(df['时间'])
    avg_days = len(df) / ((df['时间'].max() - df['时间'].min()).days + 1)

    # 将统计结果添加到总的DataFrame中
    all_stats = all_stats._append({'文件名': file_name, '平均天数': avg_days}, ignore_index=True)

# 输出平均天数统计结果
print(all_stats)

# 将统计结果保存到新的Excel文件
output_file = r"G:\Desktop\python项目\uuDemo\dataExcel\average_days.xlsx"
all_stats.to_excel(output_file, index=False)

print(f"平均天数统计结果已保存到 {output_file}")
