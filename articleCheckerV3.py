"""
Program ten scrapuje wybrane treści z interntu, sprawdza czy spełniają one kryteria, zapisuje do bazy danych i pliku wynikowego
"""

import Dictionary as Dict
import bs4


def getLinksFromPage(pageLink: str) -> bs4.BeautifulSoup:
    """
    Pobiera wsszystkie linki ze strony
    :param pageLink: link do strony która ma zostać sprawdzona
    :return: zwraca pobrany kod strony sformatowany w bs4
    """

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    import Dictionary as Dict
    import bs4
    from time import sleep
    import os

    print("Łączę z: " + pageLink)
    if Dict.isLink(pageLink, [], ""):

        Dict.addLog("PrepChrom", "")
        # Jeżeli system ma działać w tle to trzeba zainportować options i dodać headless
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        Dict.addLog("ChromStarted", "")

        # Sprawdza czy dla wybranej strony nie trzba się zalogować
        # Jeżeli skrypt logowania jest dostępny to wywołuje
        if Dict.metaFileNames["logIn"] in os.listdir():
            if Dict.makeNameFromLink(pageLink, "py") in os.listdir(Dict.metaFileNames["logIn"]):
                print("Logowanie do ", pageLink, " jest wymagane")
                execImportFile = Dict.makeNameFromLink(pageLink, "")
                # Ponieważ importowany jest zawsze skrypt dla konkretnego linku to musi być on wywołyaany za pomocą "exec"
                exec(f"from logIn import {execImportFile} as scr")
                exec("driver = scr.logIn(driver, pageLink)")
            else:
                print("Logowanie do ", pageLink, " nie jest wymagane")
        else:
            print("Nie ma folderu ze skryptami do logowań")

        driver.get(pageLink)
        sleep(5)
        driver.execute_script("return document.getElementsByTagName(\"html\")[0].innerHTML")
        sleep(5)
        better_web = bs4.BeautifulSoup(driver.page_source, "lxml")
        driver.quit()
        return better_web
    else:
        print(pageLink, " nie jest linkiem")
        Dict.addLog("LinkErr", pageLink)


def getLinks() -> dict:
    """
    Pobiera linki do sprawdzenia z pliku txt
    :return: zwraca wczytane z pliku linki lub posty dictionaty jeżeli nie było nic dowczytania
    """

    fileData = Dict.loadDataFromFile(Dict.metaFileNames["pages"])
    if fileData == {}:
        return {}
    else:
        return fileData



def isRepeated(link: str, pageLink: str) -> bool:
    """
    Sprawdza czy w wybranym linku nie doszło do błędnego powtórzenia domeny
    :param link: link sprawdzany w ramach poprawności
    :param pageLink: link strony sprawdzanej
    :return: True jeżeli jest poprawny, False jeżeli nie
    """
    import re
    pageLink = Dict.onlyData(pageLink, Dict.repetedLinks)
    reFound = re.findall(pageLink, link)

    if len(reFound) > 1:
        for element in reFound:
            print("    " + element)
        return True
    else:
        return False

