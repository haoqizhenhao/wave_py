# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 09:21:43 2018
@author: haoqi
"""
import numpy as np
from wave_process import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy as sp
from pandas import Series
from scipy import interpolate
from scipy import signal

def wave_diff(a, n=1, axis=-1):
    '''
    function：差分
        后期需要根据输入数据形式，对函数进行优化
    input:
        data:数据； n:阶次； axis:差分的维度
    output:
        返回结果
    '''
    if n == 0:
        return a
    if n < 0:
        raise ValueError(
            "order must be non-negative but got " + repr(n))

    a = np.asanyarray(a)
    nd = a.ndim
    #axis = normalize_axis_index(axis, nd)

    slice1 = [slice(None)] * nd
    slice2 = [slice(None)] * nd
    slice1[axis] = slice(1, None)
    slice2[axis] = slice(None, -1)
    slice1 = tuple(slice1)
    slice2 = tuple(slice2)

    #op = not_equal if a.dtype == np.bool_ else subtract
    for _ in range(n):
        a = np.subtract(a[slice1], a[slice2])

    return a

def find_peak(a):
    '''
    function:寻找波峰波谷
    input:数据
    outpu：
        count_peak：波峰位置
        y_peak：波峰值
        count_start：起始点位置
        y_start：起始点幅值
    '''
    # 求波峰
    pm = np.amax(a)
    G = 0.5*pm
#    a_large = np.where(a>G, a, 0)
    a_large = np.maximum(a, G)
    count_peak, y_peak = peak(a_large)
    # 将误识别点去除
    count_peak = count_peak[-1::-1]
    y_peak = y_peak[-1::-1]
    
    count_peak_diff = wave_diff(count_peak, n=1, axis=-1)
    need_to_delet = np.where(count_peak_diff>-100)
    count_peak = np.delete(count_peak, need_to_delet, axis = 0)
    y_peak = np.delete(y_peak, need_to_delet, axis = 0)

    count_peak = count_peak[-1::-1]
    y_peak = y_peak[-1::-1]
  
    # 求波谷-起始点
    ps = np.min(a)
    G2 = 0.5 * ps
    a_start = np.minimum(a, G2)
    count_start, y_start = valley(a_start)
    # 将误识别点去除
    count_start_diff = wave_diff(count_start, n=1, axis=-1)
    need_to_delet = np.where(count_start_diff<100)
    count_start = np.delete(count_start, need_to_delet, axis = 0)
    y_start = np.delete(y_start, need_to_delet, axis = 0)
    return count_peak, y_peak, count_start, y_start

def find_peak1(a):
    '''
    function:寻找波峰波谷
    input:数据
    outpu：
        count_peak：波峰位置
        y_peak：波峰值
        count_start：起始点位置
        y_start：起始点幅值
    '''
    # 求波峰
    pm = np.amax(a)
    G = 0.5*pm
#    a_large = np.where(a>G, a, 0)
    a_large = np.maximum(a, G)
    count_peak, y_peak = peak1(a_large)
    # 将误识别点去除
    count_peak = count_peak[-1::-1]
    y_peak = y_peak[-1::-1]
    
    count_peak_diff = wave_diff(count_peak, n=1, axis=-1)
    need_to_delet = np.where(count_peak_diff>-100)
    count_peak = np.delete(count_peak, need_to_delet, axis = 0)
    y_peak = np.delete(y_peak, need_to_delet, axis = 0)

    count_peak = count_peak[-1::-1]
    y_peak = y_peak[-1::-1]
  
    # 求波谷-起始点
    #ps = np.min(a)
    G2 = 0.4 * pm
    a_start = np.minimum(a, G2)  
    count_start, y_start = valley1(a_start)
    # 将误识别点去除
    count_start_diff = wave_diff(count_start, n=1, axis=-1)
    need_to_delet = np.where(count_start_diff<100)
    count_start = np.delete(count_start, need_to_delet, axis = 0)
    y_start = np.delete(y_start, need_to_delet, axis = 0)
    return count_peak, y_peak, count_start, y_start

def peak(a,n=1):
    '''
    function:寻找波峰，通过差分
    '''
    a_diff = wave_diff(a, n=n, axis=-1)
    N = len(a_diff)-n

    loc_peak = []
    y_peak = []
    for i in range(N):
        if a_diff[i] >= 0 and a_diff[i+1] < 0:
            loc_peak.append(i+n)
            y_peak.append(a[i+n])
    loc_peak = np.asarray(loc_peak)
    y_peak = np.asarray(y_peak)
    return loc_peak, y_peak

def peak1(a):
    '''
    function:通过原图形求极大值
    '''
    N = len(a)-2
    loc_peak1 = []
    y_peak1 = []
    for i in range(N):
        if a[i]<=a[i+1] and a[i+1]>a[i+2]:
            loc_peak1.append(i+1)
            y_peak1.append(a[i+1])
    loc_peak1 = np.asarray(loc_peak1)
    y_peak1 = np.asarray(y_peak1)
    return loc_peak1, y_peak1

def valley(a,n=1):
    '''
    function:寻找波谷，通过差分
    '''
    a_diff = wave_diff(a, n=n, axis=-1)
    N = len(a_diff)-1
    
    loc_valley = []
    y_valley = []
    for i in range(N):
        if a_diff[i] < 0 and a_diff[i+1] >= 0:
            loc_valley.append(i+1)
            y_valley.append(a[i+1])
    loc_valley = np.asarray(loc_valley)
    y_valley = np.asarray(y_valley)
    return loc_valley, y_valley

def valley1(a):
    '''
    function:通过原图形求极小值
    '''
    N = len(a)-2
    loc_valley1 = []
    y_valley1 = []
    for i in range(N):
        if a[i]>=a[i+1] and a[i+1]<a[i+2]:
            loc_valley1.append(i+1)
            y_valley1.append(a[i+1])
    loc_valley1 = np.asarray(loc_valley1)
    y_valley1 = np.asarray(y_valley1)
    return loc_valley1, y_valley1

def cutting(a, count_start):
    '''
    function:截取出周期波形
    '''
#    cuttings = []
#    for i in np.arange(len(count_start)-1):
#        cuttings.append(a[count_start[i]:count_start[i+1]])
    cuttings = np.array([a[count_start[i]:count_start[i+1]] for i in np.arange(len(count_start)-1)])
    return cuttings

def wave_average(a):
    '''
    function:平均波形提取，以起始点为对齐点
    input:滤波后的波形
    output:
        wave:平均波形
    '''
    _, _, count_start, _ = find_peak(a)
    cuttings = cutting(a, count_start)
    
    length = np.array([len(k) for k in cuttings])
    mark = length < 220
    length = length[mark]
    cuttings = cuttings[mark]
    
    m = np.mean(length)
    v = np.std(length) #标准差
    
    # 选出标准差小于2倍标准差的周期
    mark = np.abs(length-m)<=1.8*v
    cuttings = cuttings[mark]
    
    cuttings = mark_by_ystd(cuttings)
    length = np.array([len(kk) for kk in cuttings])
    m_length = int(round(np.mean(length)))
    
    length_length = len(length)
    # 取均值数的数据
    cuttings_new = np.array([])
    for i in range(length_length):
        if length[i] >= m_length:
            cuttings_new = np.append(cuttings_new, cuttings[i][0:m_length])
        if length[i] < m_length: # 长度不足均值的数据填充最后一个值
            cuttings_a = cuttings[i]
            for j in range(m_length-length[i]):
                cuttings_a = np.append(cuttings_a,cuttings[i][-1])
            cuttings_new = np.append(cuttings_new, cuttings_a)
    
    cuttings_new = cuttings_new.reshape([length_length,m_length])
    wave = np.mean(cuttings_new,axis = 0)
    wave = wave-min(wave)
    # 计算周期
    
    return wave

def wave_average_by_fit(a):
    '''
    function:
        平均波形提取，以起始点为对齐点
        通过插值的办法重采样
    input:滤波后的波形
    output:
        wave:平均波形
    '''
    _, _, count_start, _ = find_peak(a)
    cuttings = cutting(a, count_start)
    
    length = np.array([len(i) for i in cuttings])
    m = np.mean(length)
    v = np.std(length) #标准差
    
    # 选出标准差小于2倍标准差的周期
    mark = np.abs(length-m)<=1.8*v
    cuttings = cuttings[mark]
    length = length[mark]
    m_length = int(round(np.mean(length)))
#    m_length = max(length)
    length_length = len(length)
    # 取均值数的数据
    cuttings_new = np.array([])
    for cut in cuttings:
        cuttings_new = np.append(cuttings_new, fit(cut,n=m_length)[1])
    cuttings_new = cuttings_new.reshape([length_length,m_length])
    wave = np.mean(cuttings_new,axis = 0)
    
    return wave

def wave_T(fs = 200, length = 200):
    '''
    function:心率，通过起始点求取
    备注：后期可增加波峰求取
    '''
    return int(round(fs*60/length))

    
def find_features(wave):
    '''
    function：寻找特征点
    '''
    n_move = 2
    wave_fstdif = wave_diff(wave)
    
    m_length = len(wave)
    wave_secdif = wave_diff(wave,n=2)
    wave_thrdif = wave_diff(wave,n=3)
    
    #wave_secdif,_ = smooth(wave_diff(wave,n=2),n=3)
    #wave_thrdif,_ = smooth(wave_diff(wave,n=3),n=3)
    
    #print(i, w_T, len(count_peak)*2)
    
    # 波峰
    loc_peak, y_peak = peak1(wave)
    # 波谷
    loc_valley, y_valley = valley1(wave)
    
    wave_fstdif1 = wave_fstdif[0:100] #取一阶差分的前100点分析
    loc_peak1, y_peak1 = peak1(wave_fstdif1)    #求一阶差分曲线有几个波峰
    #   求二阶差分曲线的波峰、波谷
    loc_peak2, y_peak2 = peak1(wave_secdif)
    loc_valley2, y_valley2 = valley1(wave_secdif)
    #   删除不合理的波峰波谷
    #loc_peak = loc_peak[loc_peak<120]
    #loc_valley = loc_valley[loc_valley<100] # 这两个值决定了最后有没有误判点，此方法不通用，以后需改进
    loc_peak = loc_peak[0:3]
    loc_valley = loc_valley[0:2]
    
    loc_peak_new = np.array([])
    loc_valley_new = np.array([])
    #loc_valley_new = np.append(loc_valley_new,loc_valley)
    
#    seq = ('H1','H2','H3','H4','H5')
#    dict_features = dict.fromkeys(seq,0)
    
    if len(loc_peak) == 3:
        loc_peak_new = np.append(loc_peak_new,loc_peak)
        loc_valley_new = np.append(loc_valley_new,loc_valley)
        
#        dict_features['H1'], dict_features['H3'], dict_features['H5'] = loc_peak_new[0],loc_peak_new[1],loc_peak_new[2]
#        dict_features['H2'], dict_features['H4'] = loc_valley_new[0], loc_valley_new[1]
        
    if len(loc_peak) == 2:
        loc_peak_new = np.append(loc_peak_new,loc_peak[0])
        loc_valley_new = np.append(loc_valley_new,loc_valley)
        
#        dict_features['H1'] = loc_peak_new[0]
        
        #判断第二个波峰是潮波还是重搏波
        if (loc_peak[1]-loc_peak[0])/m_length <= 0.2:   #if True,为潮波
            loc_peak_new = np.append(loc_peak_new,loc_peak[1])
            
#            dict_features['H3'] = loc_peak_new[1]
#            dict_features['H2'] = loc_valley_new[0]
            
            #通过二阶差分判断是否有不明显的重搏波
            if len(loc_peak1) == 3: #有三个波峰，则证明有不明显的重搏波
                #此处可能由于二阶差分不准确造成误判，后期加入辅助判断
                #取出重搏波
                loc_peak2 = loc_peak2[loc_peak2<loc_peak1[2]]   #通过二阶变化曲线求圆滑过渡两边波峰波谷的点
                loc_valley_new = np.append(loc_valley_new,loc_peak2[-1]+n_move)
                
                loc_valley2 = loc_valley2[loc_valley2>loc_peak1[2]]
                loc_peak_new = np.append(loc_peak_new,loc_valley2[0])
                
#                dict_features['H4'] = loc_valley_new[1]
#                dict_features['H5'] = loc_peak_new[2]
                
                #loc_peak_new = np.append(loc_peak_new,loc_peak1[2])  #加入中点位置,后期需要去掉
                
        else:   #为重搏波
            #通过二阶差分判断是否有不明显的潮波，由于二阶差分误差较大，判断并不是很准确，需要改进
#            dict_features['H4'] = loc_valley_new[0]
            
            
            if len(loc_peak1) == 3: #有三个波峰，则证明有不明显的潮波
                loc_peak2 = loc_peak2[loc_peak2<loc_peak1[1]]
                loc_valley2 = loc_valley2[loc_valley2>loc_peak1[1]]
                
                #slope = (wave[loc_valley2[0]] - wave[loc_peak2[-1]+2]) / (loc_valley2[0] - (loc_peak2[-1] + 2))
                
                #if slope >= -0.005 :
                loc_valley_new = np.append(loc_valley_new,loc_peak2[-1]+n_move)
                loc_peak_new = np.append(loc_peak_new,loc_valley2[0])   #加入潮波位置
                
                #loc_peak_new = np.append(loc_peak_new,loc_peak1[1])  #加入中点位置,后期需要去掉
                loc_peak_new = np.append(loc_peak_new,loc_peak[1])   #加入重搏波位置
                
#                dict_features['H2'] = loc_valley_new[1]
#                dict_features['H3'] = loc_peak_new[-1]
            else: #没有潮波
                loc_peak_new = np.append(loc_peak_new,loc_peak[1])   #加入重搏波位置
#            dict_features['H5'] = loc_peak_new[-1]
                
    if len(loc_peak) == 1:
        loc_peak_new = np.append(loc_peak_new,loc_peak)
        if len(loc_peak1[1::]):
            for z in loc_peak1[1::]:
                loc_peak22 = loc_peak2
                loc_valley22 = loc_valley2
                
                loc_peak22 = loc_peak22[loc_peak22<z]
                loc_valley_new = np.append(loc_valley_new,loc_peak22[-1]+n_move)
                
                loc_valley22 = loc_valley22[loc_valley22>z]
                loc_peak_new = np.append(loc_peak_new,loc_valley22[0])
    
#    else:
#        print('数据有误，请重新测量')
    
    loc_peak_new = np.sort(loc_peak_new)
    loc_valley_new = np.sort(loc_valley_new)
    
    y_peak_new = np.array([])
    y_valley_new = np.array([])
    for j in loc_peak_new:
        y_peak_new = np.append(y_peak_new,wave[int(j)])
    for k in loc_valley_new:
        y_valley_new = np.append(y_valley_new,wave[int(k)])

    return loc_peak_new, y_peak_new, loc_valley_new, y_valley_new

def features_choose(wave,loc_peak, y_peak, loc_valley, y_valley):
    '''去除不合理特征'''
    loc_peak_new = np.array([])
    loc_valley_new = np.array([])
#    y_peak_new = y_peak[0]
#    y_valley_new = np.array([])
    loc_peak_new = np.append(loc_peak_new, loc_peak[0])
    if len(loc_valley):
        for i in np.arange(len(loc_valley)):
            slope = (y_peak[i+1] - y_valley[i]) / (loc_peak[i+1] - loc_valley[i])
            if slope >= -0.004 :
                loc_peak_new = np.append(loc_peak_new, loc_peak[i+1])
                loc_valley_new = np.append(loc_valley_new, loc_valley[i])
                
#                y_peak_new = np.append(y_peak_new, y_peak[i+1])
#                y_valley_new = np.append(y_valley_new, y_valley[i])
    y_peak_new = np.array([])
    y_valley_new = np.array([])
    for j in loc_peak_new:
        y_peak_new = np.append(y_peak_new,wave[int(j)])
    for k in loc_valley_new:
        y_valley_new = np.append(y_valley_new,wave[int(k)])
    
    
    return loc_peak_new, y_peak_new, loc_valley_new, y_valley_new
        
def features_dict(wave,loc_peak, y_peak, loc_valley, y_valley):
    '''把特征点存在字典中'''
    length = len(wave)
    seq = ('wave','H1','H2','H3','H4','H5')
    dict_features = dict.fromkeys(seq,[0,0])
    dict_features['wave'] = wave
    if len(loc_peak)==3 and len(loc_valley)==2:
        if loc_peak[0]<loc_valley[0]<loc_peak[1]<loc_valley[1]<loc_peak[2]:
            dict_features['H1'] = [loc_peak[0],y_peak[0]]
            dict_features['H3'] = [loc_peak[1],y_peak[1]]
            dict_features['H5'] = [loc_peak[2],y_peak[2]]
            
            dict_features['H2']=[loc_valley[0],y_valley[0]]
            dict_features['H4']=[loc_valley[1],y_valley[1]]
            
    if len(loc_peak)==2 and len(loc_valley)==1:
        #判断第二个波峰是潮波还是重搏波
        dict_features['H1']=[loc_peak[0],y_peak[0]]
        if (loc_peak[1]-loc_peak[0])/length <= 0.2:   #if True,为潮波
            dict_features['H3']=[loc_peak[1],y_peak[1]]
            dict_features['H2']=[loc_valley[0],y_valley[0]]
        else :
            dict_features['H5']=[loc_peak[1],y_peak[1]]
            dict_features['H4']=[loc_valley[0],y_valley[0]]
    if len(loc_peak)==1 and len(loc_valley)==0:
        dict_features['H1']=[loc_peak[0],y_peak[0]]
#    else:
#        print('数据有误，请重新测量')
    return dict_features

def values(dict_features):
    '''获取特征参数'''
    length = len(dict_features['wave'])
    
    f = 200*60/length
    
    t1_divide_T = dict_features['H1'][0]/length
    t2_divide_T = dict_features['H2'][0]/length
    t3_divide_T = dict_features['H3'][0]/length
    t4_divide_T = dict_features['H4'][0]/length
    t5_divide_T = dict_features['H5'][0]/length
    
    H1 = dict_features['H1'][1]
    
    H2_divide_H1 = dict_features['H2'][1]/H1
    H3_divide_H1 = dict_features['H3'][1]/H1
    H4_divide_H1 = dict_features['H4'][1]/H1
    H5_divide_H1 = dict_features['H5'][1]/H1
    
    H32_divide_H1 = (dict_features['H3'][1]-dict_features['H2'][1])/H1
    H54_divide_H1 = (dict_features['H5'][1]-dict_features['H4'][1])/H1
    
    values_features = {}
    
    values_features['wave'] = dict_features['wave']
    
    values_features['f'] = f
    values_features['t1_divide_T'] = t1_divide_T
    values_features['t2_divide_T'] = t2_divide_T
    values_features['t3_divide_T'] = t3_divide_T
    values_features['t4_divide_T'] = t4_divide_T
    values_features['t5_divide_T'] = t5_divide_T
    
    values_features['H1'] = H1
    values_features['H2_divide_H1'] = H2_divide_H1
    values_features['H3_divide_H1'] = H3_divide_H1
    values_features['H4_divide_H1'] = H4_divide_H1
    values_features['H5_divide_H1'] = H5_divide_H1
    
    values_features['H32_divide_H1'] = H32_divide_H1
    values_features['H54_divide_H1'] = H54_divide_H1
    
    return values_features
    
def find_features1(wave):
    '''
    function：直接通过求局部极值的方式求波峰波谷
    '''
    loc_peak1, y_peak1 = peak1(wave)
    loc_valley1, y_valley1 = valley1(wave)
    mark_p = loc_peak1<120
    mark_v = loc_valley1<120
    
    loc_peak1 = loc_peak1[mark_p]
    loc_valley1 = loc_valley1[mark_v]
    
    y_peak1 = y_peak1[mark_p]
    y_valley1 = y_valley1[mark_v]
    
    return loc_peak1,y_peak1,loc_valley1,y_valley1

def get_figure(wave,loc_peak_new, y_peak_new, loc_valley_new, y_valley_new):
    '''
    function:将特征体现在图中
    '''
    plt.figure()
    length = len(wave)
    T = wave_T(fs = 200, length = length)
    mpl.rcParams['font.sans-serif'] = [u'SimHei']
    mpl.rcParams['axes.unicode_minus'] = False
    plt.plot(wave,label=u'平均脉象波形')
    plt.xlabel('点数(N)')
    plt.ylabel('脉压')
    plt.title('脉象图')
    plt.scatter(loc_peak_new,y_peak_new,label='波峰',color='k')
    plt.scatter(loc_valley_new,y_valley_new,label='波谷',color='r',marker = '<')
    plt.text(loc_peak_new[0],min(wave),'心率：{}'.format(T),fontsize=12)
    plt.legend(loc='upper right')
    plt.grid(True)
    
def fit(a,n):
    '''
    function:数据拟合，采用B-spline插值的方法
    input:
        a:数据
        n:拟合后数据量
    '''
    x = np.arange(len(a))
    x_new = np.linspace(0, len(a), n)
    tck = interpolate.splrep(x, a)
    a_bspline = interpolate.splev(x_new, tck)
    return x_new,a_bspline

def breath(wave):
    '''
    function:提取呼吸率
    '''
    b,a = signal.butter(5,0.002,'high')
    sf = signal.filtfilt(b,a,wave)
    
    b,a = signal.butter(5,0.004,'low')
    sf = signal.filtfilt(b,a,sf)
    return sf
    
def breath_average(wave):
    '''
    function:求呼吸波平均值
    '''
    loc,y = peak(wave)
    cuttings = cutting(wave, loc)
    
    length = np.array([len(i) for i in cuttings])
    m = np.mean(length)
    v = np.std(length) #标准差
    
    # 选出标准差小于2倍标准差的周期
    mark = np.abs(length-m)<=1*v
    cuttings = cuttings[mark]
    length = length[mark]
    m_length = int(round(np.mean(length)))
#    m_length = max(length)
    length_length = len(length)
    # 取均值数的数据
    cuttings_new = np.array([])
    for cut in cuttings:
        cuttings_new = np.append(cuttings_new, fit(cut,n=m_length)[1])
    cuttings_new = cuttings_new.reshape([length_length,m_length])
    wave = np.mean(cuttings_new,axis = 0)
    
    return wave

def K(a):
    '''
    function:计算波形K值
    '''
    return (np.mean(a)-min(a))/(max(a)-min(a))

#def pm(a):
#    '''
#    function:平均脉压
#    '''
#    return np.mean(a)
    
def y_std(cuttings,list_save = [20,40,60,80,100]):
    '''求剪切信号y值的方差'''
    a = np.array([])
    for i in cuttings:
        a = np.append(a,i[list_save])
    a = a.reshape(cuttings.shape[0],5)
    a_std = np.std(a,axis=0)
    a_mean = np.mean(a,axis=0)
    mark = np.abs(a - a_mean)<=2*a_std
    mark1 = mark[:,0] & mark[:,1] & mark[:,2] & mark[:,3] & mark[:,4]
    return mark1
        
def mark_by_ystd(cuttings):
    
    mark = y_std(cuttings,list_save = [20,40,60,80,100])
    
    return (cuttings[mark])

def figure_cuttings(a):
    count_peak, y_peak, count_start, y_start = find_peak(a)
    cuttings = cutting(a, count_start)
    
    length = np.array([len(k) for k in cuttings])
    mark = length < 220
    length = length[mark]
    cuttings = cuttings[mark]
    
    m = np.mean(length)
    v = np.std(length) #标准差
    
    # 选出标准差小于2倍标准差的周期
    
    #cuttings1 = cuttings[mark]
    mark = np.abs(length-m)<=1.8*v
    cuttings1 = cuttings[mark]
    cuttings2 = mark_by_ystd(cuttings1)
    
    plt.figure()
    plt.subplot(211)
    for j in cuttings1:
        plt.plot(j)
    plt.text(100,0,'数量：{}'.format(cuttings1.shape[0]),fontsize=12)
    plt.subplot(212)
    for ii in cuttings2:
        plt.plot(ii)
    plt.text(100,0,'数量：{}'.format(cuttings2.shape[0]),fontsize=12)