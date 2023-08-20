import streamlit as st

def intro():

    st.write("# Machine Learning-Assisted Software Reuse Prediction and Analysis")
    st.sidebar.header("About")

    st.markdown(
        """
        This tool supplements RQ3 of the PhD thesis titled above.

        ### Author
        
        Matthew Yeow Yit Hang

        ### Supervisor

        - Chong Chun Yong
        - Lim Mei Kuan

        ### Features

        - Predict reuse of an existing Java GitHub project.
        - Provide suggestions on how to improve reuse.
        - Provide rankings of analysed Maven repositories based on tags.


    """
    )

intro()