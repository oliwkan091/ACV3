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
        subprocess.check_call([sys.executable, '-m', 'pip', 'install','lxml'])
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

#Oczytuje dane niezbędne do działania programu i zapusje je do Dictionary
def readMetadata():
	#Tu znajdują się wszystkie informacjie na temat nazw plików oraz ich lokalizacji 
	metadataFile = 'metadata.txt'

	maintainInfo = {'articles':'', #Nazwa pliku ze stronami to pobrania
					'resoults':'', #Nazwa pliku z wynikowego
					'resoultsLocation':'', #Lokalizacja pliku wynikowego
					'articlesLocation':'', # lokalizacja pliku ze stronami
					'databaseLocation':''} # lokalizacja folderu z bazą danych

	#Sprawdza czy plik metadata w ogóle istanieje
	try:
		file = open(metadataFile,'r')

		for line in file.readlines():
			
			line = line.strip()
			if not line[0] == '#':
				data = line.split('=')
				data[0] = data[0].strip()
				data[1] = data[1].strip()
				data[1] = data[1].replace('\"','')

				#Jeżeli w nzawie jest "Location" to ozancza że jest to ścieżka i trzeba do niej dodać lokalizację 
				if data[1] == '' or 'Location' in data[0] and not data[1][1] == ':' and not data[1][2] == '\\':
					tempData = os.getcwd()
					if data[1] != '':
						data[1] = tempData + '\\' + data[1]
					else:
						data[1] = tempData

			maintainInfo[data[0]] = data[1]


		file.close()
	except:
		print("Plik \"metadata\" nie istanieje!")
		print("Plik \"metadata\" został utworzony, uzupełnij go by korzystać z programu ")
		file = codecs.open(metadataFile,'a+','Windows-1250')

		file.close()
		exit(0)

	#Wczytuje linki do stron ze wskazanego pliku
	pagesLinks = []

	#Sprawdza czy plik istnieje
	try:
		file = open(maintainInfo['articles'],'r')

		for line in file.readlines():
			line = line.strip()
			if not line[0] == '#':
				if "title" in line:
					line = re.findall('\".[^\"]*\"',line)
					line = line[0].replace('"','')
					pagesLinks.append(line)

		file.close()

	except:
		print("Plik \"pagesToCheck.txt\" z danymi do artykułów nie istnieje")
		print("Plik \"pagesToCheck.txt\" został utworzony, uzupełnij o strony które mają być sprawdzane")
		file = codecs.open(maintainInfo['articlesLocation'] + maintainInfo['articles'],'a+','Windows-1250')

		file.close()


	return maintainInfo,pagesLinks

#Pobierra linki ze stron
def getAllLinks(pageLink):

	web = requests.get
	#Sprawdza czy do strony jest dostęp, czy istanieje 
	try:
		web = requests.get(pageLink)
	
		better_web = bs4.BeautifulSoup(web.text,'lxml')
		better_web2 = better_web.find_all('a')
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

		i = 0
		for link in links:
			i+=1;

		return links,names

	except:
		print('Witryna linku: ' + pageLink + 'jest nieosiagalna')
		return [],[]

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
def manageLinks(pageLink,links,names,maintainInfo):

	print('Sprawdzam: ' + pageLink)
	#Tworzona jest nazwa pliku bazy danych na podstawie linku
	pageFileName = ''
	for letter in pageLink:
		if letter.isdigit() or letter.isalpha():
			pageFileName = pageFileName + letter

	pageFileName = pageFileName + '.xlsx'
	#Link do folderu z bazą danych
	fileList = os.listdir(maintainInfo['databaseLocation'] + '\\')

	#Jeżeli baza już ostnieje to jest edytowana, jeżeli nie to jest tworzona na nowo bo to oznacza że został dodany nowy link
	if pageFileName in fileList:
		dataFromExcel = pandas.read_excel(maintainInfo['databaseLocation'] + '\\' + pageFileName)

		#Znajduje najwyższą liczbę pożątkową w pliku
		maxNumber = 0
		for number in dataFromExcel['Number']:
			if maxNumber < number:
				maxNumber = number

		dataToSave = []

		#Zpisuje linki w raz z nazwami i liczbami porządkowymi do do listy 
		i=0
		for pageData in  links:
			pageData = pageData.strip()
			isLinkInFile = False;
			for excelData in dataFromExcel['Link']:
				excelData = excelData.strip()
				if pageData == excelData:
					isLinkInFile = True
					break;
			if not isLinkInFile:
				maxNumber+=1
				dataToSave.append([maxNumber,names[i],pageData])

			i += 1


		#Wybiera co ma zostać tytułem linku tak by nie był to html lub data
		i=0
		j=0
		while j < len(dataToSave):
			mainLink = dataToSave[j]
			i=0
			deletePosition = j
			while i < len(dataToSave):
				if j!=i and mainLink[2] == dataToSave[i][2]:
					if isLink(mainLink[1]) or len(mainLink[1]) < len(dataToSave[i][1]) and not isLink(dataToSave[i][1]):
						mainLink = dataToSave[i]
						dataToSave.pop(deletePosition)
						deletePosition = i
					else:
						dataToSave.pop(i)


				i+=1
			j+=1
		
		numberToSave = []
		nameToSave = []
		linkToSave = []

		#Jeżeli list do zapisu nie jest pousta to zapisuje 
		if dataToSave != []:
			file = codecs.open(maintainInfo['resoultsLocation'] + '\\' + maintainInfo['resoults'],'a+','Windows-1250')
			for articles in dataToSave:
				file.write(pageLink + '\n' + articles[1] + '\n' + articles[2] + '\n' + '\n')
				numberToSave.append(articles[0])
				nameToSave.append(articles[1])
				linkToSave.append(articles[2])
			file.close()

			df = pandas.DataFrame({'Number':numberToSave,'Name':nameToSave,'Link':linkToSave})

			dataFromExcel = dataFromExcel.append(df,ignore_index=True)

			excelWriter = pandas.ExcelWriter(maintainInfo['databaseLocation'] + '\\' + pageFileName)
			dataFromExcel.to_excel(excelWriter,'1',index = False)
			excelWriter.save()

	#Jeżeli plik nie istnieje to tworzona jest nowa baza danych, w tej sytuacji nic nie zostanie zapisane do pliku wynikowego
	else:
		excelWriter = pandas.ExcelWriter(maintainInfo['databaseLocation'] + '\\' + pageFileName)
		dataF = pandas.DataFrame({'Number':[],'Name':[],'Link':[]})
		dataF.to_excel(excelWriter,'1',index = False)
		excelWriter.save()

		numbers = []
		for i in range(0,len(names)):
			numbers.append(i)
			i += 1

		df = pandas.DataFrame({'Number':numbers,'Name':names,'Link':links})

		excelWriter = pandas.ExcelWriter(maintainInfo['databaseLocation'] + '\\' + pageFileName)
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

	filesInDatabase = os.listdir(maintainInfo['databaseLocation'])
	for file in filesInDatabase:
		isfileInPage = False
		for page in pageFileNames:
			if file == page:
				isfileInPage = True
				break;
		if not isfileInPage:
			os.remove(maintainInfo['databaseLocation'] +'\\'+ file)


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

	pageFileNames = []
	
	#Przychodzi przez wszystkie strony
	for link in pagesLinks:
		links,names = getAllLinks(link)
		if not links == []: 
			pageFileNames.append(manageLinks(link,links,names,maintainInfo))

	deleteNotUsedDatabases(pageFileNames)

