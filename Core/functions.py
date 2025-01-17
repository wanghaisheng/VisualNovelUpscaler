# -*- coding:utf-8 -*-

import os
import sys
import csv
import json
import time
import math
import uuid
import zlib
import shutil
import hashlib
import logging
import tempfile
import traceback
import subprocess
import configparser
from threading import Thread
from functools import partial
from io import StringIO as PrivateStringIO
from multiprocessing import Pool, cpu_count, Process, freeze_support
# 第三方库
import png
import construct
import regex as re
from wmi import WMI
from PIL import Image
import numpy as np
from numba import jit
# 自定义库
from .pathplus import Path


def get_gpu_list() -> list:
    """
    @brief      获取显卡名称列表

    @return     返回显卡名称列表
    """
    GPUs = WMI().Win32_VideoController()
    GPU_name_list = [i.name for i in GPUs]
    return GPU_name_list


def get_gpu_id(GPU_name) -> str:
    """
    @brief      获取显卡ID

    @param      GPU_name  显卡名

    @return     返回显卡ID
    """
    GPU_name_list = get_gpu_list()
    GPU_ID = str(GPU_name_list.index(GPU_name))
    return GPU_ID


def real_digit(str1) -> bool:
    """
    @brief      判断字符串是否为数字

    @param      str1  字符串

    @return     布尔值
    """
    try:
        tmp = float(str1)
        return True
    except:
        return False


def pattern_num2x(re_result, scale_ratio, test_mode=False, line=None) -> str:
    """
    @brief      将正则匹配结果中的数字乘以放大倍数

    @param      re_result    re.match()捕获的正则匹配结果
    @param      scale_ratio  放大倍数
    @param      test_mode    测试模式
    @param      line         原始行字符串，需要test_mode为True

    @return     放大数字后的行字符串
    """
    re_result_ls = list(re_result.groups())
    if test_mode:
        print(line)
        print(re_result_ls)
    for i in range(len(re_result_ls)):
        if real_digit(re_result_ls[i]):
            if test_mode:
                print(re_result_ls[i], sep=', ')
            re_result_ls[i] = str(int(float(re_result_ls[i])*scale_ratio))
    re_result_ls = [i for i in re_result_ls if i != None]
    line = ''.join(re_result_ls)
    if test_mode:
        print(line)
    return line


def seconds_format(time_length) -> str:
    """
    @brief      将秒格式化输出为时分秒

    @param      time_length  时长

    @return     输出字符串
    """
    m, s = divmod(time_length, 60)
    h, m = divmod(m, 60)
    return "%02dh%02dm%02ds" % (h, m, s)


def batch_group_list(inlist, batch_size=10) -> list:
    """
    @brief      将列表以指定大小划分为多个列表

    @param      inlist      输入列表
    @param      batch_size  每个列表元素数量

    @return     划分列表的列表
    """
    group_list = []
    start_index = 0
    while True:
        end_index = start_index+batch_size
        group = inlist[start_index:end_index]
        if group == []:
            break
        group_list.append(group)
        start_index = end_index
    return group_list


def pool_run(workers, target, runs, *args) -> list:
    """
    @brief      使用进程池多进程加速计算

    @param      workers  进程数
    @param      target   目标执行函数
    @param      runs     执行可变参数迭代器
    @param      args     其它固定参数，按执行函数参数顺序输入

    @return     将执行函数的返回值以列表返回
    """
    pool = Pool(workers)
    processer_ls = []
    for i in runs:
        processer = pool.apply_async(target, args=(i, *args))
        processer_ls.append(processer)
    pool.close()
    pool.join()
    return [processer.get() for processer in processer_ls]


def show_folder(folder_path):
    """
    @brief      显示文件夹

    @param      folder_path  文件夹路径
    """
    folder_path = Path(folder_path)
    _p = subprocess.run(['start', folder_path], capture_output=True, shell=True)


def sub_scale_num(match, scale_ratio):
    """
    @brief      用于放大正则替换匹配到的数字pattern.sub(partial(sub_scale_num, scale_ratio), line)

    @param      match        The match
    @param      scale_ratio  放大倍数

    @return     放大后的数字
    """
    num_ = match.group()
    scaled_num_ = str(int(float(num_) * scale_ratio))
    return scaled_num_
