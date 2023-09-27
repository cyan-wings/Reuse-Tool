import streamlit as st
import pandas as pd
import os
import shutil
import dill 
import numpy as np

modelMap = {
   'RF': 'Random Forest (500 trees)',
   'MLP': 'Multi-Layer Perceptron',
   'SVM': 'Support Vector Machine (RBF)',
   'KNN': 'K-Nearest Neighbors (10 neighbors)',
   'LR': 'Logistic Regression',
   'DT': 'Decision Tree',
   'R': 'Ridge Regression',
   'GPC': 'Gaussian Process',
   'XGB': 'Extreme Gradient Boosting',
   'ADA': 'Adaptive Boosting',
   'GB': 'Gradient Boosting'
}


def classifier_long_names(key):
    return modelMap.get(key)

st.markdown("# Reuse Assessment Tool")
st.sidebar.header("Reuse Assessment Tool")
st.write(
    """This tool evaluates the reuse of a Java GitHub project given its handle."""
)

st.markdown(
    """
    ### **Usage example:** 
    
    A developer wants to assess a Java project.
    
    1. Create and upload the project onto GitHub.
    2. Select the ML classifier to use to predict the reuse of the project.
    3. Input the GitHub handle of the uploaded project onto GitHub.
    (e.g., the handle of https://github.com/skeeto/sample-java-project is 
    "skeeto/sample-java-project".)
    4. Values of important metrics are displayed in the output providing value recommendations 
    to potentially improve the reuse of the project.
    """
)

classifier = st.selectbox(
    'Selected classifier: ',
    modelMap,
    format_func = classifier_long_names)
#st.write('Classifier: ', classifier)

gh_link = st.text_input('GitHub Handle: ', placeholder='example: mockito/mockito')

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
    with st.spinner("Cloning GitHub project..."):
        flag = os.system("git clone https://{}:x-oauth-basic@github.com/{}".format(token, github_link))
    
    #if flag==32768:
        #shutil.rmtree(github_link.split('/')[1])
        #return render_template('index.html', modelData=classifier_dict, pre_text='Input a valid GitHub Link')

    with st.spinner("Extracting and Analysing features..."):
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
        
    #if sample_array.No_C == 0:
        #shutil.rmtree(gitLink.split('/')[1])
        #return render_template('index.html', modelData=classifier_dict, pre_text='Input a valid Java Project') 
    return pd.Series(data=test_sample_array, index=test_sample_metric_names).drop(['Cmin_NOC', 'Cmed_NOC', 'Cmin_NOD', 'Cmed_NOD', 'Cmin_NLPA', 'Cmin_NLS', 'Cmin_NPA', 'Cmin_NS', 'Cmin_TNLPA', 'Cmin_TNLS', 'Cmin_TNPA', 'Cmin_TNS', 'Fmin_CLOC', 'Fmed_CLOC', 'Fmax_CLOC', 'Fsum_CLOC', 'Fstd_CLOC', 'Mmin_NL', 'Mmin_NLE', 'Mmin_NII', 'Mmin_NOI', 'Mmin_CD', 'Mmin_CLOC', 'Mmin_DLOC', 'Mmin_TCD', 'Mmin_TCLOC', 'Cmin_CLOC', 'Cmin_DLOC', 'Cmin_TCLOC', 'Cmed_NOP', 'Cstd_NOP', 'Cmed_NLG', 'Cmed_TNLG', 'Mmin_HPL', 'Mmin_HPV', 'Mmin_HTRP', 'Mmin_MI'])



def generateTable(sample_array):
    status_array = []  # 1 = check, 2 = up, 3 = down
    importance_features = [('Fsum_PUA', 450, 'L'), ('No_F', 250, 'L'), ('Cmax_NII', 80, 'L'), ('Csum_NL', 450, 'L'), ('Cstd_CBO', 2, 7),  ('Cmax_LCOM5', 10, 'H'), ('Cmax_CBO', 20, 80)]
    actual_values = []
    for f in importance_features:
        actual_values.append(sample_array[f[0]])
        if f[2] == 'L':
            if sample_array[f[0]] < f[1]:
                status_array.append("✅")
            else:
                status_array.append("🔽")
        elif f[2] == 'H':
            if sample_array[f[0]] > f[1]:
                status_array.append("✅")
            else:
                status_array.append("🔼")
        else:
            if sample_array[f[0]] >= f[1] and sample_array[f[0]] <= f[2]:
                status_array.append("✅")
            elif sample_array[f[0]] < f[1]:
                status_array.append("🔼")
            elif sample_array[f[0]] > f[2]:
                status_array.append("🔽")

    outputRecommendedDF = pd.DataFrame(
        {
            "Index": list(range(1,8)),
            "Metric": [
                "PUA - File (sum)", "Number of files", 
                "NII - Class (max)", "NL - Class (sum)",
                "CBO - Class (std)", "LCOM5 - Class (max)", 
                "CBO - Class (max)"
            ],
            "Recommended": [
                "> 40", "< 250",
                "< 80", "< 450",
                "2 - 7", "> 10",
                "20 - 80"
            ],
            "Value": actual_values,
            "Status": status_array
        }
    )
        
    st.dataframe(
        outputRecommendedDF,
        hide_index = True,
    )


if st.button('Evaluate'):
    sample_array = get_evaluation_data(gh_link)
    model = dill.load(open("Saved_Models/{}.pkl".format(classifier),"rb"))
    if model.predict([sample_array])[0] == 1:
        st.write('HIGH REUSE')
    else:
        st.write('LOW REUSE')
    generateTable(sample_array)

