"""
Zawiera niezbędne bazy oraz funkcjie wspólne dla reszty plików
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium

metaFileNames = {"newArticles": "newArticles.txt",
                 "pages": "pagesToCheck.txt",
                 "database": "database",
                 "tempDb": "tempDatabase",
                 "chrome": "chromedriver.exe",
                 "logIn": "data.txt",
                 "logs": "logs.txt",
                 "NALoc": "NALocFile.txt",
                 "groupFile": "groups.txt",
                 "boot": "boot.py",
                 "gm": "gitManager.py",
                 "acm": "articleCheckerManager.py",
                 "Dict": "Dictionary.py",
                 "acv3": "articleCheckerV3.py",
                 # "logIn": "logIn",
                 "chromeZip": "chromedriver.zip"}
"""
Posiada nazwy plików kontrolowanych przez program
    - "newArticles": "newArticles.txt" - nazwa pliku zapisu noewych artykułów
    - "pages": "pagesToCheck.txt" - to baza stron obsługiwanych przez program
    - "database": "database" - to nazwa bazy danych programu
    - "tempDb": "tempDatabase" - tymczasowy folder zapisu noewych artykułów poszczególnych stron
    - "chrome": "chromedriver.exe" - nazwa sterownika chrome
    - "logIn": "data.txt" - plik z datą
    - "logs": "logs.txt" - plik z danymi logów
    - "NALoc": "NALocFile.txt" - plik z lokalizacjami zpaisu newArticles.txt na róznych urządzeniach
    - "groupFile": "groups.txt" - nazwa pliku zapisu z danymi grup
    - "boot": "boot.py" -  nazwa pliku skryptu
    - "gm": "gitManager.py" -  nazwa pliku skryptu
    - "acm": "articleCheckerManager.py" -  nazwa pliku skryptu
    - "Dict": "Dictionary.py" -  nazwa pliku skryptu
    - "acv3": "articleCheckerV3.py" -  nazwa pliku skryptu
    # - "logIn": "logIn" - folder ze skryptami do logwania
    - "chromeZip": "chromedriver.zip" - nazwa sterownika chrome w zip
"""


newALoc = ["D:\\Documents\\Dysk Google\\Schengen","C:\\Users\\Oliwier Kania\\Documents\\Google Drive\\Schengen"]
"""
Pamięta lokalizacje wynikwą wszystkich synchronizowanych urządzeń, podczas zapisywania
pliku iteruje i jak trafi na istniejącą baze to zapisuje
"""


gitMetaNames = {"repo" : "https://github.com/oliwkan091/articleCheckerV3.git"}
"""
Linki do githuba z bazą danych
"""


gitManagerMethods = {"boot": "gitManager.py c", "finish": "gitManager.py f", "autoStart": "articleCheckerV3.py"}
"""
Nazwy przełączniki pliku gitManager.py
    - boot - pobiera dane z githuba
    - finish - wysyła dane na githuba
"""


pagesData = ("title","=","\"")
"""
Elementy składowe pliku danych ze stron
"""


repetedLinks = ("https:","http:")
"""
Zawiera dane składowe pliku wyjatków
exceptionData = [("block","=","\""),("key","=","\"")]
awiera dane które należy usunąć by sprawdzić czy link się powtarza
"""


mainMenu = ("Pokaż zapisane linki", "Dodaj linki", "Usuń linki", "Pokaż wyjątki", "Dodaj wyjątek", "Usuń wyjątek",
            "Otwóz zapisane linki", "Edytuj grupy","Wygeneruj nazwę pliku z wybranego linku", "Wyjdz")
"""
Dane które nalezy wyświetlić w mennu głównym
"""


exceptionTypes = ["block", "key"]
"""
Rodzaje wyjątków
mainMenu = ("Pokaż zapisane linki","Dodaj linki","Usuń linki",
"Pokaż wyjątki","Dodaj wyjątek","Usuń wyjątek","Sprawdz stronę pochodną","Wyjdz")
"""


comma = "?!?"
"""
Rozdziela stringi
"""


doubleS = "\\"
"""
Przejście między folderami
"""


logLogs = {"ProgStart" : "Program started",
           "ProgEndDJZ" : "Program finished, everything was ap tu date \n",
           "ProgEnd" : "Program finished \n",
           "PrepChrom": "Preparing to start chromedriver.exe",
           "ChromStarted": "Chromedriver.exe started",
           "ChromFail" : "Chromedriver.exe failed to start",
           "noInternet": "No internet connection",
           "gitBootSyncStart": "Started git sync on boot",
           "gitBootSyncFinish": "Finished git sync on boot",
           "gitFinishSyncStart": "Started git sync on finish",
           "gitFinishSyncFinish": "Finished git sync on finish",
           "LinkErr": "Cannot connect to the specified link",
           "nl": "\n"}

"""
Logi które będą zapisywane do pliku logs
"""


switches = {"moduleMode": "",
            "gitMode": "g",
            "rebootMode": "r",
            "manual": "m",
            "finisher": "f",
            "checker": "c",
            "articleCheckerV3": "acv3",
            "articleCheckerManager": "acm"}
"""
Przełączniki do włączania programu
    - moduleMode - Brak przełącznik, pirwsze uruchominie, system sprawdzi stan modułów, synchronizację z git
        i zapyta co dalej
    - gitMode - uruchamia się i pomija instalację modułów
    - rebootMode - pomija instalacje modułów i synchronizację z git
    - manual - wymuszenie działania poszczególnych komponentów
    - finisher - Uruchamia wypchnięcie do gita
    - checker - uruchamia pobranie z gita
    - articleCheckerV3 - daje znać że po wstępnej synchronizacji będzie chcaił użyć acv3
    - articleCheckerManager - daje znać że po wstępnej synchronizacji będzie chcaił użyć gm
