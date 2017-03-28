from bs4 import BeautifulSoup
import urllib.request

# soup = BeautifulSoup()
tax_data = urllib.request.urlopen(urllib.request.Request('https://www.columbus.gov/tax/PrintAllMunis.aspx'))


soup = BeautifulSoup(tax_data.read().decode('utf-8'), 'html.parser')

addresses = soup.find_all('td', {'class': 'mucip_cont_address'})
for address in addresses:
  print(address.get_text())