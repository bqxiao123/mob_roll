# coding=gbk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

import warnings
warnings.filterwarnings("ignore")
# �������ݣ��޸�����Ϊ��׼����
# @st.cache
def get_dat(file,cols):
    # file = "data/data_stdz.csv"
    df = pd.read_csv(file)
    # df = df.rename(columns={"�굱ǰ��������":"��ǰ��������","���ɹ�����":"ot","dt":"dt"})
    df = df.rename(columns=cols)
    df["om"] = df["ot"].astype("str").str.slice(0, 6)
    return df

##
# ׼��״̬ת������
def roll_rate(df,**status):
    dates = np.sort(df.dt.unique())
    np.sort(dates)

    dfx=pd.DataFrame()
    for i in range(len(dates)-1):
        # print(i)
        dfx0 = df[df.dt == dates[i]][["ListingId","��ǰ��������","dt"]].merge(df[df.dt == dates[i+1]][["ListingId","��ǰ��������","dt"]],on="ListingId")
        # print(dfx0.shape)
        dfx = pd.concat([dfx,dfx0],axis=0)

    # ��������״̬���ɸ���ʵ����Ҫ�ı�����

    dfx["status1"]="M0"
    dfx["status2"]="M0"

    dfx.loc[(0<dfx.��ǰ��������_x) & (dfx.��ǰ��������_x <= status["M1"]),"status1"]="M1"
    dfx.loc[(status["M1"]<dfx.��ǰ��������_x) & (dfx.��ǰ��������_x <= status["M2"]),"status1"]="M2"
    dfx.loc[(status["M2"]<dfx.��ǰ��������_x) & (dfx.��ǰ��������_x <= status["M3"]),"status1"]="M3"
    dfx.loc[(status["M3"]<dfx.��ǰ��������_x) & (dfx.��ǰ��������_x <= status["M4"]),"status1"]="M4"
    dfx.loc[(status["M4"]<dfx.��ǰ��������_x) & (dfx.��ǰ��������_x <= status["M5"]),"status1"]="M5"
    dfx.loc[status["M5"] <dfx.��ǰ��������_x,"status1"]="M6"

    dfx.status1.value_counts()

    dfx.loc[(0<dfx.��ǰ��������_x) & (dfx.��ǰ��������_x <= status["M1"]),"status2"]="M1"
    dfx.loc[(status["M1"]<dfx.��ǰ��������_y) & (dfx.��ǰ��������_y <= status["M2"]),"status2"]="M2"
    dfx.loc[(status["M2"]<dfx.��ǰ��������_y) & (dfx.��ǰ��������_y <= status["M3"]),"status2"]="M3"
    dfx.loc[(status["M3"]<dfx.��ǰ��������_y) & (dfx.��ǰ��������_y <= status["M4"]),"status2"]="M4"
    dfx.loc[(status["M4"]<dfx.��ǰ��������_y) & (dfx.��ǰ��������_y <= status["M5"]),"status2"]="M5"
    dfx.loc[status["M5"] <dfx.��ǰ��������_y,"status2"]="M6"

    # ���������
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
    df.loc[df.��ǰ�������� >= status[dg], "status"] = 1
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
    # st.sidebar.markdown("ѡ����Ҫ����ݷü�¼�����Եķ�ʽ")
    st.title("���չʾ")
    st.sidebar.title("ѡ��")
    st.subheader("��������")
    uploaded_file = st.sidebar.file_uploader("STEP1���ϴ��ļ�")
    # status={"M1":5,
    #         "M2":10,
    #         "M3":15,
    #         "M4":20,
    #         "M5":30}

    # print(status)
    if uploaded_file is not None:
        st.text("Load {} done..........".format(uploaded_file))
        cols = eval(st.sidebar.text_input('STEP2�����õ�ǰ�����������������ot��ʱ����Ƭdt��Ӧ���ļ�����:',
                                          '{"�굱ǰ��������":"��ǰ��������","���ɹ�����":"ot","dt":"dt"}'))
        st.text("��������{} ==> {}".format(list(cols.keys())[0], list(cols.values())[0]), )
        st.text("��������{} ==> {}".format(list(cols.keys())[1], list(cols.values())[1]))
        st.text("��������{} ==> {}".format(list(cols.keys())[2], list(cols.values())[2]))
        status = eval(st.sidebar.text_input('STEP3���������ڷ����׼:',
                                            '{"M1":5,"M2":10,"M3":15,"M4":20,"M5":30}'))
        try:
            # uploaded_file = st.sidebar.file_uploader("Choose a file1")
            df = get_dat(uploaded_file,cols)
            st.dataframe(df.head(10))
            # df = pd.read_csv("data/data_stdz.csv")

        except Exception as e:
            st.text(e)
            st.text("��������ȷ���ļ���")

        if st.sidebar.checkbox("STEP4: ���������", False):
            st.subheader("���ڹ�����ת�ƾ���")
            roll_rate = roll_rate(df,**status)
            st.write(':panda_face:',"���ڷּ����壺{}".format(status))
            roll_rate.style.applymap(highlight_cols, subset=pd.IndexSlice[:, ['worst']])
            st.dataframe(roll_rate.style.applymap(highlight_cols, subset=pd.IndexSlice[:, ['worst']]))

        if st.sidebar.checkbox("STEP5: �������", False):
            st.subheader("���������Vintage��")
            dg = st.sidebar.text_input("���ڹ����ʷ������û��ͻ����ڱ�׼��Ĭ��ֵΪ������worst>60%��Ӧ�����ڵȼ�",roll_rate.idxmax().worst)
            st.text("ѡ�۵Ļ��ͻ���׼Ϊ������������{}�졣".format(status[dg]))
            print(dg,type(dg))
            fig = plot_vintage(df,dg)
            st.write(fig)


