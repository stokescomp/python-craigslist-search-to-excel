#parses html easily. install using easy_install beautifulsoup4 or sudo apt-get install python-beautifulsoup4
from bs4 import BeautifulSoup
#writing to excel. Use easy_install xlwt to install or sudo apt-get install python-xlwt
from xlwt import Workbook
#opening a url. Comes with python 2.7
import urllib

excelRowCount = 1
book = ''
sheet1 = ''
pageNumber = 1

def makelist(htmlsoup):
	global excelRowCount, book, sheet1, pageNumber
	print "searching for: "+searchTerm
	allrows = htmlsoup.find_all('p', 'row')
	if len(allrows) == 0:
		print "no results were found"
		return 0
	print "total items found:",len(allrows)
	for row in allrows:
		date = row.find('span', 'itemdate').text.strip()
		link_link = row.find('a')['href']
		link_text = row.find('a').text.strip()
		price = row.find('span', 'itempp').text.strip()
		note = row.find('span', 'itempn').text.strip()
		category_text = row.find('span', 'itemcg').text.strip()
		category_link = row.find('span', 'itemcg').a['href']
		
		sheet1.write(excelRowCount,0,date)
		sheet1.write(excelRowCount,1,link_link)
		sheet1.write(excelRowCount,2,link_text)
		sheet1.write(excelRowCount,3,price)
		sheet1.write(excelRowCount,4,note)
		sheet1.write(excelRowCount,5,category_link)
		sheet1.write(excelRowCount,6,category_text)
		excelRowCount = excelRowCount+1
		sheet1.flush_row_data()
	#get next text if it exists
	pagesElement = htmlsoup.find('h4', 'ban').findAll('span')[1].findAll('b')
	if len(pagesElement) > 0:
		pages = pagesElement[0].text
	else:
		pages = ''
	if pages == 'Next >>':
		pageNumber = pageNumber+1
		print 'going to page '+str(pageNumber)+"\n"
		next_link = htmlsoup.find('h4', 'ban').findAll('span')[1].a['href']
		searchPage(next_link)
	else:
		print 'saving excel file'
		book.save('/home/mike/MyStuff/selenium/python/craigslist/craigslist.xls')

def searchPage(page):
	#print page
	html = urllib.urlopen(page) 
	htmlsoup = BeautifulSoup(html)
	makelist(htmlsoup)

def initExcel():
	global book, sheet1
	book = Workbook()
	sheet1 = book.add_sheet('Craigs List')
	#write first row of sheet
	sheet1.write(0,0,'Date')
	sheet1.write(0,1,'Item Link')
	sheet1.write(0,2,'Description')
	sheet1.write(0,3,'Price')
	sheet1.write(0,4,'Note')
	sheet1.write(0,5,'Category Link')
	sheet1.write(0,6,'Category')
	
	#change the width of columns
	sheet1.col(0).width = 2000
	sheet1.col(1).width = 10000
	sheet1.col(2).width = 13000
	sheet1.col(3).width = 2000
	sheet1.col(4).width = 6000
	sheet1.col(5).width = 3500
	sheet1.col(6).width = 6000

#get the search term from user
#searchTerm = 'fish tank';
searchTerm = 'testing the test to find';

#start here
initExcel()
searchPage("http://boise.craigslist.org/search/sss?query="+searchTerm+"&srchType=A") 
#searchPage("http://boise.craigslist.org/search/sss?query=fish%20tank&srchType=A&s=200") 

