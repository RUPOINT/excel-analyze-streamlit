import streamlit as st
import pandas as pd
from io import BytesIO
from extract_process_hide import process_excel
from extract_stage2 import process_excel_stage2
from extract_stage3 import process_excel_stage3   # <- Добавь этот импорт

st.title("Обработка Excel — этап 1, этап 2, этап 3")

uploaded_file = st.file_uploader("Загрузите Excel-файл", type=["xlsx", "xls"])

if 'df1' not in st.session_state:
    st.session_state.df1 = None
if 'df2' not in st.session_state:
    st.session_state.df2 = None
if 'df3' not in st.session_state:
    st.session_state.df3 = None

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    if st.button("Обработать этап 1"):
        st.session_state.df1 = process_excel(df)
        st.session_state.df2 = None
        st.session_state.df3 = None   # <--- сброс третьего этапа при новом запуске

if st.session_state.df1 is not None:
    st.success("Этап 1 завершён!")
    st.dataframe(st.session_state.df1)
    output1 = BytesIO()
    st.session_state.df1.to_excel(output1, index=False)
    output1.seek(0)
    st.download_button(
        label="Скачать результат этапа 1",
        data=output1,
        file_name="result_etap1.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    st.markdown("---")
    if st.button("Обработать этап 2"):
        st.session_state.df2 = process_excel_stage2(st.session_state.df1)
        st.session_state.df3 = None  # сбросить этап 3

if st.session_state.df2 is not None:
    st.success("Этап 2 завершён! (только выбранные колонки)")
    st.dataframe(st.session_state.df2)
    output2 = BytesIO()
    st.session_state.df2.to_excel(output2, index=False)
    output2.seek(0)
    st.download_button(
        label="Скачать результат этапа 2",
        data=output2,
        file_name="result_etap2.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    st.markdown("---")
    # ----------- ЭТАП 3 ----------------
    if st.button("Обработать этап 3"):
        st.session_state.df3 = process_excel_stage3(st.session_state.df2)

if st.session_state.df3 is not None:
    st.success("Этап 3 завершён! (удалены дубликаты по ИНН)")
    st.dataframe(st.session_state.df3)
    output3 = BytesIO()
    st.session_state.df3.to_excel(output3, index=False)
    output3.seek(0)
    st.download_button(
        label="Скачать результат этапа 3",
        data=output3,
        file_name="result_etap3.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