#Zakomentowane bo wywoływało błędy
'''def manageLinks(pageLink: str, better_web: bs4.BeautifulSoup, newArticles: list[str,str]) -> list[str,str]:'''
def manageLinks(pageLink, better_web, newArticles):
    """
    Spis treści funkcji bo jest bardzo duża :
        1. Sprawdzenie czy kod źródłowy strony oraz baza danych linków istanieje
        2. Wybranie linków z kodu strony i sprawdzenie  czy istanieją
        3. Sortuje tablicę linków i nazw po linkach i rozdziela na mniejsze tablice
        4. Usuwa powtózenia linków i wybiera jeden tytuł
        5. Jeżeli baza danych funkcji już instanieje to pobiera wszystkie zapisane w niej linki i porównuje czy któreś z nowych nie były już wcześniej pobrane
        6. Sprawdza czy linki nie są wykluczone lub wymagane
        7. Zapisuje dane do excela wzbogacone o świeżo poprane linki
        8. Jeżeli baza danych nie istanieje to zapisuje wszytkie linki do excela i nie zwraca newArticles
        Z pobranych linków wyodrębnia te które są nowe

    :param pageLink: link do strony sprawdzanej
    :param better_web: pobrany kod strony sformatowany w bs4
    :param newArticles: lista do której zostaną zapisane wyniki
    :return: listę z nazwami i linkmi do zapisania
    """

    import Dictionary as Dict
    import os
    import pandas
    import re
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    # 1

    # Jeżeli strona nie odpowiedziała i jej kod źródłowy nie istnieje to program się nie wykona
    if not better_web:
        return

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # Sprawdza czy baza danych istnieje i ją otwiera
    fileList = os.listdir(os.getcwd() + "\\" + Dict.metaFileNames["database"])
    fileName = Dict.makeNameFromLink(pageLink, "xlsx")
    excelData = [[], []]
    if fileName in fileList:
        dataFromExcel = pandas.read_excel(Dict.metaFileNames["database"] + "\\" + fileName)
        i = 0
        excelLen = len(dataFromExcel["Links"])
        # Wczytuje wszystkie dane z bazy danych
        while i < excelLen:
            excelData[0].append(dataFromExcel["Links"][i])
            excelData[1].append(dataFromExcel["Names"][i])
            i += 1

    # 2

    # Nie potrafiłem przesortować tablicy po dwóch elementach więc trzeba go połączyć w jeden i przesortować, Dict.comma rodziela link od nazwy
    linkAndName = []

    # Szuka linków w kodzie strony (linki to "a")
    better_web2 = better_web.find_all("a")
    for link in better_web2:

        # Sprawdza czy jest to link
        tempLink = re.findall("href=\".[^\"]*\"", str(link))
        tempName = re.findall(">.*?<", str(link))

        # Sprawdza czy link i nazwa istanieje
        if tempName and tempLink:

            tempNameA = []
            [tempNameA.append(element.replace("<", "").replace(">", "").strip()) for element in tempName]
            tempName = tempNameA
            tempNameA = []
            [tempNameA.append(element) for element in tempName if element and len(element) != 0]
            tempName = tempNameA

            tempLink = tempLink[0].replace("href=\"", "").replace("\"", "").strip()

            if Dict.isLink(tempLink, excelData[0], driver):
                if len(tempName) != 0:
                    for name in tempName:
                        linkAndName.append(tempLink + Dict.comma + name)
                else:
                    linkAndName.append(tempLink + Dict.comma + "")
            # Na dynamicznych stronach nie ma adresu głównego są tylko adresy wewnętrze które zaczynają się od "/",
            #   należy do nich dodać adres główny

            elif not tempLink.startswith("http"):
                if tempLink.startswith("/"):
                    if Dict.isLink(makeTheMainLink(pageLink) + tempLink, excelData[0], driver):
                        if len(tempName) != 0:
                            for name in tempName:
                                linkAndName.append(makeTheMainLink(pageLink) + tempLink + Dict.comma + name)
                        else:
                            linkAndName.append(makeTheMainLink(pageLink) + tempLink + Dict.comma + "")
                else:
                    if Dict.isLink(makeTheMainLink(pageLink) + "/" + tempLink, excelData[0], driver):
                        if len(tempName) != 0:
                            for name in tempName:
                                linkAndName.append(makeTheMainLink(pageLink) + "/" + tempLink + Dict.comma + name)
                        else:
                            linkAndName.append(makeTheMainLink(pageLink) + "/" + tempLink + Dict.comma + "")

        # 3
    linkAndName = sorted(linkAndName)

    sortedDataFromPage = [[], []]

    for element in linkAndName:
        element = element.split(Dict.comma)
        sortedDataFromPage[0].append(element[0])
        sortedDataFromPage[1].append(element[1])

    # 4

    # Usuwa duplikaty linków i zostawia ten który ma najbardziej tytułowy tytuł
    links = []
    names = []
    i = 0
    startSeries = False

    # Działa tak długo aż przejdzie przez wyzstkie linki pobrane ze strony
    while i < len(sortedDataFromPage[0]):

        # Jeżeli obecny element nie jest ostatnim to sprawdza czy kolejny link nie jest taki sam
        if i < len(sortedDataFromPage[0]) - 1 and sortedDataFromPage[0][i] == sortedDataFromPage[0][i + 1]:

            # Jeżeli link i oraz i+1 są takie same to oznazca że rozpoczęła się seria identycznych linków z których
            #   należy zostawić tylko jeden
            if startSeries == False:
                startSeries = True
                starSeriesPosition = i

        # Jeżeli link i jest różny od i+1 i startSeries == True to oznacza że skńczyła się seria i
        #   trzeba wybrać jeden z linków
        elif startSeries == True:
            startSeries = False
            bestToTitle = sortedDataFromPage[1][starSeriesPosition]
            bestToLink = sortedDataFromPage[0][starSeriesPosition]
            bestTitleLocation = starSeriesPosition
            j = starSeriesPosition
            while j < i + 1:
                if not Dict.isLink(sortedDataFromPage[1][j], excelData[0], driver) and len(bestToTitle) < len(
                        sortedDataFromPage[1][j]):
                    bestToTitle = sortedDataFromPage[1][j]
                    bestToLink = sortedDataFromPage[0][j]
                    bestTitleLocation = j
                j += 1
            links.append(bestToLink)
            names.append(bestToTitle)

        # Jeżeli nie ma żadnej serii linków ale jest to ostatni element to dodaje ostatni link
        else:
            links.append(sortedDataFromPage[0][i])
            names.append(sortedDataFromPage[1][i])

        i += 1

    #Driver nie będzie już więcej potrzebny bo nie będzie sprawdzania linku
    driver.quit()

    # 5
    # Jeżeli plik danej strony już istnieje
    if len(excelData[0]) != 0:
        newDataToExcel = [], []

        # Ponieważ podczas zapisywania nowych danych wszystki w excel wszystko jest usuwane to trzeba od nowa zapisać całą bazę
        # Najpierw przepisuje wszystkie stare linki
        i = 0
        excelLen = len(excelData[0])
        while i < excelLen:
            newDataToExcel[0].append(excelData[0][i])
            newDataToExcel[1].append(excelData[1][i])
            i += 1
        # Przechodzi przez pobrane właśnie linki i jeżeli jakieś są już w bazie to je usuwa
        i = len(links) - 1
        while i >= 0:
            for excelLink in excelData[0]:
                if excelLink == links[i]:
                    links.pop(i)
                    names.pop(i)
                    break
            i -= 1

        # 6

        # Sprawdza czy linki nie są wykluczone lub wymagane
        data = ""
        if Dict.isFile(Dict.metaFileNames["database"] + "\\" + Dict.makeNameFromLink(pageLink, "txt")):
            data = Dict.loadDataFromFile(Dict.metaFileNames["database"] + "\\" + Dict.makeNameFromLink(pageLink, "txt"))
        keyed = []
        blocked = []
        if isinstance(data, dict):
            try:
                keyed = data["key"]
                blocked = data["block"]
            except:
                fileName = Dict.metaFileNames["database"] + "\\" + Dict.makeNameFromLink(pageLink, "txt")
                print(f"Plik wykluczeń {fileName} jest uszkodzony! NAPRAW GO")
                os.renames(Dict.metaFileNames["database"] + "\\" + Dict.makeNameFromLink(pageLink, "txt"), Dict.metaFileNames["database"] + "\\" + Dict.makeNameFromLink(pageLink + "ERROR", "txt"))

        tempPageLink = makeTheMainLink(pageLink)
        for element in Dict.repetedLinks:
            tempPageLink = tempPageLink.replace(element, "")

        keyed.append(tempPageLink)

        i = 0
        while i < len(links):
            wasBreak = False
            wasBlock = False
            newDataToExcel[0].append(links[i])
            newDataToExcel[1].append(names[i])
            if keyed != []:
                for key in keyed:
                    if key in links[i]:
                        if blocked != []:
                            for block in blocked:
                                if block in links[i]:
                                    wasBlock = True
                                    break
                            if not wasBlock:
                                newArticles.append(names[i])
                                newArticles.append(links[i])
                        else:
                            newArticles.append(names[i])
                            newArticles.append(links[i])

            elif blocked != []:
                for block in blocked:
                    if block in links[i]:
                        wasBreak = True
                        break
                if not wasBreak:
                    newArticles.append(names[i])
                    newArticles.append(links[i])
            else:
                newArticles.append(names[i])
                newArticles.append(links[i])

            i += 1

        # 7

        excelWriter = pandas.ExcelWriter(Dict.metaFileNames["database"] + "\\" + fileName)
        dataF = pandas.DataFrame({"Links": newDataToExcel[0], "Names": newDataToExcel[1]})
        dataF.to_excel(excelWriter, "1", index=False)
        excelWriter.save()
        return newArticles

    # 8

    # Jeżeli meta plik danej strony jeszcze nie istanieje
    else:
        excelWriter = pandas.ExcelWriter(Dict.metaFileNames["database"] + "\\" + fileName)
        dataF = pandas.DataFrame({"Links": links, "Names": names})
        dataF.to_excel(excelWriter, "1", index=False)
        excelWriter.save()
        return newArticles


