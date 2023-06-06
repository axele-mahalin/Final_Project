import streamlit as st
import pandas as pd
import numpy as np
import datetime
from PIL import Image
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns
import requests
import json
import pandas as pd
import os
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.neighbors import NearestNeighbors
import string
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split

###### To run streamlit page type in terminal 
######## streamlit run art_exhibitions.py

####### Title 
st.title('Art exhibition')
st.header('Welcome to my art exhibitions recommender in Paris!')

#import file about the french museums infos

Paris_exhibitions=pd.read_csv('Cleaned_data/Paris_exhibitions.csv', sep=',', encoding='UTF8')
pd.set_option('display.max_columns', 20)

##### Data input - date of the exhibition
d = st.date_input('When do you want to go for an exhibition?', datetime.date(2023,6,9))

##### Data input - genre of the exhibition

genres = Paris_exhibitions['genre'].unique()
genre = st.selectbox("What kind of exhibition are you interested in?", genres)

##### Data input - audience of the exhibition

audience = Paris_exhibitions['audience'].sort_values(ascending=False).unique()
audience = st.selectbox("For who?", audience)

##### Output user's selection

st.write('You want to go to an exhibition on: ', d)
st.write("**Genre:** ", genre)
st.write('**Audience:** ', audience)

##### Exhibition suggestion

exhibition_suggestion = Paris_exhibitions.loc[(Paris_exhibitions["genre"] == genre) & (Paris_exhibitions["audience"] == audience)]
exhibition_suggested = exhibition_suggestion.sample()

#retrieve the index number of the exhibition suggested

index_suggested = exhibition_suggested.index.item()

#retrieve the exhibition information
#exhibition_suggestion.loc[index_suggested:index_suggested]

title = exhibition_suggested['titre'].values[0]
header = exhibition_suggested['chapeau'].values[0]
location = exhibition_suggested['nom_du_lieu'].values[0]
adresse = exhibition_suggested['adresse_du_lieu'].values[0]
code_postal = exhibition_suggested['code_postal'].values[0]
type_de_prix = exhibition_suggested['type_de_prix'].values[0]

st.divider()

#print out information about the exhibition suggested
st.subheader("Here is one exhibition you could like:")
st.write("**Title:**", title)
st.write('**Description:** ', header)
st.write('**Location:** ', location)
st.write("**Address:**", adresse)
st.write('**Postal code:** ', code_postal)
st.write('**Price:** ', type_de_prix)

st.divider()

#### Select box

# st.subheader("Happy with the exhibition suggested?")

# ### Creating checklists
# select_box_one = st.checkbox("Yes")
# select_box_two = st.checkbox("No")

# ###### Condition 
# if select_box_one: value = "Yes"
# elif select_box_two: value = "No"
# else: value = "No value selected"
# st.write(f"You selected: {value}")