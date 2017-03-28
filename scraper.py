from bs4 import BeautifulSoup
import urllib.request
import csv

# soup = BeautifulSoup()
tax_data = urllib.request.urlopen(urllib.request.Request('https://www.columbus.gov/tax/PrintAllMunis.aspx'))

soup = BeautifulSoup(tax_data.read().decode('utf-8'), 'html.parser')

final_data = []

def fix_stupid_fractions(rate):
  if rate.find('/') > -1:
    numbers = rate.split(' of ')
    fraction = numbers[0].split('/')
    return format((float(fraction[0]) / float(fraction[1])) / 100, '.6f').rstrip('0').rstrip('.')
  else:
    return format(float(rate) / 100, '.6f').rstrip('0').rstrip('.')

addresses = soup.find_all('td', {'class': 'mucip_cont_address'})
for address in addresses:
  text = address.get_text()
  split_text = text.split('\n')
  muni_name = split_text[1].strip()

  univ_file = address.find_next('td', {'class': 'mucip_cont_col3'}).get_text().strip()
  tax_rate = fix_stupid_fractions(address.find_next('td', {'class': 'mucip_cont_col5'})
    .find_next('td', {'class': 'mucip_cont_title'})
    .find_next('td')
    .get_text().strip()[:-1])
  rate_date = address.find_next('td', {'class': 'mucip_cont_col5'}).get_text().strip()
  tax_credit = fix_stupid_fractions(address.find_next('td', {'class': 'mucip_cont_col5'})
    .find_next('td', {'class': 'mucip_cont_title'})
    .find_next('td', {'class': 'mucip_cont_title'})
    .find_next('td')
    .get_text().strip()[:-1])
  credit_limit = fix_stupid_fractions(address.find_next('td', {'class': 'mucip_cont_col5'})
    .find_next('td', {'class': 'mucip_cont_title'})
    .find_next('td', {'class': 'mucip_cont_title'})
    .find_next('td', {'class': 'mucip_cont_title'})
    .find_next('td')
    .get_text().strip()[:-1])

  final_data.append({
    'name': muni_name,
    'univ_file': univ_file,
    'tax_rate': tax_rate,
    'rate_date': rate_date,
    'tax_credit': tax_credit,
    'credit_limit': credit_limit
  })

with open('ohio-data.csv', 'w') as csvfile:
  fieldnames = ['name', 'univ_file', 'tax_rate', 'rate_date', 'tax_credit', 'credit_limit']
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  writer.writeheader()
  for row in final_data:
    writer.writerow(row)