import pandas as pd
import re

def extract_contacts(text):
    if not isinstance(text, str):
        return ""
    tel_match = re.search(r"Тел:[^|\n]*", text)
    email_match = re.search(r"Email:[^|\n]*", text)
    parts = []
    if tel_match:
        parts.append(tel_match.group().strip())
    if email_match:
        parts.append(email_match.group().strip())
    return " | ".join(parts)

def process_excel(df):
    try:
        if df is None or df.empty:
            print("Входящий DataFrame пустой!")
            return df

        # Проверка, достаточно ли столбцов для выполнения операции
        if len(df.columns) < 3:
            print("Недостаточно столбцов для объединения!")
            return df

        df = df.drop(columns=[col for col in df.columns if "грузовых мест" in col], errors='ignore')
        df = df.drop_duplicates(subset=["ND (Номер декларации)"], keep=False)

        second_col, third_col = df.columns[1], df.columns[2]
        df["Перемещение + Режим"] = df[second_col].astype(str) + " / " + df[third_col].astype(str)
        df = df.drop(columns=[second_col, third_col])

        declarant_col = "G142 (Наименование декларанта)"
        if declarant_col in df.columns:
            df[declarant_col] = df[declarant_col].astype(str).str.replace("<", '"').str.replace(">", '"')

            nd_col = "ND (Номер декларации)"
            decl_count = df.groupby(declarant_col)[nd_col].nunique().reset_index()
            decl_count.columns = [declarant_col, "Декларант — количество деклараций"]
            df = df.merge(decl_count, on=declarant_col, how="left")

            broker_col = "G541 (Номер свидетельства брокера)"
            df[broker_col] = df[broker_col].fillna("А")

            count_A = df[df[broker_col] == "А"].groupby(declarant_col)[broker_col].count().reset_index()
            count_A.columns = [declarant_col, "Пустые ячейки в колонке брокера"]
            df = df.merge(count_A, on=declarant_col, how="left")
            df["Пустые ячейки в колонке брокера"] = df["Пустые ячейки в колонке брокера"].fillna(0).astype(int)

            broker_count = df[df[broker_col] != "А"].groupby(declarant_col)[broker_col].nunique().reset_index()
            broker_count.columns = [declarant_col, "Количество брокеров"]
            df = df.merge(broker_count, on=declarant_col, how="left")
            df["Количество брокеров"] = df["Количество брокеров"].fillna(0).astype(int)

        if "FIRM (Доп.информация о контрактодержателе (Росстат))" in df.columns:
            df["Контакты"] = df["FIRM (Доп.информация о контрактодержателе (Росстат))"].apply(extract_contacts)

        # Удаляем F, G по индексу
        cols_to_drop = []
        if len(df.columns) > 5:
            cols_to_drop.append(df.columns[5])
        if len(df.columns) > 6:
            cols_to_drop.append(df.columns[6])
        df = df.drop(columns=cols_to_drop, errors="ignore")

        # Удаляем по названиям
        df = df.drop(columns=[
            "G541 (Номер свидетельства брокера)",
            "FIRM (Доп.информация о контрактодержателе (Росстат))"
        ], errors="ignore")

        return df

    except Exception as e:
        print("Ошибка при обработке:", e)
        raise
