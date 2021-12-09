# -*- coding: utf-8 -*-
#^^ Odpowiada za kodowanie do zapisu

def moduleInstaller():
    #Zawsze zainstalowane niezbędne do instalowanie modułów
    import subprocess
    import sys

    #Instaluje pakiety jeżeli któregoś nie ma 
    try:    
    	import codecs
    except :
        subprocess.check_call([sys.executable, '-m', 'pip', 'install','codecs'])
    try:
    	import urllib
    except :
        subprocess.check_call([sys.executable, '-m', 'pip', 'install','urllib'])
    try:
    	import time
    except :
        subprocess.check_call([sys.executable, '-m', 'pip', 'install','time'])
    try:
    	import requests
    except :
        subprocess.check_call([sys.executable, '-m', 'pip', 'install','requests'])
    try:
        import lxml
    except :
        subprocess.check_call([sys.executable, '-m', 'pip', 'install','lxml'])
    try:
        import bs4 
    except :
        subprocess.check_call([sys.executable, '-m', 'pip', 'install','bs4'])
    try:
        import re
    except :
        subprocess.check_call([sys.executable, '-m', 'pip', 'install','re'])
    try:
        import pandas
    except :
        subprocess.check_call([sys.executable, '-m', 'pip', 'install','pandas'])
    try:
        import os
    except :
        subprocess.check_call([sys.executable, '-m', 'pip', 'install','os'])
    try:
        import openpyxl
    except :
        subprocess.check_call([sys.executable, '-m', 'pip', 'install','openpyxl'])

#Zawiera reakcje na bledy ktore pojawia sie w programie
def errors(errorType,param1):

	#W momencie braku pliku metadata.txt 
	if errorType == 'noMetedataTxt':
		print('Plik metadata.txt nie istnieje')

		file = codecs.open("metadata.txt",'w','Windows-1250')
		file.write('#Należy wypełnić wszystkie pola. Jeżeli plik nie znajduje się w folderze z programeme to należy dodać go łącznie z jego pełną ścierzką \n')
		file.write('articles = ""\n') #Nazwa z lokazlizacją
		file.write('resoults = ""\n') #Nazwa z lokalizacją
		file.write('database = ""\n') #Nazwa z lokalizacją 
		file.close()

		print('Plik metadata.txt został utworzony w katalogu programu, uzupełnij go by kontynuowac')

	elif errorType == 'noArticlesFileTxt':
		print('Plik z linkami do stron nie zostal znaleziony, zobacz czy podana scierzka jest poprawna oraz czy plik w ogole istnieje')
		file = codecs.open("pagesToCheck.txt",'w','Windows-1250')
		file.write('title = ""\n')
		print('Utworzono przeykladowy plik w folderze programu, nazwa \" pagesToCheck.txt \"')

#Oczytuje dane niezbędne do działania programu i zapusje je do Dictionary
def readMetadata():
	#Tu znajdują się wszystkie informacjie na temat nazw plików oraz ich lokalizacji 
	metadataFile = 'metadata.txt'


	maintainInfo = {'articles':'maintainInfo', #Nazwa pliku ze stronami to pobrania
					'resoults':'', #Nazwa pliku z wynikowego
					'database':''} #Lokalizacja folderu z bazą danych



	#Sprawdza czy plik metadata w ogóle istanieje
	try:
		file = open(metadataFile,'r')
		file.close()
	except IOError:
		errors('noMetedataTxt',0)
		exit(0)

	file = open(metadataFile,'r')

	#Odczytuje dane 'metadata' z pliku i dodatje je do maintainInfo
	for line in file.readlines():
		line = line.strip()
		if not line[0] == '#':
			data = line.split('=')
			data[0] = data[0].strip()
			data[1] = data[1].strip()
			data[1] = data[1].replace('\"','')

			maintainInfo[data[0]] = data[1]

	file.close()

	#Jeżeli lokalizacja 'database nie została podana to automatycznie ją generuje'
	print(maintainInfo['database'])
	if maintainInfo['database'] == '':
		print(maintainInfo['database'])
		maintainInfo['database'] = 'database'

	#Sprawdza czy plik istnieje
	try:
		file = open(maintainInfo['articles'],'r')
		file.close()
	except IOError:
		errors('noArticlesFileTxt',0)
		exit(0)

	#Wczytuje linki do stron które mają zostać sprawdzone 
	file = open(maintainInfo['articles'],'r')
	pagesLinks = []

	for line in file.readlines():
		line = line.strip()
		if not line[0] == '#':
			if "title" in line:
				line = re.findall('\".[^\"]*\"',line)
				if line:
					line = line[0].replace('"','')
					pagesLinks.append(line)

	file.close()

	return maintainInfo,pagesLinks

