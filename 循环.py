import tgt
import glob
import statistics
import numpy as np

import os

def metircs(path):
    C_list = []
    V_list = []
    file = open(r'C:\Users\GIGABYTE\Desktop\VC_classification.txt')
    with file as f:
        lines = f.readlines()
    C_list = lines = [line.rstrip('\n\t') for line in open(r'C:\Users\GIGABYTE\Desktop\VC_classification.txt')]
    file1 = open(r'C:\Users\GIGABYTE\Desktop\All_V.txt')
    with file1 as f1:
        lines1 = f1.readlines()
    V_list = lines1 = [line.rstrip('\n\t') for line in open(r'C:\Users\GIGABYTE\Desktop\All_V.txt')] #切分 VC 列表
    print(V_list, C_list)

    # path="E:\coorpus"
    # path_cn = 'F:\SAITCorpus\CN'

    # path = 'F:\SAITCorpus'

    file_list=glob.glob(path + r"\*\sent\*.TextGrid") #glob匹配所有的符合条件的文件，并将以list的形式返回
    file_list=glob.glob(path + r"\sent\*.TextGrid") #glob匹配所有的符合条件的文件，并将以list的形式返回

    print('filename\t', '%V\t', 'deltaC\t', 'deltaV\t')
    for file in file_list:
        TextGrid=tgt.read_textgrid(file, include_empty_intervals=True) #读取TextGrid文件
        #tier = TextGrid.get_tier_by_name(TextGrid.get_tier_names()[2])
        tier = TextGrid.get_tier_by_name(TextGrid.get_tier_names()[1])
        tier_name = TextGrid.get_tier_names()  # 获取全部的tier 名字
        start = tier.start_time
        end = tier.end_time
        tier2insert = tgt.IntervalTier(start, end, name='CV')
        TextGrid.insert_tier(tier2insert, 3)
        CV = TextGrid.get_tier_by_name('CV')
        annotation = tier.intervals
        AlldeltC = []
        AlldeltV = []
        C_duration = []
        V_duration = []
        duration_all_C = 0
        duration_all_V = 0
        for i in range(len(annotation)):
            old_name = annotation[i].text
            old_start_time = annotation[i].start_time
            old_end_time = annotation[i].end_time
            duration = old_end_time-old_start_time
            if old_name in C_list:
                new_name = 'C'
            elif old_name in V_list:
                new_name = 'V'
            else:
                new_name = 'none'

            #print(old_name, new_name)
            Interval = tgt.Interval(old_start_time, old_end_time, text=new_name) #interval格式
            #print(old_name, new_name, 'duration=', duration)
            if new_name == 'C':
                C_duration.append(duration)
                duration_all_C = duration_all_C+duration
            elif new_name == 'V':
                V_duration.append(duration)
                duration_all_V += duration
            CV.add_interval(Interval)
        #print(V_duration)
        #print('%V value = ', duration_all_V / (duration_all_V + duration_all_C))
        V = duration_all_V/(duration_all_V + duration_all_C)
        deltaC = statistics.stdev(C_duration)  # 取标准差 使用 python statistic 模块
        deltaV = statistics.stdev(V_duration)  # ditto

        #print(deltaV)
        a = round(V*100, 2)
        b = round(deltaC*100, 2)
        c = round(deltaV*100, 2)
        #print(file, ',', a, ',', b, ',', c)
        AlldeltC.append(deltaC)
        AlldeltV.append(deltaV)

        C = np.mean(AlldeltC)
        V = np.mean(AlldeltV)
        #print(file, '\t', C, '\t', V)
        C_ALL = []
        C_ALL.append(C)
        V_ALL = []
        V_ALL.append(V)

    print(np.mean(C_ALL), np.mean(V_ALL))
    print('all set!')


#
# path_VN = 'F:\SAITCorpus\VN'
# path_RU = 'F:\SAITCorpus\RU'
# path_JP = 'F:\SAITCorpus\JP'
path="E:\coorpus\F001"
metircs(path)
#metircs(path_RU)
#metircs(path_VN)