# Używane przez articleCheckerManager
# Chwilowo nieużywane
# def manualDatabaseUpdate(link, pageLink, managedArticles):
#     import Dictionary as Dict
#     managedArticles = manageLinks(link, getLinksFromPage(pageLink), managedArticles)
#     return managedArticles


def saveLogIn() -> None:
    """
    Zapisuje datę ostatniego logowanie programu
    """

    from datetime import date
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")

    dataFile = open(Dict.metaFileNames["logInDate"], "w+")
    dataFile.write(d1)
    dataFile.close()


def readyToSync() -> bool:
    """
    Sprawdza czy program nie został już dziś zaktualizowany
    :return: True jeżeli nie został, False jeżeli został
    """

    from datetime import date
    if not Dict.isFile(Dict.metaFileNames["logInDate"]):
        return True
    else:
        dataFile = open(Dict.metaFileNames["logInDate"], "r+")
        dataLine = dataFile.readline()
        dataLine = dataLine.split("/")

        dataValue = int(dataLine[0]) + int(dataLine[1]) * 100 + int(dataLine[2]) * 10000

        today = date.today()
        passValue = int(today.strftime("%d")) + int(today.strftime("%m")) * 100 + int(today.strftime("%Y")) * 10000

        if dataValue < passValue:
            return True


