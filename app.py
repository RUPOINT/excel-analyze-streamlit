import streamlit as st
import pandas as pd
from io import BytesIO
from extract_process_hide import process_excel
from extract_stage2 import process_excel_stage2
from extract_stage3 import process_excel_stage3    # <--- Добавили импорт этапа 3

st.title("Обработка Excel — этап 1, этап 2 и этап 3")

uploaded_file = st.file_uploader("Загрузите Excel-файл", type=["xlsx", "xls"])

if 'df1' not in st.session_state:
    st.session_state.df1 = None
if 'df2' not in st.session_state:
    st.session_state.df2 = None
if 'df3' not in st.session_state:
    st.session_state.df3 = None

# --- Этап 1 ---
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    if st.button("Обработать этап 1"):
        st.session_state.df1 = process_excel(df)
        st.session_state.df2 = None  # сбросить второй этап при новом запуске
        st.session_state.df3 = None  # сбросить третий этап при новом запуске

# --- Этап 1 — результат и переход к этапу 2 ---
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
        st.session_state.df3 = None  # сбросить третий этап при запуске второго

# --- Этап 2 — результат и переход к этапу 3 ---
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
    if st.button("Обработать этап 3"):
        st.session_state.df3 = process_excel_stage3(st.session_state.df2)

# --- Этап 3 — результат и финальная выгрузка ---
if st.session_state.df3 is not None:
    st.success("Этап 3 завершён! (дубли по ИНН убраны)")
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

