import streamlit as st
import pandas as pd
from collections import deque

st.markdown("# Ranking")
st.sidebar.header("Ranking")
st.write(
    """The listed table is ranked Maven repositories within the 
    studied dataset grouped by selected tag ordered based on predicted 
    regression on the reuse value. Tags represent the scope domain/purpose 
    of a repository. By default, the table displays all the studied repositories."""
)

st.markdown(
    """
    ### **Example:** 
    
    A developer plans to identify the most reusable Java logging framework.
    
    - From the dropdown, search 'logging' and hit 'Enter'/click to select 'logging' to rank the list of 'logging' 
    related repositories studied.
    """
)


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
    'Selected tag: ',
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