"""


txtEssential = {metaFileNames["pages"]: [["title"], [[]]],
                metaFileNames["NALoc"]: [["Loc"], [{}]]}
"""
Podczas wcyztywanie konkretnych plików sprawdza czy nie brakuje w nich zniezbędnych danych
"""

urlLinks = {"googlePage": "https://www.google.pl/",
            "chromeDriverDownloadPermLink": "https://chromedriver.storage.googleapis.com/96.0.4664.45/chromedriver_win32.zip",
            "chromeDriverDownloadCurrLinkBegin": "https://chromedriver.storage.googleapis.com/",
            "chromeDriverDownloadCurrLinkEnd": "/chromedriver_win32.zip"}
"""
Linki do stron niezbędne do działania

    - "googlePage": "https://www.google.pl/" - strona do googla, używana do sprawdzenia połączenia
    - "chromeDriverDownloadPermLink": "https://chromedriver.storage.googleapis.com/96.0.4664.45/chromedriver_win32.zip" - stały link do pobrania drivera w sytuacji jego braku, potem i tak trzeba pobrać aktualny
    - "chromeDriverDownloadCurrLinkBegin": "https://chromedriver.storage.googleapis.com/" - pierwsza część (przez wersją) linku używana do pobrania drivera
    - "chromeDriverDownloadCurrLinkEnd": "/chromedriver_win32.zip"} - druga część linku (po wersji) używana do pobrania drivera
"""

def isFile(fileName: str) -> bool:
    """
    Sprawdza czy plik o podanej nazwie istnieje
    :param fileName: Nazwa pliku, łacznie z rozszerzeniem
    :return: True jeżeli istnieje
    """

    try:
        fileTest = open(fileName, "r+")
        fileTest.close()
        return True
    except:
        return False


def isLink(link: str, database: list, driver: selenium.webdriver.chrome.options) -> bool:
    """
    Sprawdza czy podany string jest linkiem
    :param link: link do stroy który ma zostać sprawdzony
    :param database: baza danych linków które są już znane, jeżeli podany wyżej link znajduje się w bazie to nie
    ma sensu go sprawdzać
    :param driver: bot selenium, ponieważ tworzenie za każdym razem zajmuje bardzo dużo czasu to raz stworzona
    zmianna jest ciągle przekazywana
    :return: True jeżeli string jest linkiem
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    # Jeżeli driver nie będzie będzie obiektem selenium to taki zostanie utworzony
    isRealDriver = True;
    if type(driver) != webdriver.Chrome:

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

        isRealDriver = False

    # Jeżeli link jest w bazie to nie ma po co łączyć się ze stroną
    for element in database:
        if link == element:
            print(f"Link {link} jest już w bazie")
            if not isRealDriver:
                driver.quit()
            return True
    # Jeżeli w linku nie ma elemntów charakterystycznych dla linku to nie ma sensu go sprawdzać
    if repetedLinks[0] in link or repetedLinks[1] in link:

        # from selenium import webdriver
        # from selenium.webdriver.chrome.options import Options

        # chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # driver = webdriver.Chrome(options=chrome_options)

        # Jeżeli link się nie wysypie to ozancza że istnieje
        try:
            driver.get(link)
            # driver.quit()
            print(f"Linku {link} nie ma jeszcze w bazie")
            # driver.quit()
            if not isRealDriver:
                driver.quit()
            return True
        except:
            print(f"{link} nie jest linkiem")
            if not isRealDriver:
                driver.quit()
            return False
    #return False


