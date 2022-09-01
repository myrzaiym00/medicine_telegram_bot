import json
import requests
from bs4 import BeautifulSoup as bs


def get_drug_cards(url):
    r = requests.get(url=url)
    soup = bs(r.text, 'lxml')
    page_div = soup.findAll('div', class_='ut2-gl__name')

    drug_cards = []
    for div in page_div:
        drug_cards.append(div.find('a'))
    return drug_cards


def get_all_cards():
    drugs_url = 'https://neman.kg/lekarstvennye-sredstva/'
    pages = '?page='

    all_drugs = []
    for i in range(1, 118):
        page_url = drugs_url + pages + str(i) + '/'
        drugs = get_drug_cards(page_url)
        all_drugs.extend(drugs)
    return all_drugs

def main():
    drugs_dict = {}
    all_drugs = get_all_cards()

    for drug in all_drugs:
        drug_title = drug.text
        drug_url = drug.get("href")

        drugs_dict[drug_title] = drug_url

    with open('drugs_dict.json', 'a') as file:
        json.dump(drugs_dict, file, indent=4, ensure_ascii=False)


# main()