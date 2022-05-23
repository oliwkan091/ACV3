"""
Plik ten daje użytkownikowi dostęp do programu i pozwala nim zarządzać
"""


def show_links(metaFileNames: str) -> None:
    """
    Pokazuje wszystkie linki które są w bazie
    :param metaFileNames: nazwa pliku gdzie zapisane są linki
    :return: wyłącze funkcję, nic nie zwraca
    """

    import Dictionary as Dict

    pages = Dict.loadDataFromFile(metaFileNames)
    try:
        pages["title"]
    except:
        print("Baza danych nie istenieje")
        return

    titlePages = pages["title"]
    if titlePages != []:
        i = 0
        while i < len(titlePages):
            print(str(i + 1) + ". " + titlePages[i])
            i += 1
    else:
        print('W bazie nie ma linków')


def add_link(metaFileNames: str) -> None:
    """
    Dodaje link strony do sprawdzenia do bazy
    :param metaFileNames: nazwa pliku z linkami
    """

    import Dictionary as Dict

    link = input("Wpisz link do strony: ")
    if Dict.isLink(link, []):
        links = Dict.loadDataFromFile(metaFileNames)
        if Dict.checkIfDictionElementExists(links, "title"):
            links["title"].append(link)
            Dict.saveDataToFile(metaFileNames, links)
            print("Link zapisany")
        else:
            print("Plik z linkami nie istnieje. Trwa tworznie")
            diction = {"title": link}
            Dict.saveDataToFile(metaFileNames, diction)
            print("Utworzono")

    else:
        print("Link nie istanieje lub witryna jest nieosiągalna. Sprawdź link i połączenie z internetem")


def remove_link(metaFileNames: str) -> None:
    """
    Usuwa wskazany link
    :param metaFileNames: nazwa pliku z linkami
    """

    import Dictionary as Dict

    links = Dict.loadDataFromFile(metaFileNames)
    if Dict.checkIfDictionElementExists(links, "title"):
        choice = Dict.make_choice("Wybierz który link chcesz usunąć", links["title"] + ["Wyjdź"])
        if choice != len(links["title"]) + 1:
            groupData = Dict.loadDataFromFile(Dict.metaFileNames["groupFile"])

            # Przechodzi przez grupy i sprawdza czy nie ma tam zapisanej strony która ma zostać usunięta
            for i in range(1, 4):
                currentGroup = "g" + str(i)
                if str(choice) in groupData[currentGroup]:
                    groupData[currentGroup].remove(str(choice))

                j = 0
                while j < len(groupData[currentGroup]):
                    if int(groupData[currentGroup][j]) > choice:
                        groupData[currentGroup][j] = str(int(groupData[currentGroup][j]) - 1)
                    j += 1

            Dict.saveDataToFile(Dict.metaFileNames["groupFile"], groupData)

            links["title"].pop(choice - 1)
            Dict.saveDataToFile(metaFileNames, links)
            print("Link usunięty")
    else:
        print("Baza linków nie istnieje")


def show_exceptions(metaFileNames: dict) -> None:
    """
    Pokazaju jakie wyjątki ma wybrany plik
    :param metaFileNames: dictionary z nawzwami plików
    """

    import Dictionary as Dict

    Dict.makeDatabase()
    links = Dict.loadDataFromFile(metaFileNames["pages"])

    if Dict.checkIfDictionElementExists(links, "title"):
        choice = Dict.make_choice("Z jakiego pliku wyświetlić wyjątki", links["title"])

        fileToOpenName = Dict.makeNameFromLink(links["title"][choice - 1], "txt")
        if Dict.isFile(metaFileNames["database"] + "\\" + fileToOpenName):
            exceptions = Dict.loadDataFromFile(metaFileNames["database"] + "\\" + fileToOpenName)

            # exceptions["block"] != []:
            if exceptions["block"]:
                print("Block:")
                for block in exceptions["block"]:
                    print("    " + block)
            # exceptions["key"] != []:
            if exceptions["key"]:
                print("Key:")
                for key in exceptions["key"]:
                    print("    " + key)

        else:
            print("Brak wyjątków")

    else:
        print("Baza danych nie istenieje")


