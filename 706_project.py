import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)


st.write("# BMI 706 Project ")
st.write("## Team - LuckyBabies (Fuchen Li, Xi Wang, Zihan Wang)")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    This is a project of discovering Parkinson's Disease from finger movement
    and typing data.&nbsp;
    \
     **👈 Choose a demo from the sidebar** to see some fun visualization examples!

    ### Dataset Description

    Our dataset is one of the open-source databases on PhysioNet.org. Specifically, 
    the dataset we choose is about the detection of early Parkinson's Disease using 
    finger movement patterns while typing. 
    The typing behavior is recorded by a keystroke recording app called [“Tappy”](https://physionet.org/content/tappy/1.0.0/). 

    ### Demographic Variables
    - Numerical:
        * Birth Year: Year of birth
    - Categorical: 
        * Gender: Male/Female
        * Parkinsons: Whether they have Parkinson's Disease [True/False]
        * Tremors: Whether they have tremors [True/False]
        * Diagnosis Year: If they have Parkinson's, when was it first diagnosed
        * Whether there is sidedness of movement [Left/Right/None] (self-reported)
        * UPDRS: The UPDRS score (if known) [1 to 5]
        * Impact: The Parkinson's disease severity or impact on their daily life [Mild/Medium/Severe] (self-reported)
        * Levadopa: Whether they are using Sinemet and the like [Yes/No]
        * DA: Whether they are using a dopamine agonist [Yes/No]
        * MAOB: Whether they are using an MAO-B inhibitor [Yes/No]
        * Other: Whether they are taking another Parkinson's medication [Yes/No]

    ### Reference 
    Goldberger, A., et al. "PhysioBank, PhysioToolkit, and PhysioNet: Components of 
    a new research resource for complex physiologic signals. Circulation [Online]. 101 (23), pp. e215–e220." (2000).

"""
)