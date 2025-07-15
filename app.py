import streamlit as st
import pandas as pd
from io import BytesIO
from extract_process_hide import process_excel      # этап 1
from extract_stage2 import process_excel_stage2     # этап 2

st.title("Обработка Excel: Этап 1 и Этап 2")

uploaded_file = st.file_uploader("Загрузите исходный Excel-файл", type=["xlsx", "xls"])

if 'df1' not in st.session_state:
    st.session_state.df1 = None
if 'df2' not in st.session_state:
    st.session_state.df2 = None

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    if st.button("Обработать этап 1"):
        df1 = process_excel(df)
        st.session_state.df1 = df1
        st.success("Этап 1 завершён!")
        st.dataframe(df1)

        output1 = BytesIO()
        df1.to_excel(output1, index=False)
        output1.seek(0)
        st.download_button(
            label="Скачать результат этапа 1",
            data=output1,
            file_name="result_etap1.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# --- Теперь этап 2 виден всегда после этапа 1! ---
if st.session_state.df1 is not None:
    st.markdown("---")
    st.subheader("Этап 2: Оставить только выбранные колонки")
    if st.button("Обработать этап 2"):
        df2 = process_excel_stage2(st.session_state.df1)
        st.session_state.df2 = df2
        st.success("Этап 2 завершён!")
        st.dataframe(df2)

        output2 = BytesIO()
        df2.to_excel(output2, index=False)
        output2.seek(0)
        st.download_button(
            label="Скачать результат этапа 2",
            data=output2,
            file_name="result_etap2.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
