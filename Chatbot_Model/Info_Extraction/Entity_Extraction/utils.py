#-*- coding:utf-8 _*-
"""
@author:charlesXu
@file: utils.py
@desc: 实体提取预处理工具类
@time: 2018/08/08
"""

import logging, sys, argparse

from functools import reduce


def str2bool(v):
    # copy from StackOverflow
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_entity(tag_seq, char_seq):
    PER = get_PER_entity(tag_seq, char_seq)
    # LOC = get_LOC_entity(tag_seq, char_seq)
    LOC = get_loc_entitys(tag_seq, char_seq)
    ORG = get_ORG_entity(tag_seq, char_seq)
    return PER, LOC, ORG


def get_PER_entity(tag_seq, char_seq):
    length = len(char_seq)
    PER = []
    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-PER':
            if 'per' in locals().keys():
                PER.append(per)
                del per
            per = char
            if i+1 == length:
                PER.append(per)
        if tag == 'I-PER':
            per += char
            if i+1 == length:
                PER.append(per)
        if tag not in ['I-PER', 'B-PER']:
            if 'per' in locals().keys():
                PER.append(per)
                del per
            continue
    PER = list(set(PER))     #  去重
    return PER


def get_LOC_entity(tag_seq, char_seq):
    '''
    这里需要对输出序列进行判断，对连续序列进行拼接
    :param tag_seq:
    :param char_seq:
    :return:
    '''
    length = len(char_seq)
    LOC = []
    location = []
    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-LOC':
            if 'loc' in locals().keys():
                LOC.append(loc)
                del loc
            loc = char
            if i+1 == length:
                LOC.append(loc)
        # if tag_seq[i] == 'B-LOC' and tag_seq[i - 1] == 'I-LOC':
        #     loc += char
        if tag == 'I-LOC':
            loc += char
            if i+1 == length:
                LOC.append(loc)
        if tag not in ['I-LOC', 'B-LOC']:
            if 'loc' in locals().keys():
                LOC.append(loc)
                del loc
            continue
    return LOC

def get_loc_entitys(tag_seq, char_seq):
    length = len(char_seq)
    location = []
    loc_set = []
    LOC = []
    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-LOC':
            loc = char
            location.append(loc)
        # if tag_seq[i] == 'B-LOC' and tag_seq[i - 1] == 'I-LOC':
        #     loc = char
        #     location.append(loc)
        if tag == 'I-LOC':
            loc = char
            location.append(loc)
        # location = list(set(location))
    # for j in location:
    #     if j not in loc_set:
    #         loc_set.append(j)
    t = reduce(lambda x, y: str(x) + str(y), location)
    LOC.append(t)
    return LOC

def get_ORG_entity(tag_seq, char_seq):
    length = len(char_seq)
    ORG = []
    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-ORG':
            if 'org' in locals().keys():
                ORG.append(org)
                del org
            org = char
            if i+1 == length:
                ORG.append(org)
        if tag == 'I-ORG':
            org += char
            if i+1 == length:
                ORG.append(org)
        if tag not in ['I-ORG', 'B-ORG']:
            if 'org' in locals().keys():
                ORG.append(org)
                del org
            continue
    ORG = list(set(ORG))  # 去重
    return ORG

def write_to_mysql():
    pass


def get_logger(filename):
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
    logging.getLogger().addHandler(handler)
    return logger
