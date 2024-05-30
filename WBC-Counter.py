import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from PIL import Image

# Create tabs
tab1, tab3, tab2, tab4, tab5 = st.tabs(["Counter", "Resultate", "Referenzliste", "Informationen", "Leukozyten"])

with tab1:
    # Initialize session state variables
    if "total_counter" not in st.session_state:
        st.session_state.total_counter = 0
    if "box_counters" not in st.session_state:
        st.session_state.box_counters = [0] * 13  # Updated for 13 cell types
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
        if sample_name and sample_birthdate and sample_gender and sample_id:
            data = {
                "Sample ID": [sample_id],
                "Name": [sample_name],
                "Birthdate": [sample_birthdate.strftime("%Y-%m-%d")],
                "Gender": [sample_gender],
                "Segmentkernige G.": [st.session_state.box_counters[0]],
                "Stabkernige G.": [st.session_state.box_counters[1]],
                "Monozyten": [st.session_state.box_counters[2]],
                "Lymphozyten": [st.session_state.box_counters[3]],
                "Basophile": [st.session_state.box_counters[4]],
                "Eosinophile": [st.session_state.box_counters[5]],
                "Erythroblasten": [st.session_state.box_counters[6]],
                "Metamyelozyt": [st.session_state.box_counters[7]],
                "Myeloblast": [st.session_state.box_counters[8]],
                "Myelozyt": [st.session_state.box_counters[9]],
                "Plasmazelle": [st.session_state.box_counters[10]],
                "Promyelozyt": [st.session_state.box_counters[11]],
                "Unbekannt": [st.session_state.box_counters[12]],
                "Total": [st.session_state.total_counter],
                "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            }

            df = pd.DataFrame(data)
            df.to_csv("archive.csv", mode='a', header=not pd.io.common.file_exists("archive.csv"), index=False)
            st.session_state.is_saved = True
            st.sidebar.success("Daten in Archiv gespeichert.")
        else:
            st.sidebar.error("Bitte alle Probeninformationen eingeben.")

    # Sidebar for sample information
    st.sidebar.title("Probeninformationen")
    sample_name = st.sidebar.text_input("Name")
    sample_birthdate = st.sidebar.date_input("Geburtsdatum")
    sample_gender = st.sidebar.selectbox("Geschlecht", ["Männlich", "Weiblich", "Andere"])
    sample_id = st.sidebar.text_input("Proben-ID")

    # Main content
    st.title("WBC-Counter")
    st.markdown(f"Gesamtzähler: {st.session_state.total_counter}")

    image_paths = [
        "img/Segmentkernige G..jpg",
        "img/Stabkernige G..jpg",
        "img/Monozyten.jpg",
        "img/Lymphozyten.jpg",
        "img/Basophile.jpg",
        "img/Eosinophile.jpg",
        "img/Erythroblasten.jpg",
        "img/Metamyelozyt.jpg",
        "img/Myeloblast.jpg",
        "img/Myelozyt.jpg",
        "img/Plasmazelle.jpg",
        "img/Promyelozyt.jpg",
        "img/Unbekannt.jpg",
    ]

    # Define labels and colors
    labels = [
        "Segmentkernige G.", "Stabkernige G.", "Monozyten", "Lymphozyten", "Basophile", "Eosinophile",
        "Erythroblasten", "Metamyelozyt", "Myeloblast", "Myelozyt", "Plasmazelle", "Promyelozyt", "Unbekannt"
    ]
    colors = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b",
        "#e377c2", "#7f7f7f", "#bcbd22", "#17becf", "#aec7e8", "#ffbb78", "#98df8a"
    ]

    # Create UI elements for each cell type
    for i, (label, image_path) in enumerate(zip(labels, image_paths)):
        if i % 6 == 0:
            cols = st.columns(6)
        with cols[i % 6]:
            if st.session_state.total_counter < 200:  # Added to limit counting
                img = Image.open(image_path)
                st.image(img.resize((100, 100)), caption=label, use_column_width=True)
                if st.button(f"Zähle {label}"):
                    increment_counter(i)
                st.markdown(f"<div style='text-align:center; font-size:12px;'>Zähler: {st.session_state.box_counters[i]}</div>", unsafe_allow_html=True)

    if st.button("Letzten Klick rückgängig machen"):
        undo_last_click()

    if st.session_state.total_counter >= 200:
        st.markdown("Ziel erreicht!")
        st.button("Daten speichern", on_click=save_data)  # Added to save data manually

with tab3:
    st.header("Resultate")
    total = st.session_state.total_counter
    percentages = [count / total * 100 if total > 0 else 0 for count in st.session_state.box_counters]

    fig = go.Figure(data=[go.Pie(labels=labels, values=percentages, hole=0.4, textinfo='percent', marker=dict(colors=colors))])
    fig.update_layout(title_text="Prozentualer Anteil der Klicks")

    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Referenzliste")
    reference_values = {
        "Segmentkernige G.": 60,
        "Stabkernige G.": 3,
        "Monozyten": 6,
        "Lymphozyten": 30,
        "Basophile": 1,
        "Eosinophile": 2,
        "Erythroblasten": 0,
        "Metamyelozyt": 0.5,
        "Myeloblast": 0,
        "Myelozyt": 0.5,
        "Plasmazelle": 0,
        "Promyelozyt": 0,
        "Unbekannt": 0
    }

    fig_ref = go.Figure(data=[go.Pie(labels=list(reference_values.keys()), values=list(reference_values.values()), hole=0.4, textinfo='percent', marker=dict(colors=colors))])
    fig_ref.update_layout(title_text="Referenzwerte der Zelltypen")

    st.plotly_chart(fig_ref, use_container_width=True)

