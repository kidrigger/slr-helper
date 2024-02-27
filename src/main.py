#!python

import openpyxl as xlsx
import pathlib
import pandas as pd
import bibtexparser as bibtex
from ordered_set import OrderedSet
from functools import reduce

def read_excel(filename: str) -> pd.DataFrame:
    if pathlib.Path(filename).suffix != '.xlsx':
        raise "Not an XLSX file"
    workbook = xlsx.load_workbook(filename)
    worksheet = pd.read_excel(workbook, engine='openpyxl')
    worksheet = worksheet.rename(columns = lambda x : x.lower() if x != 'DOI_GS' else 'doi')
    worksheet = worksheet.drop_duplicates(subset=['doi'])
    return worksheet

def write_excel(filename: str, output: pd.DataFrame):
    if pathlib.Path(filename).suffix != '.xlsx':
        raise "Not an XLSX file"
    workbook = xlsx.Workbook()
    output.to_excel(filename, engine='openpyxl')
    # workbook.save(filename)

def read_bibtex(filename: str) -> pd.DataFrame:
    if pathlib.Path(filename).suffix not in ['.bib', '.bibtex']:
        raise "Not an BibTex file"
    library = bibtex.parse_file(filename)
    keys = map(lambda e: OrderedSet(e.fields_dict.keys()), library.entries)
    keys = list(reduce(lambda a, b: a.union(b), keys, OrderedSet()))
    keys.append('entry_type')
    df = pd.DataFrame(columns=keys, dtype=str)
    for i, entry in enumerate(library.entries):
        fields = dict([(f.key, f.value) for f in entry.fields])
        fields['entry_type'] = entry['type']
        df.loc[i, list(fields.keys())] = list(fields.values())
    df = df.drop_duplicates(subset=['doi'])
    return df

def parse_scholar(query: str) -> pd.DataFrame:
    from bs4 import BeautifulSoup
    import requests
    import urllib
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'}
    query = urllib.parse.quote_plus(query, safe='')
    url = f'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={query}&btnG=&pass='
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html')

    for item in soup.select('[data-lid]'):
        try:
            print('------------------')
            print(item.select('h3')[0].get_text())
        except Exception as e:
            pass



def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-g','--gs', metavar='GOLDEN_STD', type=str)
    parser.add_argument('-i', '--input', metavar='INPUT_XLSX', type=str)
    parser.add_argument('-o', '--output', metavar='OUTPUT_XLSX', type=str)

    args = parser.parse_args()

    gs = read_excel(args.gs)
    rs = read_bibtex(args.input)

    out = gs.copy()
    out.loc[:, 'in_result'] = gs.doi.isin(rs.doi).values
    write_excel(args.output, out)

if __name__ == '__main__':
    main()
