# coding=gbk
import pandas as pd
import numpy as np
import streamlit as st

# 准备状态转移数据
def roll_rate(df,**status):
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

    dfx.loc[(0<dfx.标当前逾期天数_x) & (dfx.标当前逾期天数_x <= status["M1"]),"status1"]="M1"
    dfx.loc[(status["M1"]<dfx.标当前逾期天数_x) & (dfx.标当前逾期天数_x <= status["M2"]),"status1"]="M2"
    dfx.loc[(status["M2"]<dfx.标当前逾期天数_x) & (dfx.标当前逾期天数_x <= status["M3"]),"status1"]="M3"
    dfx.loc[(status["M3"]<dfx.标当前逾期天数_x) & (dfx.标当前逾期天数_x <= status["M4"]),"status1"]="M4"
    dfx.loc[(status["M4"]<dfx.标当前逾期天数_x) & (dfx.标当前逾期天数_x <= status["M5"]),"status1"]="M5"
    dfx.loc[status["M5"] <dfx.标当前逾期天数_x,"status1"]="M6"

    dfx.status1.value_counts()

    dfx.loc[(0<dfx.标当前逾期天数_x) & (dfx.标当前逾期天数_x <= status["M1"]),"status2"]="M1"
    dfx.loc[(status["M1"]<dfx.标当前逾期天数_y) & (dfx.标当前逾期天数_y <= status["M2"]),"status2"]="M2"
    dfx.loc[(status["M2"]<dfx.标当前逾期天数_y) & (dfx.标当前逾期天数_y <= status["M3"]),"status2"]="M3"
    dfx.loc[(status["M3"]<dfx.标当前逾期天数_y) & (dfx.标当前逾期天数_y <= status["M4"]),"status2"]="M4"
    dfx.loc[(status["M4"]<dfx.标当前逾期天数_y) & (dfx.标当前逾期天数_y <= status["M5"]),"status2"]="M5"
    dfx.loc[status["M5"] <dfx.标当前逾期天数_y,"status2"]="M6"

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

    roll_rate["better"] = better
    roll_rate["keep"] = keep
    roll_rate["worst"] = worst
    return(roll_rate)

@st.cache
def get_dat(file):
    return pd.read_csv(file)

# def color_coding(row):
#     return ['background-color:red'] * len(
#         row) if row.worst else ['background-color:green'] * len(row)

def highlight_cols(s):
    color = 'red'
    return 'background-color: %s' % color

if __name__ == "__main__":
    # st.sidebar.markdown("选择需要计算拜访记录相似性的方式")
    st.title("结果展示")
    st.sidebar.title("选项")
    status={"M1":5,
            "M2":10,
            "M3":15,
            "M4":20,
            "M5":30}
    # if st.sidebar.checkbox("上传文件", False):
    st.subheader("选项：上传文件:")
    try:
        uploaded_file = st.sidebar.file_uploader("Choose a file1")
        df = get_dat(uploaded_file)
        st.dataframe(df.head(10))
        # df = pd.read_csv("data/data_stdz.csv")

    except Exception as e:
        st.text(e)
        st.text("请输入正确的文件名")

    if st.sidebar.checkbox("计算滚动率", False):
        roll_rate = roll_rate(df,**status)
        st.write(':panda_face:',"逾期分级定义：{}".format(status))
        st.write("---------滚动率------")
        roll_rate.style.applymap(highlight_cols, subset=pd.IndexSlice[:, ['worst']])
        st.dataframe(roll_rate.style.applymap(highlight_cols, subset=pd.IndexSlice[:, ['worst']]))

    if st.sidebar.checkbox("账龄分析", False):
        pass
        # roll_rate = roll_rate(df,**status)
        # st.write(':panda_face:',"逾期分级定义：{}".format(status))
        # st.write("---------滚动率------")
        # st.dataframe(roll_rate.style.highlight_max(axis=0))