def makeTheMainLink(currentLink: str) -> str:
    """
    Słóży do tworznia głównego linku bez podlinków po ukośnikach
    :param currentLink: link do zmienienia
    :return: zmieniony link
    """

    linkElements = currentLink.split("/")
    return linkElements[0] + "//" + linkElements[2]


def isChromDriver() -> bool:
    """
    Sprawdza czy jakikolwiek chromedriver jest zainstalowany
    :return: True jeżeli tak, False jeżeli nie
    """

    import os
    import Dictionary as Dict

    if Dict.metaFileNames["chrome"] in os.listdir():
        return True
    else:
        print("Brak sterowanika chromedriver, trwa pobieranie")
        return False


def isChromedriverUpToDate() -> bool:
    """
    Sprawdza czy chromedriver.exe działa i jest aktualny
    :return: True jeżeli jest aktualny, False jeżeli nie
    """

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    import Dictionary as Dict

    # Jeżeli system ma działać w tle to trzeba zainportować options i dodać headless
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(Dict.urlLinks["googlePage"])
        driver.quit()
        return True

    except: # selenium.common.exceptions.SessionNotCreatedException as e
        print("ChromeDriver.exe jest nieaktualny! Trwa Aktualizowanie")
        return False


def getCurrentVersion() -> str:
    """
    Sprawdza jaka jest aktualna wersja przeglądarki chrome
    :return: xwraca aktualną wersję przeglądarki
    """

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    import selenium
    import re

    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        webdriver.Chrome(options=chrome_options)

    except selenium.common.exceptions.SessionNotCreatedException as e:
        # W opinie rzuconego wyjątku szuka informacji o wersji
        firestPattern = re.findall("Current browser version is [\d.]* with binary path", str(e))
        # Z całego zdanie wyciąga tylko wersję
        secondPattern = re.findall(" [\d.]* ", firestPattern[0])
        return secondPattern[0].replace(" ", "")


def download(downloadUrl: str, pathToSave: str) -> None:
    """
    Pobiera plik ze wszkaznego linku i zpapisuje go pod wskazaną ścieżką.
    Może być względna, ostatni element to nazwa pliku
    :param downloadUrl: adres strony do pobrania pliku
    :param pathToSave: ścieżka do zapisania pliku
    """

    import requests
    from time import sleep

    r = requests.get(downloadUrl, allow_redirects=False)
    sleep(5)
    open(pathToSave, "wb+").write(r.content)


def extractZip(pathToFile: str, PathToSave: str) -> None:
    """
    Rozpakowuje podanego zipa do podanej ścieżki
    :param pathToFile: ścieżka do zipa
    :param PathToSave: ścieżka do rozpakowania
    """

    import zipfile

    with zipfile.ZipFile(pathToFile, "r") as zip:
        zip.extractall(PathToSave)


def removeAfterDownload() -> None:
    """
    Usuwa pozostałości po pobieraniu (wskazane pliki)
    """

    import os
    import Dictionary as Dict
    os.remove(Dict.metaFileNames["chromeZip"])