def makeDatabase() -> None:
    """
    Sprawdza czy istenieje już baza danych linków, jeżeli nie to tworzy ją
    """

    import os
    try:
        os.listdir(os.getcwd() + "\\" + metaFileNames["database"])
    except:
        os.makedirs(os.getcwd() + "\\" + metaFileNames["database"])


def isDatabase() -> bool:
    """
    Tylko sprawdza czy istnieje baza danych, nic nie tworzy
    :return: True jeżeli istnieje
    """
    import os
    try:
        os.listdir(os.getcwd() + "\\" + metaFileNames["database"])
        return True
    except:
        return False


def makeNameFromLink(pageLink: str, type: str) -> str:
    """
    Zmienia podany link na unikalną nazwę pliku z podanym rozserzeniem
    :param pageLink: link na podstawie którego ma zostać stowrzona nazwa
    :param type: rozszerzenie pliku
    :return: gotową nazwę pliku
    """
    #Tworzona jest nazwa pliku bazy danych na podstawie linku
    fileName = ""
    for letter in pageLink:
        if letter.isdigit() or letter.isalpha():
            fileName = fileName + letter

    if type != "":
        return (fileName + "." + type)
    else:
        return fileName


def moduleInstaller() -> bool:
    """
    Sprawdza czy wszystkie dodatkowe biblioteki są zainstalowane, jeżeli nie to instaluje i zwraca informację
    czy wymagana była instalacja
    :return: True jeżeli niezbędna była instalacja
    """

    # Zawsze zainstalowane niezbędne do instalowanie modułów
    import subprocess
    import sys
    wasUpdated = False

    #Instaluje pakiety jeżeli któregoś nie ma

    try:
        import selenium
    except :
        subprocess.check_call([sys.executable, "-m", "pip", "install","selenium"])
        wasUpdated = True
    try:
        import codecs
    except :
        subprocess.check_call([sys.executable, "-m", "pip", "install","codecs"])
        wasUpdated = True
    try:
        import urllib
    except :
        subprocess.check_call([sys.executable, "-m", "pip", "install","urllib"])
        wasUpdated = True
    try:
        import time
    except :
        subprocess.check_call([sys.executable, "-m", "pip", "install","time"])
        wasUpdated = True
    try:
        import requests
    except :
        subprocess.check_call([sys.executable, "-m", "pip", "install","requests"])
        wasUpdated = True
    try:
        import lxml
    except :
        subprocess.check_call([sys.executable, "-m", "pip", "install","lxml"])
        wasUpdated = True
    try:
        import bs4
    except :
        subprocess.check_call([sys.executable, "-m", "pip", "install","bs4"])
        wasUpdated = True
    try:
        import re
    except :
        subprocess.check_call([sys.executable, "-m", "pip", "install","re"])
        wasUpdated = True
    try:
        import pandas
    except :
        subprocess.check_call([sys.executable, "-m", "pip", "install","pandas"])
        wasUpdated = True
    try:
        import os
    except :
        subprocess.check_call([sys.executable, "-m", "pip", "install","os"])
        wasUpdated = True
    try:
        import openpyxl
    except :
        subprocess.check_call([sys.executable, "-m", "pip", "install","openpyxl"])
        wasUpdated = True
    try:
        import git
    except:
        subprocess.check_call([sys.executable, "-m", "pip", "install","gitpython"])
        wasUpdated = True

    return wasUpdated



def addLog(logType: str, info: str) -> None:
    """
    Dodatje logi do rejestru
    :param logType: rodzaj logu którty ma zostać dodany
    :param info: inforamcja która ma zozstać zapisana
    """

    # Try catch dla upewnienia że wszystko się zapisze
    addLog = 0
    if isFile(metaFileNames["logs"]):
        addLog = open(metaFileNames["logs"], "a+")
    else:
        addLog = open(metaFileNames["logs"], "w+")

    from datetime import datetime
    currentDate = datetime.now()

    addLog.write(currentDate.strftime("%d/%m/%Y %H:%M:%S") + "  " + logLogs[logType] + " " + info + "\n")
    addLog.close()


