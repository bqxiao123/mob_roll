# coding=gbk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

import warnings
warnings.filterwarnings("ignore")
# 导入数据，修改列名为标准列名
# @st.cache
def get_dat(file,cols):
    # file = "data/data_stdz.csv"
    df = pd.read_csv(file)
    # df = df.rename(columns={"标当前逾期天数":"当前逾期天数","借款成功日期":"ot","dt":"dt"})
    df = df.rename(columns=cols)
    df["om"] = df["ot"].astype("str").str.slice(0, 6)
    return df

##
# 准备状态转移数据
def roll_rate(df,**status):
    dates = np.sort(df.dt.unique())
    np.sort(dates)

    dfx=pd.DataFrame()
    for i in range(len(dates)-1):
        # print(i)
        dfx0 = df[df.dt == dates[i]][["ListingId","当前逾期天数","dt"]].merge(df[df.dt == dates[i+1]][["ListingId","当前逾期天数","dt"]],on="ListingId")
        # print(dfx0.shape)
        dfx = pd.concat([dfx,dfx0],axis=0)

    # 定义逾期状态、可根据实际需要改变周期

    dfx["status1"]="M0"
    dfx["status2"]="M0"

    dfx.loc[(0<dfx.当前逾期天数_x) & (dfx.当前逾期天数_x <= status["M1"]),"status1"]="M1"
    dfx.loc[(status["M1"]<dfx.当前逾期天数_x) & (dfx.当前逾期天数_x <= status["M2"]),"status1"]="M2"
    dfx.loc[(status["M2"]<dfx.当前逾期天数_x) & (dfx.当前逾期天数_x <= status["M3"]),"status1"]="M3"
    dfx.loc[(status["M3"]<dfx.当前逾期天数_x) & (dfx.当前逾期天数_x <= status["M4"]),"status1"]="M4"
    dfx.loc[(status["M4"]<dfx.当前逾期天数_x) & (dfx.当前逾期天数_x <= status["M5"]),"status1"]="M5"
    dfx.loc[status["M5"] <dfx.当前逾期天数_x,"status1"]="M6"

    dfx.status1.value_counts()

    dfx.loc[(0<dfx.当前逾期天数_x) & (dfx.当前逾期天数_x <= status["M1"]),"status2"]="M1"
    dfx.loc[(status["M1"]<dfx.当前逾期天数_y) & (dfx.当前逾期天数_y <= status["M2"]),"status2"]="M2"
    dfx.loc[(status["M2"]<dfx.当前逾期天数_y) & (dfx.当前逾期天数_y <= status["M3"]),"status2"]="M3"
    dfx.loc[(status["M3"]<dfx.当前逾期天数_y) & (dfx.当前逾期天数_y <= status["M4"]),"status2"]="M4"
    dfx.loc[(status["M4"]<dfx.当前逾期天数_y) & (dfx.当前逾期天数_y <= status["M5"]),"status2"]="M5"
    dfx.loc[status["M5"] <dfx.当前逾期天数_y,"status2"]="M6"

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

# def color_coding(row):
#     return ['background-color:red'] * len(
#         row) if row.worst else ['background-color:green'] * len(row)

def highlight_cols(s):
    color = 'red'
    return 'background-color: %s' % color

def plot_vintage(df,dg):
    df["month"] = 12 * (
                df.dt.astype("str").str.slice(0, 4).astype("int") - df.ot.astype("str").str.slice(0, 4).astype("int")) \
                  + (df.dt.astype("str").str.slice(4, 6).astype("int") - df.ot.astype("str").str.slice(4, 6).astype("int"))
    df["status"] = 0
    df.loc[df.当前逾期天数 >= status[dg], "status"] = 1
    fig, ax = plt.subplots(figsize=(12, 8))
    dfz = df.groupby(["om", "month"]). \
        apply(lambda x: x.status.sum() / x.status.count()). \
        reset_index().set_index("om")
    for x in list(set(dfz.index)):
        ax.plot(dfz.loc[x, "month"], dfz.loc[x, 0],label=x)
    ax.set_xlabel('mob')  # Add an x-label to the axes.
    ax.set_ylabel('bad_rate')  # Add a y-label to the axes.
    ax.set_title("Vintage")  # Add a title to the axes.
    ax.legend()  # Add a legend.
    return fig

if __name__ == "__main__":
    # st.sidebar.markdown("选择需要计算拜访记录相似性的方式")
    st.title("结果展示")
    st.sidebar.title("选项")
    st.subheader("导入数据")
    uploaded_file = st.sidebar.file_uploader("STEP1：上传文件")
    # status={"M1":5,
    #         "M2":10,
    #         "M3":15,
    #         "M4":20,
    #         "M5":30}

    # print(status)
    if uploaded_file is not None:
        st.text("Load {} done..........".format(uploaded_file))
        cols = eval(st.sidebar.text_input('STEP2：设置当前逾期天数、借款日期ot，时间切片dt对应的文件列名:',
                                          '{"标当前逾期天数":"当前逾期天数","借款成功日期":"ot","dt":"dt"}'))
        st.text("重命名：{} ==> {}".format(list(cols.keys())[0], list(cols.values())[0]), )
        st.text("重命名：{} ==> {}".format(list(cols.keys())[1], list(cols.values())[1]))
        st.text("重命名：{} ==> {}".format(list(cols.keys())[2], list(cols.values())[2]))
        status = eval(st.sidebar.text_input('STEP3：设置逾期分类标准:',
                                            '{"M1":5,"M2":10,"M3":15,"M4":20,"M5":30}'))
        try:
            # uploaded_file = st.sidebar.file_uploader("Choose a file1")
            df = get_dat(uploaded_file,cols)
            st.dataframe(df.head(10))
            # df = pd.read_csv("data/data_stdz.csv")

        except Exception as e:
            st.text(e)
            st.text("请输入正确的文件名")

        if st.sidebar.checkbox("STEP4: 计算滚动率", False):
            st.subheader("逾期滚动率转移矩阵")
            roll_rate = roll_rate(df,**status)
            st.write(':panda_face:',"逾期分级定义：{}".format(status))
            roll_rate.style.applymap(highlight_cols, subset=pd.IndexSlice[:, ['worst']])
            st.dataframe(roll_rate.style.applymap(highlight_cols, subset=pd.IndexSlice[:, ['worst']]))

        if st.sidebar.checkbox("STEP5: 账龄分析", False):
            st.subheader("账龄分析（Vintage）")
            dg = st.sidebar.text_input("基于滚动率分析设置坏客户逾期标准，默认值为滚动率worst>60%对应的逾期等级",roll_rate.idxmax().worst)
            st.text("选折的坏客户标准为逾期天数大于{}天。".format(status[dg]))
            print(dg,type(dg))
            fig = plot_vintage(df,dg)
            st.write(fig)


