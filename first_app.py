import streamlit as st

st.set_page_config(layout="wide")

from multiapp import MultiApp

import OCR
import text_sum



app = MultiApp()

app.add_app("Optical Character Recognition", OCR.app)
app.add_app("Text Summarization and Paraphrasing", text_sum.app)

app.run()