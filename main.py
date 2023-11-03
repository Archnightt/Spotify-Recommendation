import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import time
from model import *



if 'model' not in st.session_state:
    st.session_state.model = 'Model 1'
def update_radio2():
    st.session_state.model=st.session_state.radio2
if 'genre' not in st.session_state:
    st.session_state.genre=3
def update_num_genre():
    st.session_state.genre=st.session_state.num_genre
if 'artist' not in st.session_state:
    st.session_state.artist=5
def update_same_art():
    st.session_state.artist=st.session_state.same_art
if 'model2' not in st.session_state:
    st.session_state.model2= 'Spotify model'
def update_radio1():
    st.session_state.model2 =st.session_state.radio1

if 'Region' not in st.session_state:
    st.session_state.rg="US"
def update_Region():
    st.session_state.rg=st.session_state.Region
if 'radio' not in st.session_state:
    st.session_state.feature="Playlist"
def update_radio0():
    st.session_state.feature=st.session_state.radio

if 'p_url' not in st.session_state:
    st.session_state.p_url = 'Example: https://open.spotify.com/playlist/37i9dQZF1EIYWwGqC3GC7o?si=aaa6068f7c3a4e57'
def update_playlist_url():
    st.session_state.p_url = st.session_state.playlist_url

if 's_url' not in st.session_state:
    st.session_state.s_url = 'Example: https://open.spotify.com/track/4NBTZtAt1F13VvlSKe6KTl?si=022f75b726cc40d5'
def update_song_url():
    st.session_state.s_url = st.session_state.song_url

if 'a_url' not in st.session_state:
    st.session_state.a_url = 'Example: https://open.spotify.com/artist/00FQb4jTyendYWaN8pK0wa?si=KzBERu6WSuarjD-EqGtHwQ'
def update_artist_url():
    st.session_state.a_url = st.session_state.artist_url


def play_recomm():
    if 'rs' in st.session_state:
        del st.session_state.rs,st.session_state.err
    try:
        if len(pd.read_csv('Data/new_tracks.csv')) >= 200:
            with st.spinner('Updating the dataset...'):
                x=update_dataset()
                st.success('{} New tracks were added to the dataset.'.format(x))
    except:
        st.error("The dataset update failed. ")
    with st.spinner('Getting Recommendations...'):
        res,err = playlist_model(st.session_state.p_url,st.session_state.model,st.session_state.genre,st.session_state.artist)
        st.session_state.rs=res
        st.session_state.err=err
    if len(st.session_state.rs)>=1:
        if st.session_state.model == 'Model 1' or st.session_state.model == 'Model 2':
            st.success('Go to the Result page to view the top {} recommendations'.format(len(st.session_state.rs)))
        else:
            st.success('Go to the Result page to view the  Spotify recommendations')
    else:
        st.error('Model failed. Check the log for more information.')   

def art_recomm():
    if 'rs' in st.session_state:
        del st.session_state.rs,st.session_state.err
    with st.spinner('Getting Recommendations...'):
        res,err = top_tracks(st.session_state.a_url,st.session_state.rg)
        st.session_state.rs=res
        st.session_state.err=err
    if len(st.session_state.rs)>=1:
        st.success("Go to the Result page to view the Artist's top tracks")
    else:
        st.error('Model failed. Check the log for more information.')

def song_recomm():
    if 'rs' in st.session_state:
        del st.session_state.rs,st.session_state.err
    with st.spinner('Getting Recommendations...'):
        res,err = song_model(st.session_state.s_url,st.session_state.model,st.session_state.genre,st.session_state.artist)
        st.session_state.rs=res
        st.session_state.err=err
    if len(st.session_state.rs)>=1:
        if st.session_state.model == 'Model 1' or st.session_state.model == 'Model 2':
            st.success('Go to the Result page to view the top {} recommendations'.format(len(st.session_state.rs)))
        else:
            st.success('Go to the Result page to view the  Spotify recommendations')
    else:
        st.error('Model failed. Check the log for more information.')

def playlist_page():
    st.subheader("User Playlist")
    st.markdown('---')
    playlist_uri = (st.session_state.playlist_url).split('/')[-1].split('?')[0]
    uri_link = 'https://open.spotify.com/embed/playlist/' + playlist_uri
    components.iframe(uri_link, height=300)
    return

def song_page():
    st.subheader("User Song")
    st.markdown('---')
    song_uri = (st.session_state.song_url).split('/')[-1].split('?')[0]
    uri_link = 'https://open.spotify.com/embed/track/' + song_uri
    components.iframe(uri_link, height=100)

def artist_page():
    st.subheader("User Artist")
    st.markdown('---')
    artist_uri = (st.session_state.artist_url).split('/')[-1].split('?')[0]
    uri_link = 'https://open.spotify.com/embed/artist/' + artist_uri
    components.iframe(uri_link, height=80)


def spr_sidebar():
    menu=option_menu(
        menu_title=None,
        options=['Home','Result','Log'],
        icons=['house','book','info-square','terminal'],
        menu_icon='cast',
        default_index=0,
        orientation='horizontal'
    )
    if menu=='Home':
        st.session_state.app_mode = 'Home'
    elif menu=='Result':
        st.session_state.app_mode = 'Result'
    elif menu=='Log':
        st.session_state.app_mode = 'Log'
    
