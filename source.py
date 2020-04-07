import pdfminer
import io
import os
from collections import OrderedDict

import requests
import urllib.request
import time
from bs4 import BeautifulSoup

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

import pandas as pd


def download_covid_pdfs():
    """Download all new (which not present in "data" directory) PDFs files 
    from Google Community Mobility Reports to the "data" directory
    """
    url = 'https://www.google.com/covid19/mobility/'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    new_files = False

    if not os.path.exists('data'):
        os.makedirs('data')

    for one_a_tag in soup.findAll('a', {"class": "download-link"}):
        link = one_a_tag['href']
        file_name = link[link.find('mobility') + len('mobility') + 1:]
        path = 'data/' + file_name
        if not os.path.isfile(path):
            new_files = True
            urllib.request.urlretrieve(link, path)
            print(file_name)
            time.sleep(1)
    if not new_files:
        print('No updates')
    return new_files


def extract_text_from_pdf(pdf_path):
    """Extract raw text from PDF file"""
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()
    # close open handles
    converter.close()
    fake_file_handle.close()

    if text:
        return text


def parse_covid_report(text, regions=False):
    """Create an Ordered dictionary which parsed from the text of PDF report.
    text - parsed text from PDF report
    regions - True: parse with details by regions; False: parse only total data
    """
    data = OrderedDict()
    attributes = ('Retail & recreation', 'Grocery & pharmacy',
                  'Parks', 'Transit stations',
                  'Workplaces', 'Residential')
    if not regions:
        for i in range(len(attributes)):
            index = text.find(attributes[i]) + len(attributes[i])
            if text[index] != ' ':
                data[attributes[i]] = int(
                    text[index:index + text[index:].find('%')])
            else:
                data[attributes[i]] = None

    else:
        data['Region'] = ['Total']
        for i in range(len(attributes)):
            index = text.find(attributes[i]) + len(attributes[i])
            if text[index] != ' ':
                data[attributes[i]] = data.get(
                    attributes[i], []) + [int(text[index:index + text[index:].find('%')])]
            else:
                data[attributes[i]] = data.get(attributes[i], []) + [None]

        last_index = text.find(attributes[len(attributes) - 1])

        while True:
            # Parsing region details
            if text[last_index + 1:].find(attributes[0]) < 0:
                break
            reg_ind = 1
            while True:
                # Parsing name of region from report
                m = text[last_index + 1:].find(attributes[0])
                region = text[last_index + 1 + m - reg_ind:last_index + 1 + m]

                xoc = region.find('\x0c')
                baseline = region.find('baseline')
                dat = region.find('date')

                if xoc >= 0:
                    region = region[xoc + 1:]
                    break
                if baseline >= 0:
                    region = region[8:]
                    break
                if dat >= 0:
                    region = region[4:]
                    break

                reg_ind += 1

            data['Region'] += [region]

            text = text[last_index +
                        text[last_index + 1:].find(attributes[0]):]

            for i in range(len(attributes)):
                # masterpiece trick, because this attribute
                # in region data provided without letter s
                if attributes[i] != 'Workplaces':
                    index = text.find(attributes[i]) + len(attributes[i])
                else:
                    index = text.find('Workplace') + len('Workplace')

                if text[index:index + 2] != ' N':
                    if text[index] != ' ':
                        data[attributes[i]
                             ] += [int(text[index:index + text[index:].find('%')])]
                    else:
                        data[attributes[i]
                             ] += [int(text[index + 1:index + text[index:].find('%')])]
                else:
                    data[attributes[i]] += [None]

            last_index = text.find(attributes[len(attributes) - 1])

    return data


def build_covid_report_detailed(directory='data', destination='mobility_report.csv', report_type='regions'):
    """
    Build report in CSV format
    data - path of downloaded pdfs
    destination - destination file of report
    report_type: 'regions', 'US'
    """

    if os.path.isfile('codes.csv'):
        # match 2-letter abbreviation codes with countries names
        codes = pd.read_csv('codes.csv', sep=';',
                            index_col=0, keep_default_na=False)
    else:
        codes = None

    # get list of files on which current csv reports created
    files_source = []
    if not os.path.isfile('report_source.txt'):
        open('report_source.txt', 'a').close()
    else:
        with open('report_source.txt') as f:
            files_source = [line.rstrip() for line in f]

    if report_type != 'regions' and report_type != 'US':
        raise NameError(
            "Wrong report_type. Available options: 'regions', 'US_states'")

    all_data = OrderedDict()
    reg_list = []

    for filename in os.listdir(directory):
        if filename not in files_source:
            filename_list = filename.split('_')

            if report_type == 'regions':
                if len(filename_list) == 5:
                    text = extract_text_from_pdf(
                        os.path.join(directory, filename))
                    if codes is not None:
                        country_name = codes.loc[filename_list[1], 'Country'] if filename_list[1] in codes.index else \
                            filename_list[1]
                    else:
                        country_name = filename_list[1]
                else:
                    continue

            elif report_type == 'US':
                if len(filename_list) >= 6:
                    text = extract_text_from_pdf(
                        os.path.join(directory, filename))
                    country_name = filename_list[2]
                    if len(filename_list) >= 7:
                        country_name += ' ' + filename_list[3]
                    if len(filename_list) >= 8:
                        country_name += ' ' + filename_list[4]
                else:
                    continue

            parsed = parse_covid_report(text, regions=True)
            reg_name = 'Country' if report_type == 'regions' else 'State'
            reg_list.append(country_name)
            all_data['Date'] = all_data.get(
                'Date', []) + [filename_list[0] for i in range(len(parsed['Region']))]
            all_data[reg_name] = all_data.get(
                reg_name, []) + [country_name for i in range(len(parsed['Region']))]
            for k, v in parsed.items():
                all_data[k] = all_data.get(k, []) + v

            with open('report_source.txt', 'a+') as f:
                f.write("%s\n" % filename)
    df = pd.DataFrame(data=all_data)
    if not os.path.isfile(destination):
        df.to_csv(destination, index=False)
    else:
        df.to_csv(destination, index=False, mode='a', header=False)


def run():
    """Run parse flow"""
    new_files_status = download_covid_pdfs()
    new_files_status = True
    if new_files_status:
        build_covid_report_detailed(directory='data', destination='mobility_report_regions.csv',
                                    report_type='regions')
        build_covid_report_detailed(directory='data', destination='mobility_report_US.csv',
                                    report_type='US')


if __name__ == '__main__':
    run()
