# coding=gbk

import pandas as pd
import numpy as np

# 过滤不规范数据
df = pd.read_csv("data/LCIS.csv")
df = df[df.recorddate.str.len() >= 9]
df = df.dropna(subset=["recorddate"])

# 时间字段规范化处理
def fill_date(x):
    inx = [j for j,i in enumerate(x) if i == "/"]
    return x[0:inx[0]]+x[inx[0]+1:inx[1]].rjust(2,"0")+x[inx[1]+1:].rjust(2,"0")

df["dt"] = df.recorddate.apply(fill_date)
df.to_csv("data/data_stdz.csv")

