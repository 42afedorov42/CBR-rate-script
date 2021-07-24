#!/usr/bin/python3
from xml.dom import minidom
import urllib.request
import argparse
import datetime
import csv
import time
from progress.bar import Bar


def main():
    '''Create and write report with rate and currency. Adding status bar'''
    date_create = datetime.datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
    xml_url_template = 'https://www.cbr.ru/scripts/XML_daily.asp?date_req='
    create_report(date_create)
    bar = Bar('Parse:', max=len(date_range()))
    for date in date_range():
        date_rate = date.strftime("%Y-%m-%d")
        date_url = date.strftime("%Y-%m-%d")
        xml_url = f'{xml_url_template}{date_url}'
        data = read_xml(xml_url)
        currency_dict = parse_data(data)
        write_report(currency_dict, date_create, date_rate)
        bar.next()
        time.sleep(0.01)
    bar.finish()
    return None


def create_report(date_create):
    '''Create csv file for rate export'''
    with open(f'currency_{date_create}.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['date', 'currency_code', 'rate'])
        return None


def date_range():
    '''Get date range from argparse'''
    parser = argparse.ArgumentParser()
    parser.add_argument("date_range", help="Example: \
                        python3 cbr-rate.py 08/09/2019-12/12/2019")
    args = parser.parse_args()
    date_range_arg = (args.date_range.split('-'))
    start_date = date_range_arg[0]
    end_date = date_range_arg[1]
    start = datetime.datetime.strptime(start_date, "%Y/%m/%d")
    end = datetime.datetime.strptime(end_date, "%Y/%m/%d") + datetime.timedelta(days=1)
    date_range = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    return date_range


def read_xml(xml_url):
    '''Read xml from url cbr'''
    try:
        web_file = urllib.request.urlopen(xml_url)
        data = web_file.read()
        return data
    except:
        pass


def parse_data(data):
    '''Parsing rate and currency from xml cbr'''
    dom = minidom.parseString(data)
    dom.normalize()
    elements = dom.getElementsByTagName("Valute")
    currency_dict = {}
    for node in elements:
        for child in node.childNodes:
            if child.nodeType == 1:
                if child.tagName == 'Value':
                    if child.firstChild.nodeType == 3:
                        value = round(float(child.firstChild.data.replace(',', '.')), 4)
                if child.tagName == 'CharCode':
                    if child.firstChild.nodeType == 3:
                        char_code = child.firstChild.data
        currency_dict[char_code] = value
    return currency_dict


def write_report(currency_dict, date_create, date_rate):
    '''Write xml parsing result to csv file''' 
    with open(f'currency_{date_create}.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        for char_code, rate in currency_dict.items():
            writer.writerow([date_rate, char_code, rate])


if __name__ == "__main__":
    main()
