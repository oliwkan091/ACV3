"""
Skrypt odpowiada za synchronizację z bazą naych na gitchubie
Uruchamiany przed i po właściwym programie
"""


def bootChecker() -> None:
    """
    Pobiera dane z serwera przed startem właściwego programu
    """
    import os
    import Dictionary as Dict
    Dict.moduleInstaller()

    #   UNCOMMENT WHEN READY
    if isRepo():
        import git
        repo = git.Repo(os.getcwd())
        print(repo.git.status())
        repo.git.pull()


def finisher() -> None:
    """
    Uruchamiany na końcu programu w celu wysłania zmian na serwer
    """
    import os

    #   UNCOMMENT WHEN READY
    if isRepo():
        import git
        repo = git.Repo(os.getcwd())
        print(repo.git.status())

        repo.git.add("--all")
        if repo.head.commit.diff() != []:
            repo.git.commit("-m \"auto commit\"")
            repo.git.push()
            print("Dodano zmiany")
        else:
            print("Brak nowych zmian")

    print("Synchronizacja z git zakońona")


def isRepo() -> bool:
    """
    # Sprawdza czy repoztorum już istanieje:

    :return: True repozytorium istnieje można działać, False repozytorium nie istnieje trzeba je pobrać
    """

    import git
    import os
    import Dictionary as Dict
    try:
        repo = git.Repo(os.getcwd())
        return True
    except git.exc.NoSuchPathError:
        #reso = git.Repo.clone_from(Dict.gitMetaNames["repo"], os.getcwd())
        return False
    except git.exc.InvalidGitRepositoryError:
        #reso = git.Repo.clone_from(Dict.gitMetaNames["repo"], os.getcwd())
        return False


def mainFunc(argu: str) -> None:
    """
    Główna funkcja, pozwala uruchomić program z innego skryptu
    :param argu:
    :return:
    """
    # Sprawdza, czy dodano przełącznik
    if argu:
        import Dictionary as Dict
        Dict.whileNotIsConnected()
        # Uruchamia bootChecker
        if argu == "c":
            bootChecker()
        # Uruchamia finisher
        elif argu == "f":
            finisher()

        return
    else:
        print("Przełącznik wymagany")
        print("c - uruchamia bootChecker")
        print("f - uruchamia finisher")
        # if useType == "boot":
        #     return 0


# Przyjmuje dwa przełączniki
if __name__ == "__main__":

    import sys
    import Dictionary as Dict
    argList = [sys.argv[0]] + [element.replace("-", "") for element in sys.argv[1:]]
    # [expression for item in list if conditional]
    actionSwitch = ""
    actionSwitch = [element for element in argList if element == "c" or element == "f"][0]
    print(actionSwitch)
    # action = [if elenment.equals("c") or elenment.equals("f") for element in argList]

    if len(sys.argv) > 1 and argList[1] == Dict.switches["manual"]:
        if Dict.checkIfExcelFileIsOpen():
            exit(0)
        mainFunc(actionSwitch)
    else:
        print("Do włączenia tego skryptu z pominięciem boota trzeba dodać przełącznik \"m\","
              " pomijanie nie jest jednak zalecane")