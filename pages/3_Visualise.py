import streamlit as st
import pandas as pd
import plotly.figure_factory as ff

st.markdown("# Visualise Dataset")
st.sidebar.header("Visualise Dataset")
st.write(
    """Visualises the distribution of LOW and HIGH reuse repositories of the dataset
    based on the selected software metric feature with optional repository tag filter."""
)

st.markdown(
    """
    ### **Example:** 
    
    A researcher wants to identify the distribution of the studied dataset based on specific 
    feature.
    
    1. Select the granularity level of the metric.
    2. Select the metric. Refer to TODO
    3. Select the aggregation type of the metric selected in Step 2.
    4. Check 'Filter tag' if user wants the distribution to filter the distibution based on 
       specific tag and select the specific tag from the dropdown.
    5. Hit "Visualise" to generate the graph distribution.
    """
)

@st.cache_data
def load_data():
    data = pd.read_csv("Data/DatasetWithBinaryTagsandMavenReuseBinaryTags.csv", sep=",", encoding='utf-8')
    return data

data = load_data()
features = data.columns[1:-96]

selected_granularity = st.selectbox(
    'Select granularity: ',
    ['Repository', 'File', 'Class', 'Method'])

metrics_set = []
if selected_granularity[0] == 'R':
    metrics_set += ["Number of Files", "Number of Classes", "Number of Methods"]
else:
    for f in features:
        if f[0] == selected_granularity[0]:
            metrics_set.append(f.split('_')[-1])
    metrics_set = list(set(metrics_set))

selected_metric = st.selectbox(
    'Select metric: ',
    metrics_set)

selected_aggregation = st.selectbox(
    'Select aggregation: ',
    ['sum', 'std', 'max', 'med', 'min'])

if selected_granularity[0] == 'R':
    selected_feature = 'No_' + selected_metric.split(' ')[-1][0]
else:
    selected_feature = selected_granularity[0] + selected_aggregation + '_' + selected_metric

st.write("Feature code: " + selected_feature)

tag_check = st.checkbox('Filter tag')

if tag_check:
    selected_tag = st.selectbox(
        'Selected tag: ',
        data.columns[-93:])
    
if st.button('Visualise'):

    if tag_check:
        x1 = data[(data['reusability'] <= 21) & (data[selected_tag] == 1)][selected_feature]
        x2 = data[(data['reusability'] > 21) & (data[selected_tag] == 1)][selected_feature]
    else:
        x1 = data[data['reusability'] <= 21][selected_feature]
        x2 = data[data['reusability'] > 21][selected_feature]


    # Group data together
    hist_data = [x1, x2]

    group_labels = ['LOW', 'HIGH']

    # Create distplot with custom bin_size
    fig = ff.create_distplot(
            hist_data, group_labels, bin_size=[.1, .25, .5])

    # Plot!
    st.plotly_chart(fig, use_container_width=True)