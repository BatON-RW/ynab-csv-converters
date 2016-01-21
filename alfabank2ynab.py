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


def define_ynab_category(category):
    return category


def parse_date(date):
    date = datetime.datetime.strptime(date, '%d.%m.%Y')
    return date.strftime('%d/%m/%Y')


def parse_amount(amount_in, amount_out):
    y_in = decimal.Decimal(amount_in.replace(' ', '')) if len(amount_in) > 0 else 0
    y_out = -decimal.Decimal(amount_out.replace(' ', '')) if len(amount_out) > 0 else 0
    return y_in, y_out


def parse_row(row):
    y_date = parse_date(row[0])
    y_in, y_out = parse_amount(row[4], row[5])
    y_payee = ""
    y_category = define_ynab_category("")
    y_memo = row[3]

    return [y_date, y_payee, y_category, y_memo, y_out, y_in]


with open(sys.argv[1], 'r', encoding='utf-8') as csvin, open("ynab-%s" % (sys.argv[1], ), 'w', encoding='utf-8') as csvout:
    reader = csv.reader(csvin, delimiter=';', quotechar='"')
    writer = csv.writer(csvout, delimiter=',', quotechar='"', lineterminator='\n')

    writer.writerow(['Date', 'Payee', 'Category', 'Memo', 'Outflow', 'Inflow'])

    next(reader)  # skip a CSV header row
    for row in reader:
        writer.writerow(parse_row(row))
