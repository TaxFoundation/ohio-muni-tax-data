from bs4 import BeautifulSoup
import urllib.request

# soup = BeautifulSoup()
tax_data = urllib.request.urlopen(urllib.request.Request('https://www.columbus.gov/tax/PrintAllMunis.aspx'))
print(tax_data.read().decode('utf-8'))