#!/usr/bin/env python3
# coding: utf-8

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import csv
import datetime
import decimal
import json
import os
import argparse

DEFAULT_CATEGORIES_FILE = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'categories.json'
DEFAULT_BANK_IN_FILE = 'tinkoff.csv'
DEFAULT_BANK_OUT_FILE = 'yanb-' + DEFAULT_BANK_IN_FILE

parser = argparse.ArgumentParser(description="CSV converter from tinkoff data format to ynab.")
parser.add_argument('-c', '--categories', type=str, default=DEFAULT_CATEGORIES_FILE, help="path to categories dictionary file")
parser.add_argument('-i', '--csv_file_in', type=str, default=DEFAULT_BANK_IN_FILE, help="path to input CSV file")
parser.add_argument('-o', '--csv_file_out', type=str, default=DEFAULT_BANK_OUT_FILE, help="path to output CSV file")
args = parser.parse_args()


def define_ynab_category(category):
    try:
        with open(args.categories, 'r', encoding='utf-8') as categories:
            dictionary = json.load(categories)
    except Exception as err:
        print('ERROR: %s' % err)
        print('WARNING: Categories was not loaded!')
        dictionary = {}

    return dictionary[category] if dictionary.get(category) else category


def parse_date(date):
    date = datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
    return date.strftime('%d/%m/%Y')


def parse_amount(amount):
    amount = decimal.Decimal(amount.replace(',', '.'))
    y_in, y_out = (amount, 0) if amount > 0 else (0, -amount)
    return y_in, y_out


def parse_row(row):
    y_date = parse_date(row[0])
    y_in, y_out = parse_amount(row[6])
    y_payee = row[10]
    y_category = define_ynab_category(row[8])
    y_memo = ''

    return [y_date, y_payee, y_category, y_memo, y_out, y_in]


try:
    with open(args.csv_file_in, 'r', encoding='cp1251') as csvin, open(args.csv_file_out, 'w', encoding='utf-8') as csvout:
        reader = csv.reader(csvin, delimiter=';', quotechar='"')
        writer = csv.writer(csvout, delimiter=',', quotechar='"', lineterminator='\n')

        writer.writerow(['Date', 'Payee', 'Category', 'Memo', 'Outflow', 'Inflow'])

        for row in reader:
            writer.writerow(parse_row(row))
except Exception as er:
    print('ERROR: %s' % er)