def filterBlockedLinks(fileName,links,names,maintainInfo):
	databaseLocation = os.getcwd() + '\\' + maintainInfo['database']
	fileList = os.listdir(databaseLocation)
	fileName = fileName + '.txt'
	if (fileName) in fileList:
		print('inList')
		txtFile = open(databaseLocation + '//' + fileName,'r')
		blockList = []
		for line in txtFile.readlines():
			if line and line[0] != '#' and 'phrase' in line:
				line = line.replace('phrase','')
				line = line.replace('\"','')
				line = line.replace('=','')
				line = line.strip()
			blockList.append(line)
		txtFile.close()
		if blockList:
			i = 0
			while i < len(links):
				for block in blockList:
					if block in links[i]:
						#print(links[i])
						links.pop(i)
						names.pop(i)
				i+=1
			print(links)
			return links,names
		else:
			return links,names
	else:
		print('NotInList')
		txtFile = open(databaseLocation + '//' + fileName,'w')
		txtFile.close()



#Pobierra linki ze stron
def getAllLinks(pageLink):

	isPageAvilable = False
	web = ''

	#Sprawdza czy do strony jest dostęp, czy istanieje 
	try:
		web = requests.get(pageLink)
		isPageAvilable = True
	except:
		print('Witryna linku: ' + pageLink + 'jest nieosiagalna')
		return [],[]

	if isPageAvilable:

		better_web = bs4.BeautifulSoup(web.text,'lxml')

		better_web2 = better_web.find_all('a')
		dataFromPage = [],[]
		links = []
		names = []
		for link in better_web2:

			#Sprawdza czy jest to link
			tempLink = re.findall('href=\".[^\"]*\"',str(link))
			tempName = re.findall('>.*<',str(link))

			#Sprawdza czy link i nazwa istanieje 
			if tempName and tempLink:
				tempName = tempName[0].replace('<','')
				tempName = tempName.replace('>','')
				names.append(tempName)
				tempLink = tempLink[0].replace('href="','')
				tempLink = tempLink.replace('"','')
				links.append(tempLink)

		#Ponieważ nie udało mi się przesortować podwójnej tablicy to trzeba z niej zrobić pojedyńczą. Trzeba połączyć link z nazwą link + '!?!' + nazwa przesortować i rodzielić 
		dataToSort = []
		i = 0
		while i < len(links):
			dataToSort.append(links[i] + '!?!' + names[i])
			i+=1

		sortedData = sorted(dataToSort)

		#Po sortowaniu tablica jest rodzielana
		for element in sortedData:
			tempSplit = element.split('!?!')
			if tempSplit:
				dataFromPage[0].append(tempSplit[0])
				dataFromPage[1].append(tempSplit[1])

		#Usuwa duplikaty linków i zostawia ten który ma najdziebdziej tytułowy tytuł
		finalDataFromPage = [[],[]]
		i = 0
		startSeries = False

		#Działa tak długo aż przejdzie przez wyzstkie linki pobrane ze strony
		while i < len(dataFromPage[0]):

			#Jeżeli obecny element nie jest ostatnim to sprawdza czy kolejny link nie jest taki sam
			if i < len(dataFromPage[0])-1 and dataFromPage[0][i] == dataFromPage[0][i+1]:

				#Jeżeli link i oraz i+1 są takie same to oznazca że rozpoczęła się seria identycznych linków z któryvh należy zostawić tlyko jeden 
				if startSeries == False:
					startSeries = True
					starSeriesPosition = i

			#Jeżeli link i jest różny od i+1 i startSeries == True to oznacza że skńczyła się seria i trzeba wybrać jeden z linkó
			elif startSeries == True:
				startSeries = False
				bestToTitle = dataFromPage[1][starSeriesPosition]
				bestToLink = dataFromPage[0][starSeriesPosition]
				bestTitleLocation = starSeriesPosition
				j = starSeriesPosition
				while j < i:
					if not isLink(dataFromPage[1][j]) and len(bestToTitle) < len(dataFromPage[1][j]):
						bestToTitle = dataFromPage[1][j] 
						bestToLink = dataFromPage[0][j]
						bestTitleLocation = j
					j+=1
				finalDataFromPage[0].append(bestToLink)
				finalDataFromPage[1].append(bestToTitle)
				
			#Jeżeli nie ma żadnej serii linków ale jest to ostatni element to dodaje ostatni link 
			else:
				finalDataFromPage[0].append(dataFromPage[0][i])
				finalDataFromPage[1].append(dataFromPage[1][i])

			i+=1
		
		return finalDataFromPage[0],finalDataFromPage[1]

#Sprawdza czy danyy string jest bardziej nazwą czy linkiem, niezbędne do wybrania odpowidniej nazwy do pliku wynikowego, link oznacza to wszystko co nie przypomina zwykłej nazwy
def isLink(link):
	#Znaki charakterystyczne dla linku
	linkData = '=/\"-'

	closerToLink = 0
	for letter in link:
		for sign in linkData:
			if sign == letter:
				closerToLink+=1
			if closerToLink >=3 :
				return True
	return False;

