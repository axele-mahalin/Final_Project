import streamlit as st
import pandas as pd
import numpy as np
import datetime
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
from PIL import Image
from streamlit_folium import st_folium, folium_static
import folium

pd.set_option('display.max_columns', 20)

###### To run streamlit page type in terminal 
######## streamlit run art_exhibitions.py

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
    vectorizer = CountVectorizer() # Create CountVectorizer and fit_transform the texts
    texts = ["" if pd.isna(text) else text for text in strings_without_digits]
    vectors = vectorizer.fit_transform(texts)
    vocabulary = vectorizer.get_feature_names_out()
    headers = pd.DataFrame.sparse.from_spmatrix(vectors, columns=vocabulary, index=texts) # Create DataFrame with the vectors
    vectorizer = CountVectorizer() # Create CountVectorizer and fit_transform the keywords
    vectors = vectorizer.fit_transform(keywords)
    vocabulary = vectorizer.get_feature_names_out()
    keywords = pd.DataFrame.sparse.from_spmatrix(vectors, columns=vocabulary, index=keywords) # Create DataFrame with the vectors
    pca = PCA(n_components=15) # Specify the number of components to keep
    vectors_pca = pca.fit_transform(headers.to_numpy()) # Create DataFrame with PCA components for headers
    headers_pca = pd.DataFrame(vectors_pca, index=df.index)
    pca = PCA(n_components=15)  # Specify the number of components to keep
    vectors_pca = pca.fit_transform(keywords.to_numpy())
    keywords_pca = pd.DataFrame(vectors_pca, index=keywords.index) # Create DataFrame with PCA components for keywords
    concatenated_df = pd.concat([headers_pca, keywords_pca]) # Concatenate the PCA components
    neigh = NearestNeighbors(n_neighbors=6) # Fit Nearest Neighbors model
    neigh.fit(concatenated_df)
    distances, indices = neigh.kneighbors(concatenated_df.iloc[index_suggested:index_suggested+1]) # Find similar exhibitions based on the exhibition index suggested
    return Paris_exhibitions.iloc[indices[0]][1:] # Return the similar exhibitions

## Display exhibitions info

# create variables to display after

def variables_to_display(data):
    if isinstance(data, pd.DataFrame):
        for i in range(len(data)):
            st.write("**Title:**", data['titre'].values[i])
            st.write('**Description:**', data['chapeau'].values[i])
            st.write('**Location:**', data['nom_du_lieu'].values[i])
            st.write("**Address:**")
            st.write(data['adresse_du_lieu'].values[i])
            st.write(data['code_postal'].values[i])
            st.write(data['ville'].values[i])
            st.write('**Price:**', data['type_de_prix'].values[i])
            st.write('**URL:**', data['url'].values[i])
            st.divider()
    elif isinstance(data, pd.Series):
        st.write("**Title:**", data['titre'])
        st.write('**Description:**', data['chapeau'])
        st.write('**Location:**', data['nom_du_lieu'])
        st.write("**Address:**")
        st.write(data['adresse_du_lieu'])
        st.write(data['code_postal'])
        st.write(data['ville'])
        st.write('**Price:**', data['type_de_prix'])
        st.write('**URL:**', data['url'])
        st.divider()


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
genre = st.selectbox(":sparkles: What kind of exhibition are you interested in?", options=genres, index=0)

##### Data input - audience of the exhibition

audience = Paris_exhibitions['audience'].sort_values(ascending=False).unique()
audience = st.selectbox(":family: For whom?", options=audience, index=0)

##### Output user's selection

st.write('You want to go to an exhibition on:', d)
st.write("**Genre:**", genre)
st.write('**Audience:**', audience)

##### Exhibition suggestion

exhibition_suggestion = Paris_exhibitions.loc[(Paris_exhibitions["genre"] == genre) & (Paris_exhibitions["audience"] == audience)]

exhibition_suggested = exhibition_suggestion.sample()

# retrieve the index number of the exhibition suggested
index_suggested = exhibition_suggested.index.item()

# removes the exhibition suggested from the exhibition suggestion
new_exhibition_suggestion = exhibition_suggestion.drop(index=index_suggested)

correct = st.selectbox(":white_check_mark: Is it correct?", ['Your answer...', 'Yes', 'No'], index=0)

###### Condition 
if correct == 'Yes':
    # print out information about the exhibition suggested
    st.subheader("Here is one exhibition you might like:")
    variables_to_display(exhibition_suggested)
    # Create a map
    lat = exhibition_suggested['latitude'].values[0]
    long = exhibition_suggested['longitude'].values[0]
    m = folium.Map(location=[lat, long], zoom_start=16)
    folium.Marker([lat, long], popup=exhibition_suggested['nom_du_lieu'].values[0]).add_to(m)
    folium_static(m, width=725)
else:
    st.write("Give us some information about what you're looking for!")

### Select box

interested = st.selectbox(":rocket: You liked it? Check out related activities we thought of for you!", options=['Your answer...', 'Yes','No'])

###### Condition 
if interested == 'Yes':
    similar_exhibitions = find_similar_exhibitions(index_suggested)
    variables_to_display(similar_exhibitions)
elif interested == 'No':
    st.write("Sorry, we're trying our best to match your tastes. :cry: Check the new exhibition we found out for you! :point_up_2:")
else:
    st.write("No value selected")