def home_page():
    st.session_state.radio=st.session_state.feature
    st.session_state.radio2=st.session_state.model
    st.session_state.num_genre=st.session_state.genre
    st.session_state.same_art=st.session_state.artist
    st.session_state.Region=st.session_state.rg

    
    st.title('Spotify Recommendation System')
    col,col2,col3=st.columns([2,2,3])
    radio=col.radio("Feature",options=("Playlist","Song","Artist Top Tracks"),key='radio',on_change=update_radio0)
    if radio =="Artist Top Tracks":
        radio1=col2.radio("Model",options=["Spotify model"],key='radio1',on_change=update_radio1)
        Region=col3.selectbox("Please Choose Region",index=58,key='Region',on_change=update_Region,options=('AD', 'AR', 'AU', 'AT', 'BE', 'BO', 'BR', 'BG', 'CA', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DK', 'DO', 'EC', 'SV', 'EE', 'FI', 'FR', 'DE', 'GR', 'GT', 'HN', 'HK', 'HU', 'IS', 'ID', 'IE', 'IT', 'JP', 'LV', 'LI', 'LT', 'LU', 'MY', 'MT', 'MX', 'MC', 'NL', 'NZ', 'NI', 'NO', 'PA', 'PY', 'PE', 'PH', 'PL', 'PT', 'SG', 'ES', 'SK', 'SE', 'CH', 'TW', 'TR', 'GB', 'US', 'UY'))
    elif radio =="Playlist" or radio =="Song" :
        radio2=col2.radio("Model",options=("Model 1","Model 2","Spotify Model"),key='radio2',on_change=update_radio2)
        if st.session_state.radio2=="Model 1" or st.session_state.radio2=="Model 2":
            num_genre=col3.selectbox("choose a number of genres to focus on",options=(1,2,3,4,5,6,7),index=2,key='num_genre',on_change=update_num_genre)
            same_art=col3.selectbox("How many recommendations by the same artist",options=(1,2,3,4,5,7,10,15),index=3,key='same_art',on_change=update_same_art)


    st.markdown("<br>", unsafe_allow_html=True)
    
    if radio == "Playlist" :
        st.session_state.playlist_url = st.session_state.p_url
        Url = st.text_input(label="Playlist Url",key='playlist_url',on_change=update_playlist_url)
        playlist_page()
        state =st.button('Get Recommendations')
        with st.expander("Here's how to find any Song URL in Spotify"):
            st.write(""" 
                - Search for Song on the Spotify app
                - Right Click on the Song you like
                - Click "Share"
                - Choose "Copy link to playlist"
            """)
            st.markdown("<br>", unsafe_allow_html=True)

        if state:
            play_recomm()
    elif radio == "Song" :
        st.session_state.song_url = st.session_state.s_url
        Url = st.text_input(label="Song Url",key='song_url',on_change=update_song_url)
        song_page()
        state =st.button('Get Recommendations')
        with st.expander("Here's how to find any Song URL in Spotify"):
            st.write(""" 
                - Search for Song on the Spotify app
                - Right Click on the Song you like
                - Click "Share"
                - Choose "Copy link to Song"
            """)
            st.markdown("<br>", unsafe_allow_html=True)

        if state:
            song_recomm()
    elif radio == "Artist Top Tracks" :
        st.session_state.artist_url = st.session_state.a_url
        Url = st.text_input(label="Artist Url",key='artist_url',on_change=update_artist_url)
        artist_page()
        state =st.button('Get Recommendations')
        with st.expander("Here's how to find any Artist URL in Spotify"):
            st.write(""" 
                - Search for Artist on the Spotify app
                - Right Click on the Artist you like
                - Click "Share"
                - Choose "Copy link to Artist"
            """)
            st.markdown("<br>", unsafe_allow_html=True)

        if state:
            art_recomm()
    
def result_page():
    if 'rs' not in st.session_state:
        st.error('Please select a model on the Home page and run Get Recommendations')
    else:
        st.success('Top {} recommendations'.format(len(st.session_state.rs)))
        i=0
        for uri in st.session_state.rs:
         uri_link = "https://open.spotify.com/embed/track/" + uri + "?utm_source=generator&theme=0"
         components.iframe(uri_link, height=80)
         i+=1
         if i%5==0:
            time.sleep(1)
def Log_page():
    log=st.checkbox('Display Output', True, key='display_output')
    if log == True:
     if 'err' in st.session_state:
        st.write(st.session_state.err)
    with open('Data/streamlit.csv') as f:
        st.download_button('Download Dataset', f,file_name='streamlit.csv')

def main():
    spr_sidebar()        
    if st.session_state.app_mode == 'Home':
        home_page()
    if st.session_state.app_mode == 'Result':
        result_page()
    if st.session_state.app_mode == 'Log':
        Log_page()
# Run main()
if __name__ == '__main__':
    main()

stream= open("Spotify.yaml")
spotify_details = yaml.safe_load(stream)
auth_manager = SpotifyClientCredentials(client_id=spotify_details['Client_id'],
                                        client_secret=spotify_details['client_secret'])
sp = spotipy.client.Spotify(auth_manager=auth_manager)