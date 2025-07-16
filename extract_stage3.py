import pandas as pd

def process_excel_stage3(df):
    inn_col = "G141 (ИНН декларанта)"
    if inn_col in df.columns:
        # Удаляем дубликаты по ИНН, оставляем только первую встречающуюся строку
        df_unique = df.drop_duplicates(subset=[inn_col], keep="first").reset_index(drop=True)
        return df_unique
    else:
        # Если колонки нет — возвращаем как есть
        return df