def isDir(dir: str) -> bool:
    """
    Sprawdza czy pogana ścieżka istnieje
    :param dir: link do ścież która ma zostać sprawdzona
    :return: True jeżeli istnieje
    """
    import os
    return os.path.exists(dir)


def recLoad(data: dict, i: int) -> dict:
    """
    Rekurencyjnie wczytuje dane z pliku i zmienia je na struktury wygodne dla pythona (Dictionary, list)
    Dodawanie Dictionary do Array nie ma sensu!!!
    :param data: dane po wczytaniu które zostaną zwrócone
    :param i: poziom odczytu na którym znajduje się obecnie funkcja rekurencyjna
    :return: dane z pliku w strukturze pythona
    """

    title = ""
    isArr = False
    arr = []
    levelDick = {}
    while(i<len(data)):
        element = data[i]
        if element != "" and element != "," and element != "=":
            if element[0] != "\"":
                if i+2 < len(data) and data[i+2] == "{" :
                    returnedDick, i = recLoad(data, i+3)
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
                    title = element
                    isArr = True
                    arr.clear()
                    i += 2

                else:
                    levelDick[element] = data[i+2].replace("\"", "").replace("_", " ")
                    i+=2

            else:
                if isArr:
                    arr.append(element.replace("\"", "").replace("_", " "))

        i+=1

    return levelDick, i


def loadDataFromFile(fileName: str) -> dict:
    """
    Wstępnie przygotowuje pliki przed ich przetworzeniem do struktury pythona: wczytuje z pliku i pozbywa się
    zbędnych białych znasków
    :param fileName: nazwa pliku do wczytania
    :return: wczytane dane
    """

    essentialElement = [[], []]
    if fileName in txtEssential.keys():
        essentialElement = txtEssential[fileName]

    diction = {}

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

        diction, i = recLoad(loadedData, 0)

    else:
        print(f"Baza danych  \"{fileName}\" nie istnieje, stworzono automatycznie")

    isValid, validChecked = checkValid(essentialElement[0], diction)
    if not isValid:
        print(
            f"Inforamcja w bazie \"{fileName}\" nie są kompletne, uzupełniono automatycznie, prosze sprawdzić po zakończeniu programu")
        for val, type in zip(validChecked, essentialElement[1]):
            if not validChecked[val]:
                print(f"Brak informacji \"{val}\", uzupełniono automatycznie")
                if type == []:
                    diction[val] = []
                else:
                    diction[val] = {}

                saveDataToFile(fileName, diction)
    return diction


# # Rekurencyjnie wczytuje pliki
# def recLoad(data, i):
#     title = ""
#     isArr = False
#     arr = []
#     levelDick = {}
#     while(i<len(data)):
#         element = data[i]
#         if element != "" and element != "," and element != "=":
#             if element[0] != "\"" :
#                 if i+2 < len(data) and data[i+2] == "{":
#                     returnedDick,i = recLoad(data, i+3)
#                     if isArr:
#                         toDiction = {}
#                         toDiction[element] = returnedDick
#                         arr.append(toDiction)
#                     else:
#                         levelDick[element] = returnedDick
#                 elif element == "}":
#                     return levelDick, i
#                 elif element == "]":
#                     copyToSave = []
#                     copyToSave.extend(arr)
#                     levelDick[title] = copyToSave
#                     isArr = False
#                 elif i+2 < len(data) and data[i+2] == "[":
#                     title  = element
#                     isArr = True
#                     arr.clear()
#                     i+=2
#
#                 else:
#                     levelDick[element] = data[i+2].replace("\"", "").replace("_", " ")
#                     i += 2
#
#             else:
#                 if isArr:
#                     arr.append(element.replace("\"", "").replace("_", " "))
#
#         i += 1
#
#     return levelDick, i


def checkGrandSpaces(data: str) -> str:
    """
    Zmiania spacje w stringu na znak "_"
    :param data: string w którym należy zastąpić spacje
    :return: string z zastąpionymi spacjami
    """

    data = data.replace(" ", "_")
    return data


# Przygotowywuje dane przed ich zapisaniem
def saveDataToFile(fileName: str, dataToSave: dict) -> None:
    """
    Przygotowuje plik przed rekurencyjnym zapisaem danych
    :param fileName: nazwa pliku do któego mają zostać zapisane dane
    :param dataToSave: dane do zapisania
    """

    file = open(fileName, "w+")
    recSave(file, dataToSave)


