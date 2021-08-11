import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
import streamlit as st

@st.cache
def get_model():
    model = T5ForConditionalGeneration.from_pretrained('t5-small')
    return model
@st.cache
def get_tokenizer():
    tokenizer = T5Tokenizer.from_pretrained('t5-small')
    return tokenizer

tokenizer = get_tokenizer()
model = get_model()

def preprocess(text):
    preprocess_text = text.strip().replace("\n","")
    t5_prepared_Text = "summarize: "+ preprocess_text
    print ("original text preprocessed: \n", preprocess_text)
    tokenized_text = tokenizer.encode(t5_prepared_Text, return_tensors="pt")
    return tokenized_text

def app():
    st.title("Text Summarization using Machine Learning and BERT")
    bert = "BERT is designed to pre-train deep bidirectional representations from unlabeled text. it can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial task-specific architecture modifications."
    st.write(bert)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original")
        with st.form("Paste Here then Click the submit button"):
            text = st.text_area("Paste the text you want summarized here, then click the submit button", height=250)
            tokenized_text = preprocess(text)

            selection = st.selectbox("Select the Length of Output", ["Short", "Medium", "Long"])
            
            if selection == "Short":
                min_length, max_length = 30, 100
            elif selection == "Medium":
                min_length, max_length = 90, 300
            else:
                min_length, max_length = 150, 600

            summary_ids = model.generate(tokenized_text,
                                    num_beams=4,
                                    no_repeat_ngram_size=2,
                                    min_length=min_length,
                                    max_length=max_length,
                                    early_stopping=True)
            output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            submitted = st.form_submit_button("Submit")
    with col2:
        st.subheader('Summarized')
        if submitted:
            st.write(output)