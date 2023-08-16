import streamlit as st
import pandas as pd
from collections import deque

@st.cache_data
def load_data():
    data = pd.read_csv("Data/forWebsite.csv", sep=",", encoding='utf-8')
    return data

rankingData = load_data()
tagsForSelection = []
for t in rankingData.iloc[:, 4:-2].columns:
    tagsForSelection.append(t)
tagsForSelection = deque(tagsForSelection)
tagsForSelection.appendleft('All')
tagsForSelection = list(tagsForSelection)
select = st.selectbox(
    'Tag',
    tagsForSelection)

if select != 'All':
    sortedRanking = rankingData[rankingData[select] == 1].sort_values(by=['predicted'], ascending=False).reset_index()
else:
    sortedRanking = rankingData.sort_values(by=['predicted'], ascending=False).reset_index()

def shorten_name(string):
    return '-'.join(string.split('-')[1:])

sortedRanking['Project'] = sortedRanking['library_name'].apply(shorten_name)
sortedRanking = sortedRanking.rename({'roundedPredicted': 'Reuse'}, axis='columns')
st.table(sortedRanking[['Project', 'Reuse']])



    #"Value": [],
    #"Status": []