def add_exception(metaFileNames: dict) -> None:
    """
    Dodaje wyjątek do wybranego pliku
    :param metaFileNames: dictionary z nawzwami plików
    """

    import Dictionary as Dict

    Dict.makeDatabase()
    links = Dict.loadDataFromFile(metaFileNames["pages"])

    if Dict.checkIfDictionElementExists(links, "title"):
        choice = Dict.make_choice("Wybierz do jakiego pliku chcesz dodać wyjątek", links["title"])
        typeChoice = Dict.make_choice(Dict.makeNameFromLink(links["title"][choice - 1], "txt") + "   Podaj typ wyjątku",
                                      Dict.exceptionTypes)
        excInp = input("Podaj wyjątek: ")
        excFile = Dict.loadDataFromFile(
            Dict.metaFileNames["database"] + "\\" + Dict.makeNameFromLink(links["title"][choice - 1], "txt"))
        if not Dict.checkIfDictionElementExists(excFile, "block") or not Dict.checkIfDictionElementExists(excFile,
                                                                                                          "key"):
            excFile["block"] = []
            excFile["key"] = []

        excFile[Dict.exceptionTypes[typeChoice - 1]].append(excInp)

        Dict.saveDataToFile(
            Dict.metaFileNames["database"] + "\\" + Dict.makeNameFromLink(links["title"][choice - 1], "txt"), excFile)
        print("Dodano wyjątek")

    else:
        print("Baza danych nie istnieje")


def remove_exception(metaFileNames: dict) -> None:
    """
    Usuwa wyjątek z wybranego pliku
    :param metaFileNames: dictionary z nazwami plików
    """

    import Dictionary as Dict

    Dict.makeDatabase()
    import os
    links = Dict.loadDataFromFile(metaFileNames["pages"])

    if Dict.checkIfDictionElementExists(links, "title"):
        i = 0
        while i < len(links["title"]):
            if not Dict.isFile(Dict.metaFileNames["database"] + "\\" + Dict.makeNameFromLink(links["title"][i], "txt")):
                links["title"].pop(i)
            i += 1

        choice = Dict.make_choice("Wybierz z jakiej bazy chcesz usunąć wyjątek", links["title"])

        exceptions = Dict.loadDataFromFile(
            Dict.metaFileNames["database"] + "\\" + Dict.makeNameFromLink(links["title"][choice - 1], "txt"))
        print(exceptions)
        if exceptions["block"] != [] and exceptions["key"] != []:
            typeChoice = Dict.make_choice("Który typ chcesz usunąć", Dict.exceptionTypes)
            toDel = Dict.make_choice("Który wyjątek chcesz usunąć", exceptions[Dict.exceptionTypes[typeChoice - 1]])

            exceptions[Dict.exceptionTypes[typeChoice - 1]].pop(toDel - 1)
        else:
            if exceptions["block"] != []:
                toDel = Dict.make_choice("Który wyjątek chcesz usunąć", exceptions[Dict.exceptionTypes[0]])
                exceptions[Dict.exceptionTypes[0]].pop(toDel - 1)
            else:
                toDel = Dict.make_choice("Który wyjątek chcesz usunąć", exceptions[Dict.exceptionTypes[1]])
                exceptions[Dict.exceptionTypes[1]].pop(toDel - 1)

        if exceptions["block"] == [] and exceptions["key"] == []:
            os.remove(Dict.metaFileNames["database"] + "\\" + Dict.makeNameFromLink(links["title"][choice - 1], "txt"))
        else:
            Dict.saveDataToFile(
                Dict.metaFileNames["database"] + "\\" + Dict.makeNameFromLink(links["title"][choice - 1], "txt"),
                exceptions)
    else:
        print("Baza danych nie istanieje")


