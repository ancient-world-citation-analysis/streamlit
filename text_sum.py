import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import streamlit as st
import time

@st.cache
def get_model():
    model = T5ForConditionalGeneration.from_pretrained('t5-small')
    return model
@st.cache
def get_tokenizer():
    tokenizer = T5Tokenizer.from_pretrained('t5-small')
    return tokenizer
@st.cache
def get_p_model():
    model = AutoModelForSeq2SeqLM.from_pretrained('Vamsi/T5_Paraphrase_Paws')
    return model
@st.cache
def get_p_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained('Vamsi/T5_Paraphrase_Paws')
    return tokenizer

tokenizer = get_tokenizer()
model = get_model()
p_tokenizer = get_p_tokenizer()
p_model = get_p_model()

@st.cache(allow_output_mutation=True)
def preprocess(texts):
    preprocess_texts = texts.strip().replace("\n", "")
    texts1 = [preprocess_texts[n*512: (n+1)*512] for n in range(len(preprocess_texts) // 512)]
    tokens=[]
    for text in texts1:
        t5_prepared_Text = "summarize: "+ text
        print ("original text preprocessed: \n", text)
        tokenized_text = tokenizer.encode(t5_prepared_Text, return_tensors="pt")
        tokens.append(tokenized_text)
    return tokens

@st.cache(allow_output_mutation=True)
def paraphrase(texts):
    start = time.time()
    texts1 = texts.split("\n")
    #texts1 = [texts[n * 512 : (n + 1) * 512] for n in range(len(texts) // 512)]
    lines = ""
    for texts2 in texts1:
        
        texts2 =  "paraphrase: " + texts2

        encoding = p_tokenizer.encode_plus(texts2,padding='max_length', return_tensors="pt")
        input_ids, attention_masks = encoding["input_ids"], encoding["attention_mask"]

        outputs = p_model.generate(
            input_ids=input_ids, attention_mask=attention_masks,
            max_length=10000,
            do_sample=True,
            top_k=120,
            top_p=0.95,
            early_stopping=True,
            num_return_sequences=1
        )
    
        line = p_tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
        line += "\n\n"
        lines += line
    end = time.time()
    return lines

@st.cache(allow_output_mutation=True)
def get_summarization(tokenized_texts, min_length, max_length):
    outputs = ""
    for text in tokenized_texts:
        summary_ids = model.generate(text,
                                    num_beams=4,
                                    no_repeat_ngram_size=2,
                                    min_length=min_length,
                                    max_length=max_length,
                                    early_stopping=True)
        output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        output += "\n\n"
        outputs += output
    return outputs


def app():
    
    st.title("Text Summarization and Paraphrasing using Machine Learning and BERT")
    bert = """
    - [Summarization and Paraphrasing] When choosing both summarization and paraphrasing option, the text will be summarized then paraphrased.
    - [Length Selection] only applies to Summarization.
    """
    st.markdown(bert)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original")
        with st.form("Paste Here then Click the submit button"):

            text = st.text_area("Paste the text you want summarized or paraphrased here, then click the submit button", height=250)

            # Choosing whether to paraphrase or summarize
            sorp = st.selectbox("Multiselect Paraphrase or Summarize", options=["Summarization and Paraphrasing", "Summarization Only", "Paraphrasing Only"])
            
            output = ""
            if sorp == "Paraphrasing Only":
                output = paraphrase(text)
                
            elif sorp == "Summarization and Paraphrasing":
                # Choosing the length of summarization
                selection = st.selectbox("Select the Length of Output", ["Short", "Medium", "Long"])
                if selection == "Short":
                    min_length, max_length = 10, 20
                elif selection == "Medium":
                    min_length, max_length = 20, 35
                elif selection == "Long":
                    min_length, max_length = 35, 100
            
                # Get output of summarization
                tokenized_texts1 = preprocess(text).copy()
                outputs = get_summarization(tokenized_texts1, min_length, max_length)

                output = paraphrase(outputs)
                
            elif sorp == "Summarization Only":
                # Choosing the length of summarization
                selection = st.selectbox("Select the Length of Output", ["Short", "Medium", "Long"])
                if selection == "Short":
                    min_length, max_length = 10, 20
                elif selection == "Medium":
                    min_length, max_length = 20, 35
                elif selection == "Long":
                    min_length, max_length = 35, 100
            
                # Get output of summarization
                tokenized_texts = preprocess(text).copy()
                outputs = get_summarization(tokenized_texts, min_length, max_length)
                output = outputs
                
            else:
                output = ""
            
            submitted = st.form_submit_button("Submit")
            # submit button
            
    
    with col2:
        st.subheader('Output')
        if submitted:
            st.write(output)