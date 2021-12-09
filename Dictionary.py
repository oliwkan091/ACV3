"""
Zawiera niezbędne bazy oraz funkcjie wspólne dla reszty plików
"""

# Posiada nazwy plików kontrolowanych przez program
    # 'pages' - to baza stron obsługiwanych przez program
    # 'database' - to nazwa bazy danych programu
    # 'chrome' - lokalizacja pliku chrome
    # 'logIn' - plik z datą
    # 'logs' - plik z danymi logów
    # NALoc - plik z lokalizacjami zpaisu newArticles.txt na róznych urządzeniach
metaFileNames = {'newArticles': 'newArticles.txt',
                 'pages' : 'pagesToCheck.txt',
                 'database': 'database',
                 "tempDb": "tempDatabase",
                 'chrome': 'chromedriver.exe',
                 'logIn':'data.txt',
                 'logs' : 'logs.txt',
                 'NALoc' : 'NALocFile.txt'}

# Pamięta lokalizacje wynikwą wszystkich synchronizowanych urządzeń, podczas zapisywania
# pliku iteruje i jak trafi na istniejącą baze to zapisuje
newALoc = ['D:\\Documents\\Dysk Google\\Schengen','C:\\Users\\Oliwier Kania\\Documents\\Google Drive\\Schengen']

# Linki do githuba z bazą danych
gitMetaNames = {'repo' : 'https://github.com/oliwkan091/articleCheckerV3.git'}

# Nazwy przełączniki pliku gitManager.py
    # boot - pobiera dane z githuba
    # finish - wysyła dane na githuba
gitManagerMethods = {'boot': 'gitManager.py c', 'finish': 'gitManager.py f', 'autoStart': 'articleCheckerV3.py'}

# Elementy składowe pliku danych ze stron
pagesData = ('title','=','\"')

# Zawiera dane składowe pliku wyjatków
# exceptionData = [('block','=','\"'),('key','=','\"')]
# Zawiera dane które należy usunąć by sprawdzić czy link się powtarza
repetedLinks = ('https:','http:')

# Dane które nalezy wyświetlić w mennu głównym
mainMenu = ('Pokaż zapisane linki','Dodaj linki','Usuń linki','Pokaż wyjątki','Dodaj wyjątek','Usuń wyjątek','Wyjdz')

# mainMenu = ('Pokaż zapisane linki','Dodaj linki','Usuń linki',
# 'Pokaż wyjątki','Dodaj wyjątek','Usuń wyjątek','Sprawdz stronę pochodną','Wyjdz')
# Rodzaje wyjątków
exceptionTypes = ['block','key']

# Rozdziela stringi
comma = '?!?'

# Przejście między folderami
doubleS = "\\"

# Logi które będą zapisywane do pliku logs
logLogs = {'ProgStart' : 'Program started',
           'ProgEndDJZ' : 'Program finished, everything was ap tu date \n',
           'ProgEnd' : 'Program finished \n',
           'PrepChrom': 'Preparing to start chromedriver.exe',
           'ChromStarted': 'Chromedriver.exe started',
           'ChromFail' : 'Chromedriver.exe failed to start',
           'noInternet': 'No internet connection',
           'gitBootSyncStart': 'Started git sync on boot',
           'gitBootSyncFinish': 'Finished git sync on boot',
           'gitFinishSyncStart': 'Started git sync on finish',
           'gitFinishSyncFinish': 'Finished git sync on finish',
           'LinkErr': 'Cannot connect to the specified link',
           'nl': '\n'}


# Sprawdza czy plik istnieje
def isFile(fileName):
    try:
        fileTest = open(fileName, 'r+')
        fileTest.close()
        return True
    except:
        return False


# Sprawdza czy dana fraza to link
def isLink(link, database):

    # Jeżeli link jest w bazie to nie ma po co łączyć się ze stroną
    for element in database:
        if link == element:
            print(f"Link {link} jest już w bazie")
            return True
    # Jeżeli w linku nie ma elemntów charakterystycznych dla linku to nie ma sensu go sprawdzać
    if repetedLinks[0] in link or repetedLinks[1] in link:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

        # Jeżeli link się nie wysypie to ozancza że istnieje
        try:
            driver.get(link)
            driver.quit()
            return True
        except:
            driver.quit()
            print(f"Link {link} jest nowy")
            return False
    #return False


# Sprawdza czy istenieje już baza danych, jeżeli nie to tworzy ją
def makeDatabase():
    import os
    try:
        os.listdir(os.getcwd() + '\\' + metaFileNames['database'])
    except:
        os.makedirs(os.getcwd() + '\\' + metaFileNames['database'])