def recSave(saveFile: open, dataToSave: dict) -> None:
    """
    Rekurencyjnie przetwarza dane przed ich zapisaniem do pliku a'al json i zapisauje
    :param saveFile: otawrty plik do którego mają zostać zapisane dane
    :param dataToSave: dane do zapisania
    """

    for data, name in enumerate(dataToSave):
        if type(dataToSave[name]) == str:
            saveFile.write(name + " = \"" + checkGrandSpaces(dataToSave[name]) + "\",\n")
        elif type(dataToSave[name]) == dict:
            saveFile.write(name + " = {\n")
            recSave(saveFile, dataToSave[name])
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


def checkIfDictionElementExists(diction: dict, elementName: str) -> bool:
    """
    Sprawdza czy dany element występuje w dictionary, używane przy wczytywaniu plików
    :param diction: dictionary do przeszukania
    :param elementName: nazwa szukanego elementu
    :return: True jeżeli element instnieje w dictionaty
    """

    try:
        diction[elementName]
        return True
    except:
        print("FALSE")
        return False

def isConnected() -> bool:
    """
    Łączy się z podaną bazą i sprawdza czy jest połączenie z internetem
    :return: True jeżeli jest połączenie
    """

    import requests
    host = "https://www.google.pl/"
    try:
        requests.get(host)
        return True
    except requests.ConnectionError:
        print("false")
        return False


def whileNotIsConnected() -> bool:
    """
    Czeka określony czas na połączenie z internetem. Jeżeli go nie uzyska wyłącza program
    :return: True jeżeli uzyska połączenie
    """
    import time
    import Dictionary as Dict
    timeInSeconds = 0
    while not isConnected():
        print("Czekam na połączenie z internetem")
        time.sleep(10)
        timeInSeconds += 1
        if timeInSeconds == 50:
            Dict.addLog("noInternet", "")
            return False

    return True


def NAFileLoc() -> str:
    """
    Szuka lokalizacji pliku zapisu po nazwie urządzenia, jeżeli nie znajdzie to włącza funkcję która prosi o podanie
    :return: Ścieżkę do folderu
    """

    import Dictionary as Dict
    import os
    data = Dict.loadDataFromFile(Dict.metaFileNames["NALoc"])

    pcName = os.environ["COMPUTERNAME"]

    for a, name in enumerate(data["Loc"]):
        if name == pcName:
            return data["Loc"][name]

    pathToNA = input("Brak informacji o punkcie zapisu na tym urządzniu. Wklej ścierzkę do folderu:")
    isPath = False
    while True:
        if Dict.isDir(pathToNA):
            print("Ścieżka jest poprawna")
            data["Loc"][pcName] = pathToNA
            Dict.saveDataToFile(Dict.metaFileNames["NALoc"], data)
            return pathToNA
        else:
            pathToNA = input("Ścieżka jest niepoprawna, podaj poprawną ścieżkę: ")


def loadNewArticles() -> list:
    """
    Wczytuje plik NewArticles o ile istenieje
    :return: zwraca listę linków
    """
    if isFile(NAFileLoc() + "\\" + metaFileNames["newArticles"]):
        links = []
        # with open:
        newArticlesLoadFile = open(NAFileLoc() + "\\" + metaFileNames["newArticles"], "r")
        for line in newArticlesLoadFile:
            if line.startswith(repetedLinks[0]):
                links.append(line)
        return links


def saveNewArticlesV2(isBoot: bool) -> None:
    """
    Zapisuje plik wynikowy newArticles.
    Nowa forma zapisu plików wynikowych
    Zbiera pojedyncze pliki z folderu tempDatabase które zawierają wyniki z każdej sprawdzanej strony
    i zapisuje je do jednego pliku wynikowego
    :param isBoot: True jeżeli program startuje z bool, False jeżeli został włączony inaczej
    :return: nic nie zwraca, po prostu opuszcza funkcję
    """
    import os
    nATempDatabase = os.getcwd() + doubleS + metaFileNames["tempDb"]  # \\tempDatabase
    if not isDir(nATempDatabase):
        if not isBoot :
            print("Brak nowych artykułów")
        return

    tempDatabaseList = os.listdir(os.getcwd() + doubleS + metaFileNames["tempDb"])  # + "\\tempDatabase")
    if len(tempDatabaseList) == 0:
        if not isBoot:
            print("Brak nowych artykułów")
        os.removedirs(os.getcwd() + "\\tempDatabase")
        return

    if not isBoot:
        print(NAFileLoc() + "\\" + metaFileNames["newArticles"])
    newArticlesSaveFile = open(NAFileLoc() + "\\" + metaFileNames["newArticles"], "a+")

    from datetime import datetime
    currentDate = datetime.now()
    newArticlesSaveFile.write("\n" + currentDate.strftime("%d/%m/%Y %H:%M:%S") + "\n")

    for file in tempDatabaseList:
        tempFile = open(metaFileNames["tempDb"] + doubleS + file, "r")  # "tempDatabase\\"

        for line in tempFile:
            newArticlesSaveFile.writelines(line)
        #Rozdziela pustą linią różne strony
        newArticlesSaveFile.writelines("\n")

        newArticlesSaveFile.writelines("")
        tempFile.close()
        if not isBoot:
            print(metaFileNames["tempDb"] + doubleS + file)  # "tempDatabase\\"
        os.remove(metaFileNames["tempDb"] + doubleS + file)  # "tempDatabase\\"

    newArticlesSaveFile.close()
    os.removedirs(os.getcwd() + doubleS + metaFileNames["tempDb"])  # "\\tempDatabase"


