import streamlit as st
import pandas as pd
from io import BytesIO
from extract_process_hide import process_excel

st.title("Обработка Excel — этап 1")

uploaded_file = st.file_uploader("Загрузите Excel-файл", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    if st.button("Обработать этап 1"):
        df_processed = process_excel(df)
        st.success("Этап 1 завершён!")
        st.dataframe(df_processed)

        # Готовим Excel для скачивания
        output = BytesIO()
        df_processed.to_excel(output, index=False)
        output.seek(0)

        st.download_button(
            label="Скачать результат",
            data=output,
            file_name="result_etap1.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
