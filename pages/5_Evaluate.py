import streamlit as st
import pandas as pd
import os
import shutil

modelMap = {
   'RF': 'Random Forest (500 trees)',
   'MLP': 'Multi-Layer Perceptron',
   'SVM': 'Support Vector Machine (RBF)',
   'KNN': 'K-Nearest Neighbors (10 neighbors)',
   'SGD': 'Logistic Regression',
   'DT': 'Decision Tree',
   'R': 'Ridge Regression',
   'GPC': 'Gaussian Process',
   'XGB': 'Extreme Gradient Boosting',
   'ADA': 'Adaptive Boosting',
   'GB': 'Gradient Boosting'
}


def classifier_long_names(key):
    return modelMap.get(key)

select = st.selectbox(
    'Model',
    modelMap,
    format_func = classifier_long_names)
st.write('Classifier: ', select)

gh_link = st.text_input('GitHub Link', placeholder='Ex. https://github.com/TheAlgorithms/Java')
st.write('GitHub Link: ', gh_link)

def remove_columns(df):
   #Uses for loop to skip any error in dropping columns that don't exist (Some files may not have columns with a subset of these columns)
   columns_to_remove = ['ID', 'Name', 'LongName', 'Parent', 'Component', 'Path', 'Line', 'Column', 'EndLine', 'EndColumn', 'WarningBlocker', 'WarningCritical', 'WarningInfo', 'WarningMajor', 'WarningMinor', 'Anti Pattern', 'Design Pattern']
    
   for col in columns_to_remove:
      try:
         df = df.drop(columns=[col], axis=1)
      except:
         pass
    
   return df
   
def get_evaluation_data(github_link):
    '''
    Input: GitHub link of the project to be evaluated
    Output: A pandas.Series that contains the extracted data of the GitHub project from SourceMeter
    '''
    
    token = st.secrets["GH_TOKEN"]
    flag = os.system("git clone https://{}:x-oauth-basic@github.com/{}".format(token, github_link))
    #print(flag)
    flag = os.system("SourceMeter-9.1.1/Java/SourceMeterJava " + "-projectName=test " + "-resultsDir=r -projectBaseDir={} ".format(github_link.split('/')[1]) + "-runAndroidHunter=false -runMetricHunter=false -runVulnerabilityHunter=false -runFaultHunter=false -runRTEHunter=false -runDCF=false -runMET=true -currentDate=none -runPMD=false -runFB=false")
    error_array = []
        
    if flag == 0:
        os.system('mv r/test/java/none/test-Class.csv r/test')
        os.system('mv r/test/java/none/test-File.csv r/test')
        os.system('mv r/test/java/none/test-Method.csv r/test')
        shutil.rmtree('r/test/java', ignore_errors=True)
    
    else:
        print('error')
        #error_array.append(i)
        
    try:
        granularities = ['Class', 'File', 'Method']
        test_sample_metric_names = []
        test_sample_array = []
        for g in granularities:
            df = pd.read_csv('r/test/test-{}.csv'.format(g), encoding='utf-8')
            df = remove_columns(df)
            test_sample_array.append(len(df.index))   #For No_C, No_F and No_M
            test_sample_metric_names.append('No_{}'.format(g[0]))
            for col in df.columns:
                test_sample_array.append(df[col].min())
                test_sample_array.append(df[col].median())
                test_sample_array.append(df[col].max())
                test_sample_array.append(df[col].sum())
                test_sample_array.append(df[col].std())

                test_sample_metric_names.append('{}min_{}'.format(g[0], col))
                test_sample_metric_names.append('{}med_{}'.format(g[0], col))
                test_sample_metric_names.append('{}max_{}'.format(g[0], col))
                test_sample_metric_names.append('{}sum_{}'.format(g[0], col))
                test_sample_metric_names.append('{}std_{}'.format(g[0], col))
    except FileNotFoundError:
        print('File not found')
        
    return pd.Series(data=test_sample_array, index=test_sample_metric_names)

if st.button('Evaluate'):
    st.write(get_evaluation_data(gh_link))
    print(get_evaluation_data(gh_link))
    st.write('Reusability is LOW')
    st.write('Reusability is HIGH')
else:
    st.write('Goodbye')




ind = [1,2,3,4,5,6,7]
outputRecommendedTable = pd.DataFrame({
    "Metric": ["Number of Files", "CBO", "NL", "PUA", "CBOI", "NII", "CBO"],
    "Granularity": ["project", "class", "class", "file", "class", "class", "class"],
    "Aggregation": ["-", "std", "sum", "sum", "std", "max", "max"],
    "Recommended": ["< 250", "2 - 7", "< 450", "> 100", "2 - 11", "< 200", "20 - 80"]}, index=ind)
    
st.table(outputRecommendedTable)

