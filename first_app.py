import streamlit as st
from multiapp import MultiApp

import OCR
import text_sum

app = MultiApp()

app.add_app("Optical Character Recognition", OCR.app)
#app.add_app("Text Summarization", text_sum.app)

app.run()