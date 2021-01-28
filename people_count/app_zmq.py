import streamlit as st
import pandas as pd
import time

import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://127.0.0.1:2000')
socket.setsockopt_string(zmq.SUBSCRIBE,'')


###
st.set_page_config(layout="wide")

st.markdown("""
<style>
.big-font {
    font-size:300px !important;
}
</style>
""", unsafe_allow_html=True)
###


st.write("""
# Total People Currently
""")
placeholder = st.empty()
mdText = ""
while True:
    message = socket.recv_pyobj()
    mdText = '<p class="big-font">'+ str(message.get("Total_People")) +'</p>'
    placeholder.markdown(mdText, unsafe_allow_html=True)