#Operuje na popranych linkach
def manageLinks(pageLink,links,names,maintainInfo,newArticles):

	print('Sprawdzam: ' + pageLink)
	#Tworzona jest nazwa pliku bazy danych na podstawie linku
	pageFileNameNoEnding = ''
	for letter in pageLink:
		if letter.isdigit() or letter.isalpha():
			pageFileNameNoEnding = pageFileNameNoEnding + letter

	pageFileName = pageFileNameNoEnding + '.xlsx'

	links , names = filterBlockedLinks(pageFileNameNoEnding, links,names,maintainInfo)
	#if 'histo' in pageFileName:
		#print(links)
	#Link do folderu z bazą danych
	fileList = os.listdir(os.getcwd() + '\\' + maintainInfo['database'])

	#Jeżeli baza już ostnieje to jest edytowana, jeżeli nie to jest tworzona na nowo bo to oznacza że został dodany nowy link
	if pageFileName in fileList:
		dataFromExcel = pandas.read_excel(maintainInfo['database'] + '\\' + pageFileName)
		newDataFromExcel = [],[],[]
		firstFromPage = True

		#Przechodzi przez cały zbiór linków pobrany ze strony i porównuej je z pobranymi by sprawdzić który jest nowy a który już był. Jeżeli linku nie ma w bazie excela to oznacza że jest nowy 
		number = 0
		while number < len(links):
			linkInDatabase = False
			for dataLink in dataFromExcel['Link']:
				if links[number] == dataLink:
					linkInDatabase = True
					break;	

			if linkInDatabase == False:
				if firstFromPage:
					newArticles.append('\n')
					newArticles.append(pageLink)
					firstFromPage = False
				newArticles.append(names[number])
				newArticles.append(links[number])
			
			newDataFromExcel[0].append(number+1)
			newDataFromExcel[1].append(names[number])
			newDataFromExcel[2].append(links[number])

			number+=1

		#Baza danych jest za każdym razem usuwana i tworzona na nowo by nie trzymać niepotrzebnych linków
		os.remove(os.getcwd() + '\\' + maintainInfo['database'] + '\\' + pageFileName)

		excelWriter = pandas.ExcelWriter(maintainInfo['database'] + '\\' + pageFileName)
		dataF = pandas.DataFrame({'Number':newDataFromExcel[0],'Name':newDataFromExcel[1],'Link':newDataFromExcel[2]})
		dataF.to_excel(excelWriter,'1',index = False)
		df = pandas.DataFrame({'Number':newDataFromExcel[0],'Name':newDataFromExcel[1],'Link':newDataFromExcel[2]})
		excelWriter.save()

				
	#Jeżeli baza nie istnieje to zapisuje wszystkie linki
	else:

		excelWriter = pandas.ExcelWriter(maintainInfo['database'] + '\\' + pageFileName)
		dataF = pandas.DataFrame({'Number':[],'Name':[],'Link':[]})
		dataF.to_excel(excelWriter,'1',index = False)
		excelWriter.save()

		numbers = []
		for i in range(1,len(names)+1):
			numbers.append(i)
			i += 1

		df = pandas.DataFrame({'Number':numbers,'Name':names,'Link':links})

		excelWriter = pandas.ExcelWriter(maintainInfo['database'] + '\\' + pageFileName)
		df.to_excel(excelWriter,'1',index = False)
		excelWriter.save()


	return pageFileName
	
#Sprawdza czy jest połączenie z internetem
def isConnected():
	host = 'http://google.com'
	try:
	    urllib.request.urlopen(host)
	    return True
	except:  
	    return False

#Usuwa bazy danych które nie są używane bo link został usunięty
def deleteNotUsedDatabases(pageFileNames):

	isfileInPage = False

	#print(os.getcwd() + maintainInfo['database'])
	filesInDatabase = os.listdir(os.getcwd() +'\\' +  maintainInfo['database'])
	for file in filesInDatabase:
		if 'xlsx' in file:
			isfileInPage = False
			for page in pageFileNames:
				if file == page:
					isfileInPage = True
					break;
			if not isfileInPage:
				os.remove(maintainInfo['database'] +'\\'+ file)

def saveNewArtiles(newArticles):
	#file = open(maintainInfo['resoults'],'a+')
	file = codecs.open(maintainInfo['resoults'] ,'a+','Windows-1250')
	for link in newArticles:
		file.write(link + '\n')

	file.close()



if __name__ == "__main__":
	

	moduleInstaller()

	import requests 
	import bs4
	import re
	import codecs
	import pandas 
	import codecs
	import os
	import time
	import urllib

	timeInSeconds = 0
	while not isConnected():
		print(isConnected())
		print('Czekam na połączenie z internetem')
		time.sleep(10)
		timeInSeconds+=1
		if timeInSeconds == 50:
			exit(0)

	maintainInfo,pagesLinks =  readMetadata()

	if maintainInfo['database'] not in os.listdir(os.getcwd()):
		os.makedirs(os.getcwd() + '\\' + maintainInfo['database'])
	pageFileNames = []
	newArticles = []
	
	#Przychodzi przez wszystkie strony
	for link in pagesLinks:
		links,names = getAllLinks(link)
		if not links == []: 
			pageFileNames.append(manageLinks(link,links,names,maintainInfo,newArticles))
	if newArticles:
		saveNewArtiles(newArticles)
	deleteNotUsedDatabases(pageFileNames)