def deleteNewArticles() -> bool:
    """
    Usuwa zapisane dane artykułów
    :return: True jeżeli plik istnieje, False jeżeli nie
    """

    import Dictionary as Dict
    import os

    if(Dict.isFile(Dict.NAFileLoc() + "\\" + Dict.metaFileNames["newArticles"])):
        os.remove(Dict.NAFileLoc() + "\\" + Dict.metaFileNames["newArticles"])
        return True
    else:
        return False


def open_browser(links: list) -> bool:
    """
    Wczytuje do przeglądarki strony
    :param links: lista linków zapisanych w newArticles
    """

    if not links:
        print("Brak linków do otworzenia")
        return False

    from selenium import webdriver

    driver_path = "chromedriver.exe"
    brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"

    option = webdriver.ChromeOptions()
    option.binary_location = brave_path
    # option.add_argument("--incognito") OPTIONAL
    # option.add_argument("--headless") OPTIONAL

    # Create new Instance of Chrome
    browser = webdriver.Chrome(executable_path=driver_path, chrome_options=option)
    browser.get(links[0])
    pagesNumber = range(0, len(links)-1)
    print("Wczytywanie")
    for link, i in zip(links,pagesNumber):
        browser.execute_script(f"window.open(\"about:blank\",\"{i}\");")
        browser.switch_to.window(f"{i}")
        browser.get(link)
    input("Naciśnij dowolny klawisz by zamknąć przeglądarkę")
    return True


def open_saved_links() -> None:
    """
    Wczytuje zapisane linki
    """

    import Dictionary as Dict

    if not open_browser(Dict.loadNewArticles()):
        return

    if not Dict.make_choice("Czy chcesz usunąć plik z zakładkami", ["Tak", "Nie"]) - 1:
        if deleteNewArticles():
            print("Usunięto")
        else:
            print("Błąd usuwania")
    else:
        print("Nie usunięto")


def edit_groups() -> None:
    """
    Odpowiada za edycję grup
    """

    import Dictionary as Dict

    # Jeżeli plik z grupami nie istnieje to go tworzy
    if not Dict.isFile(Dict.metaFileNames["groupFile"]):
        baseGroup = []
        baseData = {"g1": baseGroup, "g2": baseGroup, "g3": baseGroup}
        Dict.saveDataToFile(Dict.metaFileNames["groupFile"], baseData)
    # Wczytuje zawartość grupy
    fileData = Dict.loadDataFromFile(Dict.metaFileNames["groupFile"])

    groupChoice = Dict.make_choice("Co którą grupę chcesz edytować ?", list(fileData))
    groupChoiceName = "g" + str(groupChoice)

    linksFromFile = Dict.loadDataFromFile(Dict.metaFileNames["pages"])["title"]

    action = -1
    # Działa tak długo dopóki nie zostanie wybrane wyjście
    while action != 4:
        action = Dict.make_choice("Co chcesz zrobić ?", ["Zobaczyć zawartość grupy", "Dodać do grupy", "Usunąć z grupy", "Wyjść"])

        # Pokazuje linki przypisane do konkretnej grupy
        if action == 1:
            if len(fileData[groupChoiceName]) == 0:
                print("Brak elementów w grupie")
            else:
                for link in fileData[groupChoiceName]:
                    print(linksFromFile[int(link)-1])

        # Pozwala dodać nowe linki do grupy
        elif action == 2:
            linkuNumber = Dict.make_choice("Wybierz który link chcesz dodać do grupy: ", linksFromFile + ["Wyjście"])
            if linkuNumber != len(linksFromFile + ["Wyjście"]):
                if str(linkuNumber) in fileData[groupChoiceName]:
                    print("Link jest już w grupie")
                else:
                    fileData[groupChoiceName].append(str(linkuNumber))

        # POzwala usunąć linki z grup
        elif action == 3:

            if len(fileData[groupChoiceName]) == 0:
                print("Nie ma linków do usunięcia")
            else:
                # Ponieważ w pliku z grupami zapisane jest tylko położenie linków to by je wyświetlić trzeba je najpierw wczytać
                # LOVE Comprehensions
                listWithLinks = []
                listWithLinks = listWithLinks + [(linksFromFile[int(element) - 1]) for element in
                                                fileData[groupChoiceName]]
                linkuNumber = Dict.make_choice("Wybierz który link chcesz usunąć do grupy: ", listWithLinks + ["Wyjście"])

                if linkuNumber != len(listWithLinks + ["Wyjście"]):
                    fileData[groupChoiceName].pop(linkuNumber-1)

    Dict.saveDataToFile(Dict.metaFileNames["groupFile"], fileData)


