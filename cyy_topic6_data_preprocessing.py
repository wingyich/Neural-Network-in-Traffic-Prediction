# -*- coding: utf-8 -*-
#!/usr/bin/env python

import pandas as pd
import numpy as np
import glob
from sklearn import preprocessing


FILE_NUMS = 33

# 读取所有.txt 文件的列 Read the columns of all.txt files
def read_files():
    allframes = pd.DataFrame()
    list_ = []
    for i in range(FILE_NUMS):
        path = r'C:\Users\25080\OneDrive - University College London\Desktop\numerical method and application\PEMS\station' + str(i+1)
        print(f"Reading files from: {path}")  # 调试输出路径 Debug output path
        allfiles = glob.glob(path + "/*.txt")
        if len(allfiles) == 0:
            print(f"No files found in: {path}")  # 输出如果没有找到文件 Output if the file is not found
            continue  # 如果没有找到文件，跳过当前文件夹 If no file is found, skip the current folder
        frame_ = []
        for file_ in allfiles:
            print(f"Reading file: {file_}")  # 输出当前读取的文件 Output the currently read file
            table = pd.read_table(file_, usecols=[0,1])
            frame_.append(table)
        frame = pd.concat(frame_)
        list_.append(frame)
    if len(list_) == 0:
        print("No data was read from any files.")  # 如果没有数据，输出提示 If no data is available, a message is displayed
        return pd.DataFrame()  # 返回空的数据帧 Return an empty data frame
    allframes = pd.concat(list_)
    print("Finished reading all files.")
    return allframes

# 按时间序列对数据分组并标准化 Group and standardize data by time series
def group_by_time():
    frame = read_files()
    if frame.empty:
        print("No data to process.")
        return []
    print("Converting '5 Minutes' to datetime.")
    frame['5 Minutes'] = pd.to_datetime(frame['5 Minutes'], format='%m/%d/%Y %H:%M', errors='coerce')
    frame = frame.dropna(subset=['5 Minutes'])  # 如果日期解析失败会生成 NaT，这里删除 If the date resolution fails, NaT will be generated, which is deleted here
    values = frame.groupby('5 Minutes')['Flow (Veh/5 Minutes)'].apply(list)
    vehicles = []
    for i in range(len(values)):
        vehicles.append(values[i])
    print("Finished grouping data.")
    return vehicles

vehicles = group_by_time()
if len(vehicles) > 0:
    print("Scaling data with MinMaxScaler.")
    scaler = preprocessing.MinMaxScaler()
    samples = scaler.fit_transform(vehicles)
else:
    print("No vehicles data available to scale.")
    samples = []

# 将处理后的数据保存为CSV文件 Save the processed data as a CSV file
def save_to_csv(data, filename):
    if len(data) > 0:
        print(f"Saving data to {filename}")
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print("File saved successfully.")
    else:
        print("No data to save.")

# 保存标准化后的样本数据  Save standardized sample data
save_to_csv(samples, 'normalized_data.csv')