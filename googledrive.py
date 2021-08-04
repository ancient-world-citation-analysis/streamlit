import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import base64
from googleapiclient import discovery
from httplib2 import Http
import oauth2client
from oauth2client import file, client, tools
import os

import asyncio

from session_state import get
from httpx_oauth.clients.google import GoogleOAuth2


async def write_authorization_url(client,
                                  redirect_uri):
    authorization_url = await client.get_authorization_url(
        redirect_uri,
        scope=["https://www.googleapis.com/auth/drive.file"],
    )
    return authorization_url


async def write_access_token(client,
                             redirect_uri,
                             code):
    token = await client.get_access_token(code, redirect_uri)
    return token

def download_page():
    st.write(f"Let's process your pdf file.")

client_id = ''
client_secret = ''
redirect_uri = ''

client = GoogleOAuth2(client_id, client_secret)
authorization_url = asyncio.run(
        write_authorization_url(client=client,
                                redirect_uri=redirect_uri)
    )

session_state = get(token=None)
if session_state.token is None:
    try:
        code = st.experimental_get_query_params()['code']
    except:
        st.write(f'''<h1>
            Please give us access to pdf using this <a target="_self"
            href="{authorization_url}">url</a></h1>''',
                     unsafe_allow_html=True)
    else:
            # Verify token is correct:
        try:
            token = asyncio.run(
                write_access_token(client=client,
                                       redirect_uri=redirect_uri,
                                       code=code))
        except:
            st.write(f'''<h1>
                    This account is not allowed or page was refreshed.
                    Please try again: <a target="_self"
                    href="{authorization_url}">url</a></h1>''',
                         unsafe_allow_html=True)
        else:
                # Check if token has expired:
            if token.is_expired():
                if token.is_expired():
                    st.write(f'''<h1>
                        Login session has ended,
                        please <a target="_self" href="{authorization_url}">
                        login</a> again.</h1>
                        ''')
            else:
                    session_state.token = token

download_page()

@st.cache
def load_model():

    save_dest = Path('model')
    save_dest.mkdir(exist_ok=True)
    
    f_checkpoint = Path("model/skyAR_coord_resnet50.pt")

    if not f_checkpoint.exists():
        with st.spinner("Downloading model... this may take awhile! \n Don't stop it!"):
            from GD_download import download_file_from_google_drive
            download_file_from_google_drive(cloud_model_location, f_checkpoint)
    
    model = torch.load(f_checkpoint, map_location=device)
    model.eval()
    return model


