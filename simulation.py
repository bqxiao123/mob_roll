# coding=gbk
import pandas as pd
import numpy as np
import streamlit as st

# ׼��״̬ת������
def roll_rate(df):
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

    dfx.loc[(0<dfx.�굱ǰ��������_x) & (dfx.�굱ǰ��������_x <= 30),"status1"]="M1"
    dfx.loc[(30<dfx.�굱ǰ��������_x) & (dfx.�굱ǰ��������_x <= 60),"status1"]="M2"
    dfx.loc[(60<dfx.�굱ǰ��������_x) & (dfx.�굱ǰ��������_x <= 90),"status1"]="M3"
    dfx.loc[(90<dfx.�굱ǰ��������_x) & (dfx.�굱ǰ��������_x <= 120),"status1"]="M4"
    dfx.loc[(120<dfx.�굱ǰ��������_x) & (dfx.�굱ǰ��������_x <= 150),"status1"]="M5"
    dfx.loc[150<dfx.�굱ǰ��������_x,"status1"]="M6"

    dfx.status1.value_counts()

    dfx.loc[(0<dfx.�굱ǰ��������_y) & (dfx.�굱ǰ��������_y <= 30),"status2"]="M1"
    dfx.loc[(30<dfx.�굱ǰ��������_y) & (dfx.�굱ǰ��������_y <= 60),"status2"]="M2"
    dfx.loc[(60<dfx.�굱ǰ��������_y) & (dfx.�굱ǰ��������_y <= 90),"status2"]="M3"
    dfx.loc[(90<dfx.�굱ǰ��������_y) & (dfx.�굱ǰ��������_y <= 120),"status2"]="M4"
    dfx.loc[(120<dfx.�굱ǰ��������_y) & (dfx.�굱ǰ��������_y <= 150),"status2"]="M5"
    dfx.loc[150<dfx.�굱ǰ��������_y,"status2"]="M6"

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

    roll_rate["worst"] = worst
    roll_rate["better"] = better
    roll_rate["keep"] = keep
    return(roll_rate)

if __name__ == "__main__":
    # st.sidebar.markdown("ѡ����Ҫ����ݷü�¼�����Եķ�ʽ")
    st.title("���չʾ")
    st.sidebar.title("ѡ��")
    if st.sidebar.checkbox("�ϴ��ļ�", False):
        st.subheader("ѡ��ϴ��ļ�:")
        try:
            uploaded_file = st.sidebar.file_uploader("Choose a file1")
            df = pd.read_csv(uploaded_file)
            st.write(df)
            # df = pd.read_csv("data/data_stdz.csv")
            roll_rate = roll_rate(df)
            st.dataframe(roll_rate)
        except Exception as e:
            st.text(e)