# Sprawdza czy istnieje baza danych
def isDatabase():
    import os
    try:
        os.listdir(os.getcwd() + '\\' + metaFileNames['database'])
        return True
    except:
        return False


# Zmienia link na unikalną nazwę pliku
def makeNameFromLink(pageLink,type):
    #Tworzona jest nazwa pliku bazy danych na podstawie linku
    fileName = ''
    for letter in pageLink:
        if letter.isdigit() or letter.isalpha():
            fileName = fileName + letter

    return (fileName + '.' + type)


# Instaluje dodatkowe pakiety
def moduleInstaller():

    # Zawsze zainstalowane niezbędne do instalowanie modułów
    import subprocess
    import sys

    #Instaluje pakiety jeżeli któregoś nie ma

    try:
        import selenium
    except :
        subprocess.check_call([sys.executable, '-m', 'pip', 'install','selenium'])
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
    try:
        import git
    except:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install','gitpython'])
    try:
        import git
    except:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install','os'])


# Dodatje logi do rejestru
def addLog(logType,info):
    # Try catch dla upewnienia że wszystko się zapisze
    addLog = 0
    if isFile(metaFileNames['logs']):
        addLog = open(metaFileNames['logs'], 'a+')
    else:
        addLog = open(metaFileNames['logs'], 'w+')

    from datetime import datetime
    currentDate = datetime.now()

    addLog.write(currentDate.strftime("%d/%m/%Y %H:%M:%S") + '  ' + logLogs[logType] + ' ' + info + '\n')
    addLog.close()


# Sprawdza czy pogana ścieżka istnieje
def isDir(dir):
    import os
    return os.path.exists(dir)


# Dodawanie Dictionary do Array nie ma sensu!!!
def recLoad(data,i):
    title = ""
    isArr = False
    arr = []
    levelDick = {}
    while(i<len(data)):
        element = data[i]
        if element != "" and element != "," and element != "=":
            if element[0] != "\"":
                if i+2 < len(data) and data[i+2] == "{" :
                    returnedDick,i = recLoad(data, i+3)
                    if isArr:
                        toDiction = {}
                        toDiction[element] = returnedDick
                        arr.append(toDiction)
                    else:
                        levelDick[element] = returnedDick
                elif element == "}":
                    return levelDick, i
                elif element == "]":
                    copyToSave = []
                    copyToSave.extend(arr)
                    levelDick[title] = copyToSave
                    isArr = False
                elif i+2 < len(data) and data[i+2] == "[":
                    title  = element
                    isArr = True
                    arr.clear()
                    i+=2

                else:
                    levelDick[element] = data[i+2].replace("\"", "").replace("_", " ")
                    i+=2

            else:
                if isArr:
                    arr.append(element.replace("\"", "").replace("_", " "))

        i+=1

    return levelDick, i


# Wstępnie przygotowuje pliki przed ich wczytanie do programu
def loadDataFromFile(fileName):

    if isFile(fileName):
        dataToLoad = open(fileName, "r")
        loadedData = ""
        for line in dataToLoad:
            loadedData = loadedData + line.strip()

        dataToLoad.close()
        loadedData = loadedData.replace(" ", "")

        loadedData = loadedData.replace("=", " = ")
        loadedData = loadedData.replace("[", "[ ")
        loadedData = loadedData.replace("]", " ] ")
        loadedData = loadedData.replace("{", "{ ")
        loadedData = loadedData.replace("}", " } ")
        loadedData = loadedData.replace(",", " , ")

        loadedData = loadedData.split(" ")

        diction = {}
        diction,i = recLoad(loadedData,0)

        return diction

    else:
        print("Baza danych nie istnieje")
        return {}


# Rekurencyjnie wczytuje pliki
def recLoad(data, i):
    title = ""
    isArr = False
    arr = []
    levelDick = {}
    while(i<len(data)):
        element = data[i]
        if element != "" and element != "," and element != "=":
            if element[0] != "\"" :
                if i+2 < len(data) and data[i+2] == "{":
                    returnedDick,i = recLoad(data, i+3)
                    if isArr:
                        toDiction = {}
                        toDiction[element] = returnedDick
                        arr.append(toDiction)
                    else:
                        levelDick[element] = returnedDick
                elif element == "}":
                    return levelDick, i
                elif element == "]":
                    copyToSave = []
                    copyToSave.extend(arr)
                    levelDick[title] = copyToSave
                    isArr = False
                elif i+2 < len(data) and data[i+2] == "[":
                    title  = element
                    isArr = True
                    arr.clear()
                    i+=2

                else:
                    levelDick[element] = data[i+2].replace("\"", "").replace("_", " ")
                    i += 2

            else:
                if isArr:
                    arr.append(element.replace("\"", "").replace("_", " "))

        i += 1

    return levelDick, i


