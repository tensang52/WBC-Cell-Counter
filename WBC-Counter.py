import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# Initialize session state variables
if "total_counter" not in st.session_state:
    st.session_state.total_counter = 0
if "box_counters" not in st.session_state:
    st.session_state.box_counters = [0, 0, 0, 0, 0]
if "click_history" not in st.session_state:
    st.session_state.click_history = []
if "is_saved" not in st.session_state:
    st.session_state.is_saved = False

# Functions to increment counters and undo last click
def increment_counter(index):
    st.session_state.box_counters[index] += 1
    st.session_state.total_counter += 1
    st.session_state.click_history.append(index)
    if st.session_state.total_counter >= 200 and not st.session_state.is_saved:
        save_data()
    st.experimental_rerun()

def undo_last_click():
    if st.session_state.click_history:
        last_index = st.session_state.click_history.pop()
        st.session_state.box_counters[last_index] -= 1
        st.session_state.total_counter -= 1
        st.experimental_rerun()

def save_data():
    if patient_name and patient_birthdate and patient_gender and patient_id:
        data = {
            "Patient ID": [patient_id],
            "Name": [patient_name],
            "Birthdate": [patient_birthdate.strftime("%Y-%m-%d")],
            "Gender": [patient_gender],
            "Segmentkernige Granulozyten": [st.session_state.box_counters[0]],
            "Stabkernige Granulozyten": [st.session_state.box_counters[1]],
            "Monozyten": [st.session_state.box_counters[2]],
            "Lymphozyten": [st.session_state.box_counters[3]],
            "Eosinophile": [st.session_state.box_counters[4]],
            "Total": [st.session_state.total_counter],
            "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        }

        df = pd.DataFrame(data)
        df.to_csv("archive.csv", mode='a', header=not pd.io.common.file_exists("archive.csv"), index=False)
        st.session_state.is_saved = True
        st.sidebar.success("Data saved to archive.")
    else:
        st.sidebar.error("Please enter all patient information.")

# Sidebar for patient information
st.sidebar.title("Patient Information")
patient_name = st.sidebar.text_input("Name")
patient_birthdate = st.sidebar.date_input("Birthdate")
patient_gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
patient_id = st.sidebar.text_input("Patient ID")

# Main content
st.title("WBC-Counter")

image_paths = [
    "img/img1.png",
    "img/img2.png",
    "img/img3.png",
    "img/img4.png",
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

progress = st.session_state.total_counter / 200 * 100
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

if st.session_state.total_counter >= 200:
    st.markdown("**Ziel erreicht!**")

labels = ["Segmentkernige Granulozyten", "Stabkernige Granulozyten", "Monozyten", "Lymphozyten", "Eosinophile"]
sizes = st.session_state.box_counters
total = st.session_state.total_counter

percentages = [count / total * 100 if total > 0 else 0 for count in sizes]

fig = go.Figure(data=[go.Pie(labels=labels, values=percentages, hole=0.4, textinfo='percent')])
fig.update_layout(title_text="Prozentualer Anteil der Klicks")

st.plotly_chart(fig, use_container_width=True)