def threadCheeck(link: object) -> None:
    """
    Jest równloegłą funkcją wywoływaną osobno dla każdego linku
    :param link: link do strony
    """

    import os

    pageSourceCode = getLinksFromPage(link)
    newArticles = []
    manageLinks(link, pageSourceCode, newArticles)

    if len(newArticles) > 0:
        nATempDatabase = os.getcwd() + "\\tempDatabase"
        nATempSaveFile = os.getcwd() + "\\tempDatabase\\" + Dict.makeNameFromLink(link, "txt")
        if not Dict.isDir(nATempDatabase):
            os.makedirs(nATempDatabase)

        newArticlesTempFile = open(nATempSaveFile, "a+")

        for article in newArticles:
            try:
                newArticlesTempFile.write(article + "\n")
            except:
                for sign in article:
                    try:
                        newArticlesTempFile.write(sign)
                    except:
                        print("Znak błędu: ", sign)
                # dodac log error
                newArticlesTempFile.write("\n")

        newArticlesTempFile.close()


def filterForGroup(pageslinks: list, gGroup: str) -> dict:
    """
    Jeżeli została wywołana grupa to filtruje i zostawia tylko linki w niej zawarte
    :param pageslinks: linki do sprawdznia
    :param gGroup: wywołana grupa filtrowania
    :return: linki zawarte w grupie
    """

    fileData = Dict.loadDataFromFile(Dict.metaFileNames["groupFile"])[gGroup]
    filteredPageslinks = []

    pageslinks = pageslinks["title"]

    for number in fileData:
        filteredPageslinks.append(pageslinks[int(number)-1])

    filteredPageslinksInDictionary = {"title": filteredPageslinks}
    return filteredPageslinksInDictionary


def mainFunc(gGroup: str) -> None:
    """
    Główna funkcja, pozwala na uruchomienie z innego skryptu
    :param gGroup: nazwa grupy, jeżeli pusta to żadna grupa nie została wywołana
    """

    # Miernik czasu
    # import time
    # t_start = time.perf_counter()
    import Dictionary as Dict
    from time import sleep
    Dict.moduleInstaller()
    Dict.addLog("ProgStart", "")

    # Sprawdza czy dziś nie doszło już do synchronizacji
    if readyToSync():
        if not Dict.whileNotIsConnected():
            exit(0)

        # Ścieżka do zapisu zawartosci pliku zip
        PathToSaveExtract = ""

        #Sprawdza czy chromedriver w ogóle istnieje
        if not isChromDriver():
            # Jeżeli nie to pobiera wskazany z internetu
            # Nie byłem w stanie sprawdzić wersji przeglądarki chrome więc najpierw trzba pobrać losowy chromerdriver
            # a potem sparwdzić wersję i jeszcze raz pobrać odpowieni
            download(Dict.urlLinks["chromeDriverDownloadPermLink"], Dict.metaFileNames["chromeZip"])
            extractZip(Dict.metaFileNames["chromeZip"], PathToSaveExtract)

        # Sprawdza czy chromedriver jest aktulany
        if not isChromedriverUpToDate():
            # Sprawdza wersję aktualnej wersji
            version = getCurrentVersion()
            # Link do pobrania
            currentDownloadUrl = Dict.urlLinks["chromeDriverDownloadCurrLinkBegin"] + str(version) + Dict.urlLinks["chromeDriverDownloadCurrLinkEnd"]
            download(currentDownloadUrl, Dict.metaFileNames["chromeZip"])
            extractZip(Dict.metaFileNames["chromeZip"], PathToSaveExtract)
            # Usuwa niepotrzebne pliki (tu zip po pobieraniu)
            removeAfterDownload()

        pageslinks = getLinks()

        if gGroup != "":
            pageslinks = filterForGroup(pageslinks, gGroup)

        Dict.makeDatabase()
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as thread:

            for i, link in enumerate(pageslinks["title"]):
                sleep(5)
                if link:
                    thread.submit(threadCheeck, link)

        from time import sleep
        print("Czekam na zamknięcie wątków")
        sleep(5)
        print("Wątki zamknięte")

        Dict.saveNewArticlesV2(False)
    # Miernik czasu
    # t_stop = time.perf_counter()

    else:
        Dict.addLog("ProgEndDJZ", "")
        print("Dziś już zaktualizowano")


if __name__ == "__main__":

    import sys
    argList = [sys.argv[0]] + [element.replace("-", "") for element in sys.argv[1:]]

    if len(sys.argv) > 1 and argList[1] == "m":
        print("Włączono działanie manualne, synchronizacja z git zostanie pominięta")
        if Dict.checkIfExcelFileIsOpen():
            exit(0)
        mainFunc()
    else:
        print("Do włącznia tego skryptu z pominięciem boota trzeba dodać przełącznik \"m\", "
              "pomijanie nie jest jednak zalecane bo omija synchronizacje z git")