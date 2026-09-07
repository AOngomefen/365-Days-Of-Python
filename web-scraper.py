#small web scraper /practice/
#sample site /qoutes to scrape webstite/

#import libs

from bs4 import BeautifulSoup
import requests

# create vars
link = "https://quotes.toscrape.com"
page_to_scrape = requests.get(link)
soup = BeautifulSoup(page_to_scrape.text, "html.parser")

#find objective attributes text and author 
quotes = soup.find_all("span", attrs={"class":"text"})
authors = soup.find_all("small", attrs={"class":"author"})

# print individual quote & author
for quote, author in zip(quotes, authors):
    print(quote.text + " - " + author.text)
    print("")



############### 
#choice = input("pick a number between 1-10: ")
#
#for quote, author in choice:
#    print(quote.text + " - " + author.text)
##############