# Spacje w pliku zastąpione są przez "_"
def checkGrandSpaces(data):
    data = data.replace(" ","_")
    return data


# Przygotowywuje dane przed ich zapisaniem
def saveDataToFile(fileName,dataToSave):

    file = open(fileName,"w+")
    recSave(file,dataToSave)


# Rekurencyjnie przetwarza dane przed ich zapisaniem do pliku a'al json
def recSave(saveFile, dataToSave):
    for data, name in enumerate(dataToSave):
        if type(dataToSave[name]) == str:
            saveFile.write(name + " = \"" + checkGrandSpaces(dataToSave[name]) + "\",\n")
        elif type(dataToSave[name]) == dict:
            saveFile.write(name + " = {\n")
            recSave(saveFile,dataToSave[name])
            saveFile.write("}\n")
        else:
            saveFile.write(name + " = [\n")
            i = 0
            while i < len(dataToSave[name]):
                if i+1 != len(dataToSave[name]):
                    saveFile.write("\"" + checkGrandSpaces(dataToSave[name][i]) + "\",\n")
                else:
                    saveFile.write("\"" + checkGrandSpaces(dataToSave[name][i]) + "\"\n")
                i+=1
            saveFile.write("]\n")


# Sprawdza czy dany element występuje w dictionary, używane przy wczytywaniu plików
def checkIfDicionEelementExists(diction,elementName):
    try:
        diction[elementName]
        return True
    except:
        print("FALSE")
        return False

# Łączy się z podaną bazą i sprawdza czy jest połączenie z internetem
def isConnected():
    import requests
    host = 'https://www.google.pl/'
    try:
        requests.get(host)
        return True
    except requests.ConnectionError:
        print("false")
        return False

# Czeka określony czas na połączenie z internetem. Jeżeli go nie uzyska wyłącza program
def whileNotIsConnected():
    import time
    import Dictionary as Dict
    timeInSeconds = 0
    while not isConnected():
        print('Czekam na połączenie z internetem')
        time.sleep(10)
        timeInSeconds += 1
        if timeInSeconds == 50:
            Dict.addLog('noInternet', '')
            exit(0)


# Szuka lokalizacji pliku zapisu po nazwie urządzenia, jeżeli nie znajdzie to włącza funkcję która prosi o podanie
def NAFileLoc():
    import Dictionary as Dict
    import os
    data = Dict.loadDataFromFile(Dict.metaFileNames['NALoc'])

    pcName = os.environ['COMPUTERNAME']

    for a, name in enumerate(data["Loc"]):
        if name == pcName:
            return data["Loc"][name]

# Nowa forma zapisu plików wynikowych
# Zbiera pojedyncze pliki z folderu tempDatabase które zawierają wyniki z każdej sprawdzanej strony
# i zapisuje je do jednego pliku wynikowego
def saveNewArticlesV2(isBoot):
    import os
    nATempDatabase = os.getcwd() + "\\tempDatabase"
    if not isDir(nATempDatabase):
        if not isBoot :
            print("Brak nowych artykułów")
        return

    tempDatabaseList = os.listdir(os.getcwd() + '\\tempDatabase')
    if len(tempDatabaseList) == 0:
        if not isBoot:
            print("Brak nowych artykułów")
        os.removedirs(os.getcwd() + '\\tempDatabase')
        return

    if not isBoot:
        print(NAFileLoc() + '\\' + metaFileNames['newArticles'])
    newArticlesSaveFile = open(NAFileLoc() + '\\' + metaFileNames['newArticles'], "a+")

    from datetime import datetime
    currentDate = datetime.now()
    newArticlesSaveFile.write(currentDate.strftime("%d/%m/%Y %H:%M:%S") + "\n")

    for file in tempDatabaseList:
        tempFile = open("tempDatabase\\" + file, "r")

        for line in tempFile:
            newArticlesSaveFile.writelines(line)

        newArticlesSaveFile.writelines("")
        tempFile.close()
        if not isBoot:
            print("tempDatabase\\" + file)
        os.remove("tempDatabase\\" + file)

    newArticlesSaveFile.close()
    os.removedirs(os.getcwd() + '\\tempDatabase')


# Jeżeli podczas poprzedniego wywołania programu wystąpił błąd to funkcja sprząta
# i zapisuje to co nie zostało poprzednio zapisane
def cleanAfterError():
    import os
    if isDir(os.getcwd() + doubleS + metaFileNames["tempDb"]):
        print("Naprawa po awarii")
        saveNewArticlesV2(True)

# Ostrzeżenie przed wywołaniem
if __name__ == "__main__":
    print("Biblioteka Dictionary nie została stworzona do samodzielnego uruchamiania,"
          " zalecane jest jej importowanie")