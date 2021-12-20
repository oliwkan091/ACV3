"""
Skrypt odpowiada za synchronizację z bazą naych na gitchubie
Uruchamiany przed i po właściwym programie
"""


# Pobiera dane z serwera przed startem właściwego programu
def bootChecker():
    import os
    import Dictionary as Dict
    Dict.moduleInstaller()


    if isRepo():
        import git
        # repo =  git.Repo(os.getcwd())
        # print(repo.git.status())
        # repo.git.pull()


# Uruchamiany na końcu prgoramu w celu wysłania zmian na serwer
def finisher():
    import os


    if isRepo():
        import git
        # repo =  git.Repo(os.getcwd())
        # print(repo.git.status())
        # repo.git.add("--all")
        # repo.git.commit('-m "auto commit"')
        # repo.git.push()
        # print('Synchronizacja zakończona')


# Sprawdza czy repoztorum już istanieje:
#	- Jeżeli tak to je aktualizuje
#	- Jeżeli nie to pobiera
def isRepo():
    import git
    import os
    import Dictionary as Dict
    try:
        repo = git.Repo(os.getcwd())
        return True
    except git.exc.NoSuchPathError:
        #reso = git.Repo.clone_from(Dict.gitMetaNames['repo'], os.getcwd())
        return False
    except git.exc.InvalidGitRepositoryError:
        #reso = git.Repo.clone_from(Dict.gitMetaNames['repo'], os.getcwd())
        return False


# Główna funkcja, pozwala łatow uruchomić program z innego skryptu
def mainFunc(argu):
    # Sprawdza, czy dodano przełącznik
    if argu:
        import Dictionary as Dict
        Dict.whileNotIsConnected()
        # Uruchamia bootChecker
        if argu == 'c':
            bootChecker()
        # Uruchamia finisher
        elif argu == 'f':
            finisher()

        return 1
    else:
        print('Przełącznik wymagany')
        print('c - uruchamia bootChecker')
        print('f - uruchamia finisher')
        # if useType == "boot":
        #     return 0


# Przyjmuje dwa przełączniki
if __name__ == "__main__":

    import sys
    import Dictionary as Dict

    if len(sys.argv) > 1 and sys.argv[1] == Dict.switches["manual"]:
        mainFunc(sys.argv, "main")
    else:
        print("Do włączenia tego skryptu z pominięciem boota trzeba dodać przełącznik \"m\","
              " pomijanie nie jest jednak zalecane")
