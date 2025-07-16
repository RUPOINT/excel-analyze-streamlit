import requests
import time

def get_site_dadata(inn, token):
    url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party"
    headers = {"Authorization": f"Token {token}"}
    data = {"query": inn}
    try:
        resp = requests.post(url, json=data, headers=headers, timeout=10)
        if resp.status_code == 200:
            suggestions = resp.json().get('suggestions', [])
            if suggestions:
                # Обычно сайт в "data"->"contact"->"email/website"
                site = suggestions[0]['data'].get('contact', {}).get('website')
                if not site:
                    # Попробуй management или state если нужно (редко бывает)
                    site = suggestions[0]['data'].get('management', {}).get('website')
                if not site:
                    site = suggestions[0]['data'].get('state', {}).get('website')
                return site
    except Exception as e:
        print(f"Dadata error: {e}")
    return None

def get_site_kontur(inn, token):
    url = f"https://focus-api.kontur.ru/api3/req?inn={inn}&key={token}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list) and len(data) > 0:
                site = data[0].get('СвОбрЮЛ', {}).get('СвУчетНО', {}).get('@Сайт')
                if not site:
                    site = data[0].get('website')
                return site
    except Exception as e:
        print(f"Kontur error: {e}")
    return None

def get_site_fns(inn, token):
    url = f"https://api-fns.ru/api/search?q={inn}&key={token}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            js = resp.json()
            items = js.get('items', [])
            if items and isinstance(items, list):
                org = items[0]
                site = org.get('site') or org.get('сайт') or org.get('СвОКВЭД', {}).get('website')
                return site
    except Exception as e:
        print(f"FNS error: {e}")
    return None

def find_company_site(inn, dadata_token, kontur_token, fns_token):
    for func, name in [
        (get_site_dadata, 'dadata'),
        (get_site_kontur, 'kontur'),
        (get_site_fns, 'fns'),
    ]:
        token = dadata_token if name == 'dadata' else kontur_token if name == 'kontur' else fns_token
        site = func(inn, token)
        if site:
            return site
        time.sleep(0.3)
    return None

def process_excel_stage4(df, dadata_token, kontur_token, fns_token):
    sites = []
    for idx, inn in enumerate(df["G141 (ИНН декларанта)"]):
        if pd.isna(inn):
            sites.append(None)
            continue
        site = find_company_site(str(inn), dadata_token, kontur_token, fns_token)
        sites.append(site)
        # Можно выводить прогресс
        print(f"Искал сайт для ИНН {inn}: {site}")
    df['Сайт компании'] = sites
    return df