# Dodaje linki z innej podstrony do wyznaczonej bazy danych
# Chwilowo nieużywane
# def manualManageLinks():
#     if Dict.isFile(Dict.metaFileNames['pages']):
#         txtFile = open(Dict.metaFileNames['pages'], 'r')
#         links = txtFile.readlines()
#         txtFile.close()
#
#         if len(links) != 0:
#             i = 0
#             linksLen = len(links)
#             while i < linksLen:
#                 links[i] = Dict.onlyData(links[i], Dict.pagesData)
#                 i += 1
#             choice = Dict.make_choice('Wybierz link którego strona pochodna ma zostać sprawdzona', links)
#
#             if choice != 0:
#
#                 pageLink = input("Podaj link do strony pochodnej która ma zostać sprawdzona: ")
#                 if Dict.isLink(pageLink, []):
#                     import articleCheckerV3 as ac3
#                     managedArticles = []
#                     managedArticles = ac3.manualDatabaseUpdate(links[choice - 2], pageLink, managedArticles)
#
#                     if len(managedArticles) != 0:
#                         print('Uzupełniono')
#                         for article in managedArticles:
#                             print(article)
#
#                     else:
#                         print('Nie dodadno żadnych linków')
#                 else:
#                     print('To nie jest link')
#         else:
#             print('Nie ma stron do sprawdzenia')
#     else:
#         print('Nie ma stron do sprawdzenia')


def genereate_name_from_link() -> None:
    """
     Wyświetla nazwę stworzoną z linku
    """

    import Dictionary as Dict

    pages = Dict.loadDataFromFile(Dict.metaFileNames["pages"])["title"]
    choice = Dict.make_choice("Z którego linku chcesz wygenerować nazwę: ", pages + ["Wyjdź"])

    if choice != len(pages) + 1:
        print(Dict.makeNameFromLink(pages[choice-1], ""))


def mainFunc() -> None:
    """
    Główna funkcja programu
    """
    import Dictionary as Dict

    if Dict.checkIfExcelFileIsOpen():
        exit(0)

    choice = 0
    while choice != 10:
        choice = Dict.make_choice("Wybierz co chcesz zrobić", Dict.mainMenu)

        if choice == 1:
            show_links(Dict.metaFileNames["pages"])
        elif choice == 2:
            add_link(Dict.metaFileNames["pages"])
        elif choice == 3:
            remove_link(Dict.metaFileNames["pages"])
        elif choice == 4:
            show_exceptions(Dict.metaFileNames)
        elif choice == 5:
            add_exception(Dict.metaFileNames)
        elif choice == 6:
            remove_exception(Dict.metaFileNames)
        elif choice == 7:
            open_saved_links()
        elif choice == 8:
            edit_groups()
        elif choice == 9:
            genereate_name_from_link()

        # Wykonywane jest teraz w boocie
        # elif choice == 9:
            # import gitManager as gm
            # gm.mainFunc("f")
            # exit(0)


if __name__ == "__main__":

    import sys
    import Dictionary as Dict

    # Usuwa "-" sprzed przełącznika
    argList = [sys.argv[0]] + [element.replace("-", "") for element in sys.argv[1:]]

    if len(sys.argv) > 1 and Dict.switches["manual"] in argList:
        print("Włączono działanie manualne, synchronizacja z git zostanie pominięta")
        mainFunc()
    else:
        print("Do włącznia tego skryptu z pominięciem boota trzeba dodać przełącznik \"m\","
              " pomijanie nie jest jednak zalecane bo omija synchronizacje z git ")
