import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import base64
import os
import pytesseract
import pandas as pd
from pdf2image import *
import PIL
import re
from PyPDF3 import PdfFileWriter, PdfFileReader
import io
#Import the garbage collection module
import gc
#Enable garbage collection
gc.enable()
#Clean up the memory from unused objects


def populate_ocr(files):
    page_ids = []
    #list of all documents
    page_texts = []
    for open_file in files:
        page_ids.append(open_file.name)
        inputpdf = PdfFileReader(io.BytesIO(open_file.getvalue()))
        maxPages = inputpdf.numPages
        image_counter = 1
        for page in range(1, maxPages, 10):
            try:
                images = convert_from_bytes(open_file.getvalue(), first_page=page, last_page=min(page + 10 - 1, maxPages))
                for image in images:
                    image.save('page' + str(image_counter) + '.jpg', 'jpeg')
                    image_counter += 1
            except exceptions.PDFPageCountError as error:
                st.write("Error:")
                st.write(page)
                continue
            

        filelimit = image_counter - 1
        #list of each document
        individual = []
        # read the images generated, and turn into csv using ocr
        for i in range(1, image_counter):
            filename = "page" + str(i) + ".jpg"
            text = pytesseract.image_to_string(PIL.Image.open(filename))
            text.replace("\n'", " ")
            individual += [text]
            if os.path.isfile(filename):
                os.remove(filename)
            else:    ## Show an error ##
                print("Error: %s file not found" % filename)
        page_texts.append(individual)
        
    csv = pd.DataFrame(data={
        'page_ids': page_ids,
        'page_texts': page_texts
    }).to_csv(index=False)
    return csv

def app():
    # Create a title
    st.title('PDF2CSV')
    # Create content and a mock data frame
    st.write('first attempt at creating a csv using OCR from PDF, please be patient while we work the Optical Character Recognition Model :D')
    uploaded_files = st.file_uploader("Choose a PDF file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        st.write("filename:", uploaded_file.name)
        st.header("File Download - A Workaround")

    csv = populate_ocr(uploaded_files)

    gc.collect()

    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as &lt;some_name&gt;.csv)'
    st.markdown(href, unsafe_allow_html=True)