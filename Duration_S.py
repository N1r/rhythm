import tgt
import glob
import statistics
import numpy as np
import allperson as ap
def deltaS(S_duration):
    deltaS = round(statistics.stdev(S_duration), 4)  # 取标准差 使用 python statistic 模块
    return deltaS
def rPVI_s(Duration):
    # print(len(Duration)) rpvi的 计算方式 公式 如图
    i =0
    sum = 0
    for i in range(len(Duration)):
        a = abs(Duration[i] - Duration[i - 1])
        i = i + 1
        # print(a)
        sum = sum + a
    #value = round((sum * (1 / len(Duration)) * 100), 4)
    value = sum * (1 / (len(Duration)-1))

    return value
    #     print(sum),
def nPVI_S(Duration):
    # print(len(Duration)) npvi的 计算方式 公式 如图
    i = 0
    # i = 的起始段 是否 有问题
    sum = 0
    for i in range(len(Duration)):
        a = abs(Duration[i] - Duration[i - 1])
        b = abs((Duration[i] + Duration[i - 1]) / 2)
        c = abs(a / b)
        i = i + 1
        # print(a)
        sum = sum + c
    #value = round((sum * (1 / len(Duration)) * 100), 4)
    value = sum * (100 / (len(Duration)-1))

    return value



def CV_list():
    C_list = []
    V_list = []
    file = open(r'C:\Users\GIGABYTE\Desktop\VC_classification.txt')
    with file as f:
        lines = f.readlines()
    C_list = lines = [line.rstrip('\n\t') for line in open(r'C:\Users\GIGABYTE\Desktop\VC_classification.txt')]
    file1 = open(r'C:\Users\GIGABYTE\Desktop\All_V.txt')
    with file1 as f1:
        lines1 = f1.readlines()
    V_list = lines1 = [line.rstrip('\n\t') for line in open(r'C:\Users\GIGABYTE\Desktop\All_V.txt')]  # 切分 VC 列表
    # print(V_list, '\n', C_list)
    return C_list, V_list  # c_v list 需要提前准备好 分别读取到两个列表中



def duration(path, C_list, V_list, cid):
    #file_list = glob.glob(path + r"\*\sent\*.TextGrid")  # glob匹配所有的符合条件的文件，并将以list的形式返回
    file_list = glob.glob(path + r"\sent\*.TextGrid")  # glob匹配所有的符合条件的文件，并将以list的形式返回
    #print(file_list)
    AlldeltS = []  # 依次计算 每一个 textgrid 的 结果值 把结果存在 总列表中
    all_vs = []
    all_rpvis = []  # 可能有点问题 每次累加进去 一个值 但是 不清空
    all_npvis = []
    all_ms = []
    for file in file_list:
        TextGrid = tgt.read_textgrid(file, include_empty_intervals=True)  # 依次读取TextGrid文件
        if cid == 'jp':
            tier = TextGrid.get_tier_by_name(TextGrid.get_tier_names()[0])
            #print(tier)
        if cid == 'cn':
            tier = TextGrid.get_tier_by_name(TextGrid.get_tier_names()[0])
            #print(tier)
        elif cid == 'ru':
            tier = TextGrid.get_tier_by_name(TextGrid.get_tier_names()[1])  # 根据 tier的 name/位置 读取 intervals
            #print(tier)
        # tier = TextGrid.get_tier_by_name('SY')
        tier_name = TextGrid.get_tier_names()  # 获取全部的tier 名字
        start = tier.start_time
        end = tier.end_time
        start_syl = tier.start_time
        end_syl = tier.end_time
        tier2insert = tgt.IntervalTier(start, end, name='CV')  # 获取起始点和 终点 插入一条 CV的 intervals
        TextGrid.insert_tier(tier2insert, 3)
        CV = TextGrid.get_tier_by_name('CV')
        annotation = tier.intervals  # 插入一个 intervals
        #syllable = tier_syll.intervals
        num = []
        S_duration = []  # syllable_duration
        duration_all_S = 0  # 全部时长和 （用于计算 %V 和 其他相关参数）

        for i in range(len(annotation)):  # 循环 替换 和 计算 时长
            old_name = annotation[i].text
            old_start_time = annotation[i].start_time
            old_end_time = annotation[i].end_time
            duration = old_end_time - old_start_time
            #if old_name in C_list:  # 判断 属于 C / V
            if old_name != 'sil':
                new_name = 'S'
            # elif old_name in V_list:  # 判断 属于 C / V
            #     new_name = 'S'
            else:
                new_name = 'none'

            # print(old_name, new_name)
            Interval = tgt.Interval(old_start_time, old_end_time, text=new_name)  # interval格式- 依次填写
            # print(old_name, new_name, 'duration=', duration)
            if new_name == 'S':
                S_duration.append(duration)  # 加入 duration 的list
                duration_all_S = duration_all_S + duration

            CV.add_interval(Interval)  # 将 intervals 的标注 >> 到 textgrid
        #print(file, S_duration)
        mean_syl = duration_all_S/len(S_duration)
        #print(mean_syl)
        vacS = duration_all_S / len(S_duration)
        # print(num)
        # if num > 0:
        # mean_syl = a / (len(C_duration) + len(V_duration)) # 计算一个 mean_syllable duration 用于 语速
        # print(mean_syl)
        # mean_syl = a/(len(C_duration)+len(V_duration))
        # print(mean_syl)
        #       vacroC = round(deltaC(C_duration) / mean_syl * 100, 4)
        #       vacroV = round(deltaC(V_duration) / mean_syl * 100, 4)
        vacroS = round(deltaS(S_duration) / vacS * 100, 4)
        # print(file, ',',
        #
        #       deltaS(S_duration), ',',
        #
        #       vacroS, ',',
        #
        #       rPVI_s(S_duration), ',',
        #
        #       nPVI_S(S_duration), ',',
        #       )
        #print(nPVI_S(S_duration))
        AlldeltS.append(deltaS(S_duration))
        all_vs.append(vacroS)
        all_rpvis.append(rPVI_s(S_duration))
        all_npvis.append(nPVI_S(S_duration))
        all_ms.append(mean_syl)
    deltS = round(np.mean(AlldeltS), 9)
    vs = round(np.mean(all_vs), 9)
    rpvis = round(np.mean(all_rpvis), 9)
    npvis = round(np.mean(all_npvis), 9)
    ms = round(np.mean(all_ms), 9)

    #
    print(path, ',',
          ms, ',',
          deltS, ',',
          vs, ',',
          rpvis, ',',
          npvis, ',',
          )
    # return file,C_duration,V_duration
    # print(V_duration)
    # print('%V value = ', duration_all_V / (duration_all_V + duration_all_C))
    # return C_duration,V_duration

#
a, b = CV_list()
#path = "E:\COUNTRY\RU"
#path = 'F:\\SAITCorpus_SENT\\JP'
#duration(path, a, b,'ru')