with tab4:
    st.header("Informationen")
    st.markdown("""
    ### Anwendung für den WBC-Counter 
    Diese App ermöglicht die Zählung und Speicherung von verschiedenen Typen weisser Blutkörperchen. 
    Die erfassten Daten können anschliessend visualisiert und mit Referenzwerten verglichen werden.

    #### Nutzung der App:
    1. Probeninformationen eingeben: Geben Sie die erforderlichen Probeninformationen in der Seitenleiste ein.
    2. Zellen zählen: Klicken Sie auf die entsprechenden Buttons, um die verschiedenen Zelltypen zu zählen.
    3. Ergebnisse ansehen: Die Ergebnisse können im Tab "Resultate" visualisiert werden.
    4. Referenzwerte: Im Tab "Referenzliste" können Sie die Referenzwerte für die verschiedenen Zelltypen einsehen.
    5. Daten speichern: Wenn die Zählung abgeschlossen ist, können die Daten gespeichert werden.

    #### Hinweise:
    - Die Zählung wird bei 200 Zellen automatisch gespeichert.
    - Sie können den letzten Klick rückgängig machen, indem Sie auf den entsprechenden Button klicken.
    - Stellen Sie sicher, dass alle Probeninformationen korrekt eingegeben wurden, bevor Sie die Daten speichern.
    """)

with tab5:
    st.header("Leukozyten")
    st.subheader("Segmentkernige Granulozyten")
    st.write("Die Segmentkernigen Neutrophilen sind granuläre Zellen mit einem mehrteiligen Kern und einer leicht rosafarbenen bis neutralen Zytoplasmafarbe. Sie sind normalerweise die zahlreichsten Leukozyten im Blutkreislauf.")

    st.subheader("Stabkernige Granulozyten")
    st.write("Die Stabkernigen Neutrophilen ähneln den Segmentkernigen Neutrophilen, jedoch ist ihr Kern in der Regel länglich und nicht in mehrere Segmente unterteilt.")
    
    st.subheader("Basophile Leukozyten")
    st.write("Basophile Leukozyten sind ebenfalls granuläre Zellen, jedoch sind ihre Granula aufgrund ihrer hohen Dichte an entzündungsfördernden Substanzen oft dunkelblau oder violett gefärbt.")
    
    st.subheader("Eosinophile Leukozyten")
    st.write("Eosinophile Leukozyten haben granuläre Zellen, deren Granula eine charakteristische rote bis orange Farbe haben. Der Kern ist oft bilobulär und gut sichtbar.")
    
    st.subheader("Monozyten")
    st.write("Monozyten sind große Zellen mit einem unregelmäßig geformten Kern und einem bläulich-grauen Zytoplasma. Sie können variabel in ihrer Größe sein und haben eine gewisse Ähnlichkeit mit Makrophagen.")
    
    st.subheader("Vorstufen der Granulozyten")
    st.write("Die Vorstufen der Granulozyten gehören zu den unreifen Zellen im Knochenmark, die sich zu den verschiedenen Arten von Granulozyten entwickeln.")
    st.write("Diese Vorläuferzellen umfassen Myeloblasten, Promyelozyten, Myelozyten und Metamyelozyten.")
    st.write("Myeloblasten sind die frühesten erkennbaren Vorläuferzellen der Granulozyten und sind große Zellen mit einem hohen Kern-zu-Zytoplasma-Verhältnis und einem unregelmäßig geformten Kern.")
    st.write("Promyelozyten haben einen größeren Kern als Myeloblasten und beginnen, spezifische Granula im Zytoplasma zu entwickeln.")
    st.write("Myelozyten haben einen runden bis ovalen Kern und ihr Zytoplasma ist zunehmend granulär, wobei die Granula spezifischer und deutlicher werden.")
    st.write("Metamyelozyten sind fast vollständig differenzierte Vorläuferzellen mit einem leicht segmentierten Kern und einem Zytoplasma, das reich an spezifischen Granula ist.")
    
    st.subheader("Weitere wichtige Leukozyten")
    st.write("Neben den genannten Leukozyten spielen auch Erythroblasten eine wichtige Rolle im Körper.")
    st.write("Sie sind die Vorläufer der roten Blutkörperchen und werden im Knochenmark gebildet. Rote Blutkörperchen sind entscheidend für den Sauerstofftransport im Körper.")
    st.write("Plasmazellen sind spezialisierte Zellen des Immunsystems, die Antikörper produzieren. Diese Antikörper sind wichtig für die Erkennung und Neutralisierung von Krankheitserregern.")

    st.markdown("[Link zu Erythrozyt im Flexikon](https://flexikon.doccheck.com/de/Leukozyt)")
