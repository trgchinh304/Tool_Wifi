import requests, sys
from deep_translator import GoogleTranslator

def get_data_nation(*, nation: str, lang: str):
    try:
        def translate_keyword(keyword):
            return GoogleTranslator(source='auto', target=lang).translate(keyword)
        api = f"https://restcountries.com/v3.1/name/{nation}"
        response = requests.get(api)
        if response.status_code == 200:
            countries = response.json()
            for country in countries:
                if country['name']['common'].lower() == nation.lower():
                    name = country['name']['common']
                    official_name = country['name']['official']
                    capital = country.get('capital', ['N/A'])[0]
                    region = country.get('region', 'N/A')
                    population = country.get('population', 'N/A')
                    timezones = ', '.join(country.get('timezones', []))
                    area = country.get('area', 'N/A')
                    languages = ', '.join(country.get('languages', {}).values())
                    currencies = ', '.join([f"{cur['name']} ({cur['symbol']})" for cur in country.get('currencies', {}).values()])
                    flag = country.get('flags', {}).get('png', 'N/A')
                    coordinates = country.get('latlng', 'N/A')
                    alpha2_code = country.get('cca2', 'N/A')
                    alpha3_code = country.get('cca3', 'N/A')
                    borders = ', '.join(country.get('borders', ['None']))
                    country_domain = ', '.join(country.get('tld', []))
                    demonym = country.get('demonym', 'N/A')
                    government = country.get('government', 'N/A')
                    independent = country.get('independent', 'N/A')
                    independent = "Yes" if independent == True else "No" if independent == False else independent
                    un_member = country.get('unMember', 'N/A')
                    un_member = "Yes" if un_member == True else "No" if un_member == False else un_member
                    country_label = translate_keyword("Country")
                    official_name_label = translate_keyword("Official Name")
                    capital_label = translate_keyword("Capital")
                    government_label = translate_keyword("Government")
                    independent_label = translate_keyword("Independence")
                    un_member_label = translate_keyword("UN Membership")
                    region_label = translate_keyword("Region")
                    population_label = translate_keyword("Population")
                    timezones_label = translate_keyword("Timezones")
                    area_label = translate_keyword("Area")
                    languages_label = translate_keyword("Languages")
                    currencies_label = translate_keyword("Currencies")
                    alpha2_code_label = translate_keyword("Alpha-2 Code")
                    alpha3_code_label = translate_keyword("Alpha-3 Code")
                    coordinates_label = translate_keyword("Coordinates")
                    borders_label = translate_keyword("Borders")
                    country_domain_label = translate_keyword("Country Domain")
                    info = (
                        f"\n"
                        f"┌ {country_label}: {name}\n"
                        f"├ {official_name_label}: {official_name}\n"
                        f"├ {capital_label}: {capital}\n"
                        f"├ {government_label}: {government}\n"
                        f"├ {independent_label}: {independent}\n"
                        f"├ {un_member_label}: {un_member}\n"
                        f"├ {region_label}: {region}\n"
                        f"├ {population_label}: {population}\n"
                        f"├ {timezones_label}: {timezones}\n"
                        f"├ {area_label}: {area} km²\n"
                        f"├ {languages_label}: {languages}\n"
                        f"├ {currencies_label}: {currencies}\n"
                        f"├ {alpha2_code_label}: {alpha2_code}\n"
                        f"├ {alpha3_code_label}: {alpha3_code}\n"
                        f"├ {coordinates_label}: {coordinates}\n"
                        f"├ {borders_label}: {borders}\n"
                        f"└ {country_domain_label}: {country_domain.upper()}\n"
                    )
                    return info
            return None  
        else:
            return None
    except Exception as e:
        return str(e)

def input_nation():
    while True:
        try:
            user_input = input("Nhập theo mẫu: /[tên_quốc_gia] [mã_ngôn_ngữ] (VD: /Vietnam vi): ").strip()
            if not user_input.startswith('/'):
                print("Bắt đầu bằng dấu `/`. Ví dụ: /Vietnam vi")
                continue
            parts = user_input[1:].rsplit(maxsplit=1)  
            if len(parts) != 2:
                print("Sai định dạng. Nhập theo ví dụ: /Vietnam vi")
                continue
            nation = parts[0].replace('%20', ' ')
            lang = parts[1].strip().lower()
            print(get_data_nation(nation = nation, lang = lang))
        except Exception as e:
            print(f"Lỗi: {e}")
            break

if __name__ == '__main__':            
    input_nation()
    
# print(nation(nation="Vietnam", lang="zh-CN"))
