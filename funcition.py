import tgt
import glob
import statistics
import numpy as np
import allperson as ap


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


def deltaC(C_duration):
    deltaC = round(statistics.stdev(C_duration), 4)  # 取标准差 使用 python statistic 模块
    return deltaC


def deltaV(V_duration):
    deltaV = round(statistics.stdev(V_duration), 4)  # 取标准差 使用 python statistic 模块
    return deltaV


def rPVI_c(Duration):
    # print(len(Duration)) rpvi的 计算方式 公式 如图
    i = 0
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


def rPVI_V(Duration):
    # print(len(Duration))
    i = 0
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


def nPVI_C(Duration):
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


def nPVI_V(Duration):
    # print(len(Duration))
    i = 0
    sum = 0
    for i in range(len(Duration)):
        a = abs(Duration[i] - Duration[i - 1])
        b = abs((Duration[i] + Duration[i - 1]) / 2)
        #print(b)
        c = abs(a / b)
        i = i + 1
        # print(a)
        sum = sum + c
    #value = round((sum * (1 / len(Duration)) * 100), 4)
    value = sum * (100 / (len(Duration)-1))
    return value


def deltaS(S_duration):
    deltaS = round(statistics.stdev(S_duration), 4)  # 取标准差 使用 python statistic 模块
    return deltaS


def rPVI_s(Duration):
    # print(len(Duration)) rpvi的 计算方式 公式 如图
    i = 0
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



def duration(path, C_list, V_list,mode,cid):
    # path="E:\coorpus"
    # path_cn = 'F:\SAITCorpus\CN'
    # path = 'F:\SAITCorpus'
    #if mode = # 传递 参数
    #if len(path) < 14: # 判断是否 是 计算国家 / 发音人( 路径结构略不一样）
    if mode == 'country':
        file_list = glob.glob(path + r"\*\sent\*.TextGrid")  # glob匹配所有的符合条件的文件，并将以list的形式返回 国家
    elif mode == 'spker':
        file_list = glob.glob(path + r"\sent\*.TextGrid")  # glob匹配所有的符合条件的文件，并将以list的形式返回 国家
    #else:  #ditto
    #file_list=glob.glob(path + r"\sent\*.TextGrid") # 发音人；

    # print('filename',',', '%V\t',',', 'deltaC\t', ',', 'deltaV\t')
    # print(file_list)

    AlldeltC = [] # 依次计算 每一个 textgrid 的 结果值 把结果存在 总列表中
    AlldeltV = []
    all_vc = []
    all_vv = []
    all_rpvic = []
    all_rpviv = [] # 可能有点问题 每次累加进去 一个值 但是 不清空
    all_npvic = []
    all_npviv = []
    all_pctV = []
    for file in file_list:
        TextGrid = tgt.read_textgrid(file, include_empty_intervals=True)  # 依次读取TextGrid文件
        if cid == 'cn':
            tier = TextGrid.get_tier_by_name(TextGrid.get_tier_names()[2])
            #print(tier)
        elif cid == 'jp':
            tier = TextGrid.get_tier_by_name(TextGrid.get_tier_names()[1])
        elif cid == 'ru':
            tier = TextGrid.get_tier_by_name(TextGrid.get_tier_names()[2])
        #tier_syll = TextGrid.get_tier_by_name(TextGrid.get_tier_names()[1]) #根据 tier的 name/位置 读取 intervals
        #tier = TextGrid.get_tier_by_name('SY')
        tier_name = TextGrid.get_tier_names()  # 获取全部的tier 名字
        start = tier.start_time
        end = tier.end_time
        tier2insert = tgt.IntervalTier(start, end, name='CV') # 获取起始点和 终点 插入一条 CV的 intervals
        TextGrid.insert_tier(tier2insert, 3)
        CV = TextGrid.get_tier_by_name('CV')
        annotation = tier.intervals  # 插入一个 intervals
        num = []
        C_duration = [] # 每一个 intervals 的 时长信息 表
        V_duration = []
        duration_all_C = 0 # 全部时长和 （用于计算 %V 和 其他相关参数）
        duration_all_V = 0
        for i in range(len(annotation)): # 循环 替换 和 计算 时长
            old_name = annotation[i].text
            old_start_time = annotation[i].start_time
            old_end_time = annotation[i].end_time
            duration = old_end_time - old_start_time

            if old_name in C_list: # 判断 属于 C / V
                new_name = 'C'
            elif old_name in V_list: # 判断 属于 C / V
                new_name = 'V'
            else:
                new_name = 'none'

            Interval = tgt.Interval(old_start_time, old_end_time, text=new_name)  # interval格式- 依次填写
            # print(old_name, new_name, 'duration=', duration)
            if new_name == 'C':
                C_duration.append(duration) #加入 duration 的list
                duration_all_C = duration_all_C + duration

            elif new_name == 'V':
                V_duration.append(duration)
                duration_all_V += duration
            CV.add_interval(Interval) # 将 intervals 的标注 >> 到 textgrid
        a = duration_all_V + duration_all_C # 句子时长(去除 sli）
        pctV = duration_all_V/a
        #mean_syl = a / (len(C_duration) + len(V_duration)) # 计算一个 mean_syllable duration 用于 语速
        #print(mean_syl)
        #print(len(C_duration))

        vacC = duration_all_C / len(C_duration)
        vacV = duration_all_V / len(V_duration)
        #vacroC = round(deltaC(C_duration) / vacC * 100, 4)
        #vacroV = round(deltaC(V_duration) / vacV * 100, 4)
        vacroC = deltaC(C_duration) / vacC * 100
        vacroV = deltaC(V_duration) / vacV * 100
        # print(file, ',',
        #
        #       deltaC(C_duration), ',',
        #       deltaV(V_duration), ',',
        #
        #       vacroC, ',',
        #       vacroV, ',',
        #
        #       rPVI_c(C_duration), ',',
        #       rPVI_V(V_duration), ',',
        #
        #       nPVI_C(C_duration), ',',
        #       nPVI_V(V_duration), ',',
        #
        #       )

        AlldeltC.append(deltaC(C_duration))
        AlldeltV.append(deltaV(V_duration))
        all_vc.append(vacroC)
        all_vv.append(vacroV)
        all_rpvic.append(rPVI_c(C_duration))
        all_rpviv.append(rPVI_V(V_duration))
        all_npvic.append(nPVI_C(C_duration))
        all_npviv.append(nPVI_V(V_duration))
        all_pctV.append(pctV)
    deltC = round(np.mean(AlldeltC),9)
    deltV = round(np.mean(AlldeltV),9)
    vc = round(np.mean(all_vc),9)
    vv = round(np.mean(all_vv),9)
    rpvic = round(np.mean(all_rpvic),9)
    rpviv = round(np.mean(all_rpviv),9)
    npvic = round(np.mean(all_npvic),9)
    npviv = round(np.mean(all_npviv),9)
    perctV = round(np.mean(all_pctV),9)

    print(path,',',
          perctV,',',
          deltC,',',
          deltV,',',
          vc,',',
          vv,',',
          rpvic,',',
          rpviv,',',
          npvic,',',
          npviv,','
          )
        # return file,C_duration,V_duration
        # print('%V value = ', duration_all_V / (duration_all_V + duration_all_C))
        # return C_duration,V_duration


a, b = CV_list()
#path = "F:\SAITCorpus_SENT\JP"
#duration(path, a, b,'country')
#duration(path, a, b,'spker')

# path_ps = 'E:\coorpus\F001'
# duration(path_ps,a,b)
