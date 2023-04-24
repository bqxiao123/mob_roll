# coding=gbk
import pandas as pd
import numpy as np
import streamlit as st

# ׼��״̬ת������
def roll_rate(df,**status):
    dates = np.sort(df.dt.unique())
    np.sort(dates)

    dfx=pd.DataFrame()
    for i in range(len(dates)-1):
        # print(i)
        dfx0 = df[df.dt == dates[i]][["ListingId","�굱ǰ��������","dt"]].merge(df[df.dt == dates[i+1]][["ListingId","�굱ǰ��������","dt"]],on="ListingId")
        # print(dfx0.shape)
        dfx = pd.concat([dfx,dfx0],axis=0)

    # ��������״̬���ɸ���ʵ����Ҫ�ı�����

    dfx["status1"]="M0"
    dfx["status2"]="M0"

    dfx.loc[(0<dfx.�굱ǰ��������_x) & (dfx.�굱ǰ��������_x <= status["M1"]),"status1"]="M1"
    dfx.loc[(status["M1"]<dfx.�굱ǰ��������_x) & (dfx.�굱ǰ��������_x <= status["M2"]),"status1"]="M2"
    dfx.loc[(status["M2"]<dfx.�굱ǰ��������_x) & (dfx.�굱ǰ��������_x <= status["M3"]),"status1"]="M3"
    dfx.loc[(status["M3"]<dfx.�굱ǰ��������_x) & (dfx.�굱ǰ��������_x <= status["M4"]),"status1"]="M4"
    dfx.loc[(status["M4"]<dfx.�굱ǰ��������_x) & (dfx.�굱ǰ��������_x <= status["M5"]),"status1"]="M5"
    dfx.loc[status["M5"] <dfx.�굱ǰ��������_x,"status1"]="M6"

    dfx.status1.value_counts()

    dfx.loc[(0<dfx.�굱ǰ��������_x) & (dfx.�굱ǰ��������_x <= status["M1"]),"status2"]="M1"
    dfx.loc[(status["M1"]<dfx.�굱ǰ��������_y) & (dfx.�굱ǰ��������_y <= status["M2"]),"status2"]="M2"
    dfx.loc[(status["M2"]<dfx.�굱ǰ��������_y) & (dfx.�굱ǰ��������_y <= status["M3"]),"status2"]="M3"
    dfx.loc[(status["M3"]<dfx.�굱ǰ��������_y) & (dfx.�굱ǰ��������_y <= status["M4"]),"status2"]="M4"
    dfx.loc[(status["M4"]<dfx.�굱ǰ��������_y) & (dfx.�굱ǰ��������_y <= status["M5"]),"status2"]="M5"
    dfx.loc[status["M5"] <dfx.�굱ǰ��������_y,"status2"]="M6"

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
    # st.sidebar.markdown("ѡ����Ҫ����ݷü�¼�����Եķ�ʽ")
    st.title("���չʾ")
    st.sidebar.title("ѡ��")
    status={"M1":5,
            "M2":10,
            "M3":15,
            "M4":20,
            "M5":30}
    # if st.sidebar.checkbox("�ϴ��ļ�", False):
    st.subheader("ѡ��ϴ��ļ�:")
    try:
        uploaded_file = st.sidebar.file_uploader("Choose a file1")
        df = get_dat(uploaded_file)
        st.dataframe(df.head(10))
        # df = pd.read_csv("data/data_stdz.csv")

    except Exception as e:
        st.text(e)
        st.text("��������ȷ���ļ���")

    if st.sidebar.checkbox("���������", False):
        roll_rate = roll_rate(df,**status)
        st.write(':panda_face:',"���ڷּ����壺{}".format(status))
        st.write("---------������------")
        roll_rate.style.applymap(highlight_cols, subset=pd.IndexSlice[:, ['worst']])
        st.dataframe(roll_rate.style.applymap(highlight_cols, subset=pd.IndexSlice[:, ['worst']]))

    if st.sidebar.checkbox("�������", False):
        pass
        # roll_rate = roll_rate(df,**status)
        # st.write(':panda_face:',"���ڷּ����壺{}".format(status))
        # st.write("---------������------")
        # st.dataframe(roll_rate.style.highlight_max(axis=0))


