import streamlit as st
import pandas as pd
import numpy as np
import datetime
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
from PIL import Image
from streamlit_folium import st_folium
import folium

####### Definition

## Machine Learning

def find_similar_exhibitions(index_suggested):
    df = Paris_exhibitions.drop_duplicates(subset=["chapeau"]).reset_index(drop=True)
    strings = list(df["chapeau"])
    strings_without_digits = []
    pattern = r"\d+" # Uses a regex in order to remove the numbers

    for s in strings:
        if isinstance(s, str):
            s_without_digits = re.sub(pattern, "", s)
            strings_without_digits.append(s_without_digits)
        else:
            strings_without_digits.append(s)

    keywords = list(df["mots_clés"]) # Convert the keywords into a list

    # Create CountVectorizer and fit_transform the texts
    vectorizer = CountVectorizer()
    texts = ["" if pd.isna(text) else text for text in strings_without_digits]
    vectors = vectorizer.fit_transform(texts)
    vocabulary = vectorizer.get_feature_names_out()

    # Create DataFrame with the vectors
    headers = pd.DataFrame.sparse.from_spmatrix(vectors, columns=vocabulary, index=texts)

    # Create CountVectorizer and fit_transform the keywords
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(keywords)
    vocabulary = vectorizer.get_feature_names_out()

    # Create DataFrame with the vectors
    keywords = pd.DataFrame.sparse.from_spmatrix(vectors, columns=vocabulary, index=keywords)

    # Apply PCA on headers
    pca = PCA(n_components=15)  # Specify the number of components to keep
    vectors_pca = pca.fit_transform(headers.to_numpy())

    # Create DataFrame with PCA components for headers
    headers_pca = pd.DataFrame(vectors_pca, index=df.index)

    # Apply PCA on keywords
    pca = PCA(n_components=15)  # Specify the number of components to keep
    vectors_pca = pca.fit_transform(keywords.to_numpy())

    # Create DataFrame with PCA components for keywords
    keywords_pca = pd.DataFrame(vectors_pca, index=keywords.index)

    # Concatenate the PCA components
    concatenated_df = pd.concat([headers_pca, keywords_pca])

    # Fit Nearest Neighbors model
    neigh = NearestNeighbors(n_neighbors=6)
    neigh.fit(concatenated_df)

    # Find similar exhibitions based on the exhibition index suggested
    distances, indices = neigh.kneighbors(concatenated_df.iloc[index_suggested:index_suggested+1])

    # Return the similar exhibitions
    return Paris_exhibitions.iloc[indices[0]]

####### Title 
st.title('Art exhibition :art:')
st.header('Welcome to my art exhibitions recommender in Paris!')

##### Image #########
image = Image.open('Images/kandinsky-jaune-rouge-bleu-bandeau.jpg')
st.image(image) 

# import file about the French museums info
Paris_exhibitions = pd.read_csv('Cleaned_data/Paris_exhibitions.csv', sep=',', encoding='UTF8')
pd.set_option('display.max_columns', 20)

##### Data input - date of the exhibition
d = st.date_input(':alarm_clock: When do you want to go for an exhibition?', datetime.date(2023, 6, 9))
Paris_exhibitions["date_choisie"] = d

##### Data input - genre of the exhibition

genres = ['Art contemporain', 'Expo', 'Littérature', 'Cinéma', 'Bd', 'Histoire', 'Lgbt', 'Photo', 'Innovation', 'Nature', 'Photographie', 'Street-art', 'Peinture', 'Sculpture', 'Sciences']
genre = st.selectbox(":sparkles: What kind of exhibition are you interested in?", genres)

##### Data input - audience of the exhibition

audience = Paris_exhibitions['audience'].sort_values(ascending=False).unique()
audience = st.selectbox(":family: For whom?", audience)

##### Output user's selection

st.write('You want to go to an exhibition on:', d)
st.write("**Genre:**", genre)
st.write('**Audience:**', audience)

##### Exhibition suggestion

# NOTE: VOIR POUR FILTRER EN FONCTION DE LA DATE 

exhibition_suggestion = Paris_exhibitions.loc[(Paris_exhibitions["genre"] == genre) & (Paris_exhibitions["audience"] == audience)]

exhibition_suggested = exhibition_suggestion.sample()

# retrieve the index number of the exhibition suggested
index_suggested = exhibition_suggested.index.item()

# removes the exhibition suggested from the exhibition suggestion
new_exhibition_suggestion = exhibition_suggestion.drop(index=index_suggested)

# create variables to display after

title = exhibition_suggested['titre'].values[0]
header = exhibition_suggested['chapeau'].values[0]
location = exhibition_suggested['nom_du_lieu'].values[0]
adresse = exhibition_suggested['adresse_du_lieu'].values[0]
code_postal = exhibition_suggested['code_postal'].values[0]
type_de_prix = exhibition_suggested['type_de_prix'].values[0]
url = exhibition_suggested['url'].values[0]
ville = exhibition_suggested['ville'].values[0]
lat = exhibition_suggested['latitude'].values[0]
long = exhibition_suggested['longitude'].values[0]

st.divider()

### Select box

correct = st.selectbox(":white_check_mark: Is it correct?", ['Your answer...', 'Yes','No'])

import sys
import streamlit as st

# Initialize session state
if 'map_shown' not in st.session_state:
    st.session_state.map_shown = False

###### Condition 
if correct == 'Yes':
    # print out information about the exhibition suggested
    st.divider()
    st.subheader("Here is one exhibition you might like:")
    st.write("**Title:**", title)
    st.write('**Description:**', header)
    st.write('**Location:**', location)
    st.write("**Address:**", adresse)
    st.write(adresse)
    st.write(code_postal)
    st.write(ville)
    st.write('**Price:**', type_de_prix)
    st.write('**URL:**', url)

    # Create a map button
    show_map = st.button(":white_check_mark: Show Location on Map")

    # Check if the show_map button is clicked and map has not been shown
    if show_map and not st.session_state.map_shown:
        # Set the map_shown session state to True
        st.session_state.map_shown = True

        # Create a map
        m = folium.Map(location=[lat, long], zoom_start=16)
        folium.Marker([lat, long], popup="location").add_to(m)
        st_data = st_folium(m, width=725)

else:
    st.write("Give us some information about what you're looking for!")

# Reset map_shown session state if the exhibition suggestion changes
if exhibition_suggested.index.item() != st.session_state.get('exhibition_index'):
    st.session_state.map_shown = False

# Set the exhibition_index session state
st.session_state.exhibition_index = exhibition_suggested.index.item()



st.divider()


### Select box

interested = st.selectbox(":rocket: You liked it? Check out related activities we thought of for you!", ['Your answer...', 'Yes','No'])

###### Condition 
if interested == 'Yes':
    similar_exhibitions = find_similar_exhibitions(index_suggested)
    st.write(pd.DataFrame(similar_exhibitions))
elif interested == 'No':
    st.write("Sorry, we're trying our best to match your tastes. :cry: Check the new exhibition we found out for you! :point_up_2:")
else:
    st.write("No value selected")
