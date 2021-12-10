'''
Plik ten daje użytkownikowi dostęp do programu i pozwala nim zarządzać
'''


import Dictionary as Dict

# Pokazuje wszystkie linki które są w bazie
def show_links(metaFileNames):
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


# Dodaje link strony do sprawdzenia do bazy
def add_link(metaFileNames, pagesData):
    link = input("Wpisz link do strony: ")
    if Dict.isLink(link, []):
        links = Dict.loadDataFromFile(metaFileNames)
        if Dict.checkIfDicionEelementExists(links, "title"):
            links["title"].append(link)
            Dict.saveDataToFile(metaFileNames, links)
            print("Link zapisany")
        else:
            print("Plik z linkami nie istnieje. Trwa tworznie")
            diction = {"title": link}
            Dict.saveDataToFile(metaFileNames, diction)
            print("Utworzono")

    else:
        print('Link nie istanieje lub witryna jest nieosiągalna. Sprawdź link i połączenie z internetem')


# Usuwa wskazany link
def remove_link(metaFileNames):
    links = Dict.loadDataFromFile(metaFileNames)
    if Dict.checkIfDicionEelementExists(links, "title"):
        choice = Dict.make_choice('Wybierz który link chcesz usunąć', links["title"])
        links["title"].pop(choice - 1)

        Dict.saveDataToFile(metaFileNames, links)

        print("Link usunięty")

    else:
        print("Baza linków nie istnieje")


# Pokazaju jakie wyjątki ma wybrany plik
def show_exceptions(metaFileNames):
    Dict.makeDatabase()
    links = Dict.loadDataFromFile(metaFileNames["pages"])

    if Dict.checkIfDicionEelementExists(links, "title"):
        choice = Dict.make_choice('Z jakiego pliku wyświetlić wyjątki', links["title"])

        fileToOpenName = Dict.makeNameFromLink(links["title"][choice - 1], 'txt')
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


# Dodaje wyjątek do wybranego pliku
def add_exception(metaFileNames):
    Dict.makeDatabase()
    links = Dict.loadDataFromFile(metaFileNames["pages"])

    if Dict.checkIfDicionEelementExists(links, "title"):
        choice = Dict.make_choice("Wybierz do jakiego pliku chcesz dodać wyjątek", links["title"])
        typeChoice = Dict.make_choice(Dict.makeNameFromLink(links["title"][choice - 1], 'txt') + '   Podaj typ wyjątku',
                                      Dict.exceptionTypes)
        excInp = input('Podaj wyjątek: ')
        excFile = Dict.loadDataFromFile(
            Dict.metaFileNames['database'] + '\\' + Dict.makeNameFromLink(links["title"][choice - 1], 'txt'))
        if not Dict.checkIfDicionEelementExists(excFile, "block") or not Dict.checkIfDicionEelementExists(excFile,
                                                                                                          "key"):
            excFile["block"] = []
            excFile["key"] = []

        excFile[Dict.exceptionTypes[typeChoice - 1]].append(excInp)

        Dict.saveDataToFile(
            Dict.metaFileNames['database'] + '\\' + Dict.makeNameFromLink(links["title"][choice - 1], 'txt'), excFile)
        print("Dodano wyjątek")

    else:
        print("Baza danych nie istnieje")


# Usuwa wyjątek z wybranego pliku
def remove_exception(metaFileNames):
    Dict.makeDatabase()
    import os
    links = Dict.loadDataFromFile(metaFileNames["pages"])

    if Dict.checkIfDicionEelementExists(links, "title"):
        i = 0
        while i < len(links["title"]):
            if not Dict.isFile(Dict.metaFileNames['database'] + '\\' + Dict.makeNameFromLink(links["title"][i], 'txt')):
                links["title"].pop(i)
            i += 1

        choice = Dict.make_choice("Wybierz z jakiej bazy chcesz usunąć wyjątek", links["title"])

        exceptions = Dict.loadDataFromFile(
            Dict.metaFileNames['database'] + '\\' + Dict.makeNameFromLink(links["title"][choice - 1], "txt"))
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
            os.remove(Dict.metaFileNames['database'] + '\\' + Dict.makeNameFromLink(links["title"][choice - 1], "txt"))
        else:
            Dict.saveDataToFile(
                Dict.metaFileNames['database'] + '\\' + Dict.makeNameFromLink(links["title"][choice - 1], "txt"),
                exceptions)
    else:
        print("Baza danych nie istanieje")


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


def mainFunc():
    import Dictionary as Dict

    # os.system(Dict.gitManagerMethods['boot'])

    choice = 0
    while True:
        choice = Dict.make_choice('Wybierz co chcesz zrobić', Dict.mainMenu)

        if choice == 1:
            show_links(Dict.metaFileNames['pages'])
        elif choice == 2:
            add_link(Dict.metaFileNames["pages"], Dict.pagesData)
        elif choice == 3:
            remove_link()
        elif choice == 4:
            show_exceptions(Dict.metaFileNames)
        elif choice == 5:
            add_exception(Dict.metaFileNames)
        elif choice == 6:
            remove_exception(Dict.metaFileNames)
        elif choice == 7:
            # os.system(Dict.gitManagerMethods['finish'])
            exit(0)


if __name__ == '__main__':

    import sys
    import Dictionary as Dict

    if len(sys.argv) > 1 and Dict.switches["manual"] in sys.argv:
        print("Włączono działanie manualne, synchronizacja z git zostanie pominięta")
        mainFunc()
    else:
        print("Do włącznia tego skryptu z pominięciem boota trzeba dodać przełącznik \"m\","
              " pomijanie nie jest jednak zalecane bo omija synchronizacje z git ")