def cleanAfterError() -> None:
    """
    Jeżeli podczas poprzedniego wywołania programu wystąpił błąd to funkcja sprząta
    i zapisuje to co nie zostało poprzednio zapisane
    """

    import os
    if isDir(os.getcwd() + doubleS + metaFileNames["tempDb"]):
        print("Naprawa po awarii")
        saveNewArticlesV2(True)


def make_choice(instruction: str, elementList: list) -> int:
    """
    Zadaje pytanie i porównuje odpowiedz z listą, jeżeli pasuje to zwraca wynik
    :param instruction: pytanie które zostanie zadane
    :param elementList: lista możliwych odpowiedzi do wyboru
    :return: numer odpowiedzi licząc od 1
    """

    if len(elementList) != 0:
        print(instruction)
        i = 1
        for element in elementList:
            print(str(i) + ".	" + element.replace("\n", ""))
            i += 1
        choice = 0
        i -= 1
        while choice < 1 or choice > i:
            choice = input("Wybierz: ")
            if choice.isdigit():
                choice = int(choice)
                if choice < 1 or choice > i:
                    print("Nie ma takiego wyboru")
            else:
                print("Nie ma takiego wyboru")
                choice = 0
        print()
        return choice
    print()
    return 0


def checkValid(validity: [str, list[list[str] | list[list]] | list[list[str] | list[dict]]], diction:  dict[str, list[dict]]) \
        -> [bool, dict[object, bool]]:
    """
    Sprawdza czy w pliku nie brakuje niezbędnych danych, czy nie jest uszkodzony
    :param validity: wskazówki poprawności
    :param diction: dictionary do sprawdzenia
    :return: listę poprawności
    """

    validityDick = {}
    for val in validity:
        validityDick[val] = False

    validityDick = recValid(validityDick, diction)
    for val in validityDick:
        if not validityDick[val]:
            return [False, validityDick]

    return [True, []]


def recValid(validityDick: object, diction: object) -> object:
    """
    Sprawdza poprawność danych wejściowych rekurencyjnie
    ???Powyższa wunkcja rekurencyjnie???
    :param validityDick: wskazówki poprawności
    :param diction: dictionary do sprawdzenia
    :return: listę poprawności
    """
    dictType = type({})
    if type(diction) == dictType:
        for dict in diction:
            if dict in validityDick.keys():
                validityDick[dict] = True
            if type(diction[dict]) == dictType:

                validityDick = recValid(validityDick, diction[dict])
    return validityDick


def checkIfExcelFileIsOpen() -> bool:
    """
    Sprawdza czy wszystkie pliki danych (xlsx) nie są uszkodzone lub otwarte, jeżeli napotka problem wstrzymuje program
    :return: True jeżeli napotka problem
    """
    import os
    import pandas
    exceptList = []
    wasException = False
    xlsxList = os.listdir(metaFileNames["database"] + doubleS)
    for file in xlsxList:
        if "xlsx" in file:
            try:
                pandas.read_excel(metaFileNames["database"] + doubleS + file)
            except:
                exceptList.append(file)
                wasException = True

    if wasException:
        print("Niektórych plików nie da się otworzyć, mogą być otwarte, napraw to i uruchom ponownie")
        print("Błędne pliki")
        for file in exceptList:
            print(file)

    return wasException

# Ostrzeżenie przed wywołaniem
if __name__ == "__main__":
    print("Biblioteka Dictionary nie została stworzona do samodzielnego uruchamiania,"
          " zalecane jest jej importowanie")