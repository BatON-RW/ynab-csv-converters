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
import sys
import decimal
import json


def define_ynab_category(category):
    try:
        dict_file = 'categories.json' if len(sys.argv) != 3 else sys.argv[2]
        with open(dict_file, 'r', encoding='utf-8') as categories:
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


with open(sys.argv[1], 'r', encoding='cp1251') as csvin, open("ynab-%s" % (sys.argv[1], ), 'w', encoding='utf-8') as csvout:
    reader = csv.reader(csvin, delimiter=';', quotechar='"')
    writer = csv.writer(csvout, delimiter=',', quotechar='"', lineterminator='\n')

    writer.writerow(['Date', 'Payee', 'Category', 'Memo', 'Outflow', 'Inflow'])

    for row in reader:
        writer.writerow(parse_row(row))
