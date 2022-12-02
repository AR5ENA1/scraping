import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from pprint import pprint
import unicodedata
import json


def search_jobs(url):
    next_page = 1
    count = 1
    count2 = 0
    while count2 != 5:
        html = requests.get(f'{url}', headers=headers.generate())
        bs = BeautifulSoup(html.content, features='html.parser')
        teg = bs.find_all(class_="serp-item")

        try:
            next_page = bs.find(attrs={"data-qa": "pager-next"})['href']
        except TypeError:
            break
        else:
            for job_openings in teg:
                if job_openings.find(attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}) != None:
                    if 'Django' and 'Flask' in job_openings.find(
                            attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text:
                        vacancy = job_openings.find(class_='serp-item__title').text
                        vacancy_website = job_openings.find(class_='serp-item__title')['href']
                        vacancy_compensation = job_openings.find(
                            attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
                        if vacancy_compensation != None:
                            vacancy_compensation = unicodedata.normalize("NFKC", vacancy_compensation.text)
                        else:
                            vacancy_compensation = 'Отсутствует'
                        vacancy_company = unicodedata.normalize("NFKC",
                                                                job_openings.find(
                                                                    class_='vacancy-serp-item__meta-info-company').text)
                        vacancy_city = unicodedata.normalize("NFKC",
                                                             job_openings.find(
                                                                 attrs={
                                                                     'data-qa': "vacancy-serp__vacancy-address"}).text)
                        list_vacancy[f'vacancy№{count}'] = {'vacancy': vacancy,
                                                            'website': vacancy_website,
                                                            'compensation': vacancy_compensation,
                                                            'company': vacancy_company,
                                                            'city': vacancy_city
                                                            }
                        count += 1
            print(url)
            url = f"https://spb.hh.ru{next_page}"
            count2 += 1


def record_json(list_vacancy):
    with open('list_vacancy.json', 'w') as lv:
        json.dump(list_vacancy, lv,  indent=4, ensure_ascii= True)


if __name__ == '__main__':
    headers = Headers(os='win', browser='firefox', headers=True)
    url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&items_on_page=20'

    list_vacancy = {}

    search_jobs(url)
    record_json(list_vacancy)

    pprint(list_vacancy, sort_dicts=None)
