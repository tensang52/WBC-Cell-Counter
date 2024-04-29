import streamlit as st
import plotly.graph_objects as go
import pandas as pd

if "total_counter" not in st.session_state:
    st.session_state.total_counter = 0
if "box_counters" not in st.session_state:
    st.session_state.box_counters = [0, 0, 0, 0, 0, 0]
if "click_history" not in st.session_state:
    st.session_state.click_history = [] 

def increment_counter(index):
    st.session_state.box_counters[index] += 1 
    st.session_state.total_counter += 1  
    st.session_state.click_history.append(index)  

def undo_last_click():
    if st.session_state.click_history:
        last_index = st.session_state.click_history.pop() 
        st.session_state.box_counters[last_index] -= 1  
        st.session_state.total_counter -= 1 

st.title("WBC-Counter")

image_paths = [
    "img/img1.png",
    "img/img4.png",
    "img/img3.png",
    "img/img2.png",
    "img/img5.png",
]

cols1 = st.columns(3)

with cols1[0]:
    if st.button("Segmentkernige Granulozyten"):
        increment_counter(0) 
    st.image(image_paths[0], caption="Segmentkernige Granulozyten", use_column_width=True)
    
    st.markdown("<div style='min-height:30px;'>Zähler: {}</div>".format(st.session_state.box_counters[0]),
                unsafe_allow_html=True)

with cols1[1]:
    if st.button("Stabkernige Granulozyten"):
        increment_counter(1)  
    st.image(image_paths[1], caption="Stabkernige Granulozyten", use_column_width=True)
    st.markdown("<div style='min-height:30px;'>Zähler: {}</div>".format(st.session_state.box_counters[1]), unsafe_allow_html=True)

with cols1[2]:
    if st.button("Monozyten"):
        increment_counter(2) 
    st.image(image_paths[2], caption="Monozyten", use_column_width=True)
    st.markdown("<div style='min-height:30px;'>Zähler: {}</div>".format(st.session_state.box_counters[2]), unsafe_allow_html=True)


cols2 = st.columns(3)

with cols2[0]:
    if st.button("Lymphozyten"):
        increment_counter(3)  
    st.image(image_paths[3], caption="Lymphozyten", use_column_width=True)
    st.markdown("<div style='min-height:30px;'>Zähler: {}</div>".format(st.session_state.box_counters[3]), unsafe_allow_html=True)

with cols2[1]:
    if st.button("Eosinophile"):
        increment_counter(4) 
    st.image(image_paths[4], caption="Eosinophile", use_column_width=True)
    st.markdown("<div style='min-height:30px;'>Zähler: {}</div>".format(st.session_state.box_counters[4]), unsafe_allow_html=True)


if st.button("Letzten Klick rückgängig machen"):
    undo_last_click()


st.markdown(
    f"<div style='text-align:center; font-size:80px; color: red;'>Gesamtzähler: {st.session_state.total_counter}</div>",
    unsafe_allow_html=True,
)


progress = st.session_state.total_counter / 100 * 100  
fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=progress,
        gauge={"axis": {"range": [0, 100]}, "bar": {"color": "red"}},
        domain={"x": [0, 1], "y": [0, 1]}
    )
)
fig.update_layout(title="Fortschrittsanzeige")

st.plotly_chart(fig, use_container_width=True)


if st.session_state.total_counter >= 100:
    st.markdown("**Ziel erreicht!**")


labels = ["Segmentkernige Granulozyten", "Stabkernige Granulozyten", "Monozythen", "Lymphozyten", "Eosinophile"]
sizes = st.session_state.box_counters  
total = st.session_state.total_counter 


percentages = [count / total * 100 if total > 0 else 0 for count in sizes]


fig = go.Figure(data=[go.Pie(labels=labels, values=percentages, hole=0.4, textinfo='percent')])
fig.update_layout(title_text="Prozentualer Anteil der Klicks")

st.plotly_chart(fig, use_container_width=True)
