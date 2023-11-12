import pandas as pd
import os

# 读取主CSV文件
main_file = 'D:/李文/Documents/Python/draft/rapid/ExtraInfo.csv'  # 主要的CSV文件
df_main = pd.read_csv(main_file)

# 设置目录路径
directory = 'D:/李文/Documents/Python/RapidAPI数据/Basic_Mine'  # 包含其他CSV文件的目录

# 获取目录下所有CSV文件
files = [file for file in os.listdir(directory) if file.endswith('.csv')]

# 循环处理每个文件
for file in files:
    file_path = os.path.join(directory, file)

    # 读取当前文件
    df = pd.read_csv(file_path)

    # 连接具有相同链接的行
    merged_df = pd.merge(df_main, df, on='API链接')

    # 将合并的数据保存为新的CSV文件
    merged_df.to_csv(f'D:/李文/Documents/Python/RapidAPI数据/Connect/{file}', index=False, encoding='utf_8_sig')

    # 打印合并后的数据
    print(merged_df)
