from lxml import html  
import requests

page = requests.get('http://quotes.toscrape.com/')
tree = html.fromstring(page.content)

stuff = tree.xpath('//span[@class="text"]/text()')

thefile = open('Words.txt', 'w')

for quote in stuff:
  thefile.write("%s\n" % quote)

