# coding=gbk
import pandas as pd
import numpy as np
import streamlit as st

# 准备状态转移数据
def roll_rate(df):
    dates = np.sort(df.dt.unique())
    np.sort(dates)

    dfx=pd.DataFrame()
    for i in range(len(dates)-1):
        # print(i)
        dfx0 = df[df.dt == dates[i]][["ListingId","标当前逾期天数","dt"]].merge(df[df.dt == dates[i+1]][["ListingId","标当前逾期天数","dt"]],on="ListingId")
        # print(dfx0.shape)
        dfx = pd.concat([dfx,dfx0],axis=0)

    # 定义逾期状态、可根据实际需要改变周期

    dfx["status1"]="M0"
    dfx["status2"]="M0"

    dfx.loc[(0<dfx.标当前逾期天数_x) & (dfx.标当前逾期天数_x <= 30),"status1"]="M1"
    dfx.loc[(30<dfx.标当前逾期天数_x) & (dfx.标当前逾期天数_x <= 60),"status1"]="M2"
    dfx.loc[(60<dfx.标当前逾期天数_x) & (dfx.标当前逾期天数_x <= 90),"status1"]="M3"
    dfx.loc[(90<dfx.标当前逾期天数_x) & (dfx.标当前逾期天数_x <= 120),"status1"]="M4"
    dfx.loc[(120<dfx.标当前逾期天数_x) & (dfx.标当前逾期天数_x <= 150),"status1"]="M5"
    dfx.loc[150<dfx.标当前逾期天数_x,"status1"]="M6"

    dfx.status1.value_counts()

    dfx.loc[(0<dfx.标当前逾期天数_y) & (dfx.标当前逾期天数_y <= 30),"status2"]="M1"
    dfx.loc[(30<dfx.标当前逾期天数_y) & (dfx.标当前逾期天数_y <= 60),"status2"]="M2"
    dfx.loc[(60<dfx.标当前逾期天数_y) & (dfx.标当前逾期天数_y <= 90),"status2"]="M3"
    dfx.loc[(90<dfx.标当前逾期天数_y) & (dfx.标当前逾期天数_y <= 120),"status2"]="M4"
    dfx.loc[(120<dfx.标当前逾期天数_y) & (dfx.标当前逾期天数_y <= 150),"status2"]="M5"
    dfx.loc[150<dfx.标当前逾期天数_y,"status2"]="M6"

    # 计算滚动率
    roll_num = dfx.groupby(["status1","status2"]).ListingId.count().unstack().fillna(0)
    roll_rate = (roll_num.T/roll_num.T.sum()).T
    worst=[]
    for i in range(roll_rate.shape[0]):
        worst.append(sum(roll_rate.iloc[i,i+1:]))

    better=[]
    for i in range(roll_rate.shape[0]):
        better.append(sum(roll_rate.iloc[i,:i]))

    keep=[]
    for i in range(roll_rate.shape[0]):
        keep.append(roll_rate.iloc[i,i])

    roll_rate["worst"] = worst
    roll_rate["better"] = better
    roll_rate["keep"] = keep
    return(roll_rate)

if __name__ == "__main__":
    # st.sidebar.markdown("选择需要计算拜访记录相似性的方式")
    st.title("结果展示")
    st.sidebar.title("选项")
    if st.sidebar.checkbox("上传文件", False):
        st.subheader("选项：上传文件:")
        try:
            uploaded_file = st.sidebar.file_uploader("Choose a file1")
            df = pd.read_csv(uploaded_file)
            st.write(df)
            # df = pd.read_csv("data/data_stdz.csv")
            roll_rate = roll_rate(df)
            st.dataframe(roll_rate)
        except Exception as e:
            st.text(e)