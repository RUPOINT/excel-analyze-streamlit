import streamlit as st
import pandas as pd
from io import BytesIO
from extract_process_hide import process_excel      # этап 1
from extract_stage2 import process_excel_stage2      # этап 2

st.title("Обработка Excel: Этап 1 и Этап 2")

uploaded_file = st.file_uploader("Загрузите исходный Excel-файл", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Этап 1 — обработка
    if st.button("Обработать этап 1"):
        df1 = process_excel(df)
        st.success("Этап 1 завершён!")
        st.dataframe(df1)
        # Кнопка скачать этап 1
        output1 = BytesIO()
        df1.to_excel(output1, index=False)
        output1.seek(0)
        st.download_button(
            label="Скачать результат этапа 1",
            data=output1,
            file_name="result_etap1.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # Этап 2 — сразу после этапа 1
        st.markdown("---")
        st.subheader("Этап 2: Оставить только выбранные колонки")
        if st.button("Обработать этап 2"):
            df2 = process_excel_stage2(df1)
            st.success("Этап 2 завершён!")
            st.dataframe(df2)
            # Кнопка скачать этап 2
            output2 = BytesIO()
            df2.to_excel(output2, index=False)
            output2.seek(0)
            st.download_button(
                label="Скачать результат этапа 2",
                data=output2,
                file_name="result_etap2.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
