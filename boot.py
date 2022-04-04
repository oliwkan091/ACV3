"""
Funkcja startuje cały program i poszczególne jego skrypty składowe, do tego restartuje, jeżeli trzeba
"""

if __name__ == "__main__":
    import sys
    import Dictionary as Dict
    import gitManager as gm
    import articleCheckerV3 as acv3
    import articleCheckerManager as acm
    import os

    # LOVE Comprehensions
    # Usuwa ogonki przed przetacznikami o ile istnieją
    argList = [sys.argv[0]] + [element.replace("-", "") for element in sys.argv[1:]]

    # Sprawdza czy nie ma modułów do zainstalowania, jeżeli tak to instaluje i restartuje program,
    #  jeżeli nie to przechodzi dalej pomijając restart
    if not (Dict.switches["gitMode"] in argList or Dict.switches["rebootMode"] in argList or Dict.switches["finisher"] in argList):
        argList = argList + [Dict.switches["gitMode"]]
        if Dict.moduleInstaller():
            print("Ponowne uruchamianie po instalacji modułów")
            # Restartuje program
            if Dict.checkIfExcelFileIsOpen():
                exit(0)
            os.execv(sys.executable, ["python"] + argList)

    # Synchronize z githubem, zawsze restartuje
    if Dict.switches["gitMode"] in argList:
        # Sprawdza czy jakieś pliki nie są uszkodzone/otwarte
        Dict.cleanAfterError()
        # Wywołuje skrypt synchronizacji z git
        gm.mainFunc(Dict.switches["checker"])
        # Usuwa zbędny przełącznik z gitMode jeżeli istanieje
        if Dict.switches["gitMode"] in argList:
            argList.pop()
        argList.append(Dict.switches["rebootMode"])
        print("Ponowne uruchamianie po synchronizacji z git")
        # Restartuje program
        os.execv(sys.executable, ["python"] + argList)

    # Po synchronizacji z githubem i restarcie, główna część
    if Dict.switches["rebootMode"] in argList:
        choice = -1
        # Jeżeli nie ma wymaganych przełączników to pozwala je wybrać
        if Dict.switches["articleCheckerV3"] not in sys.argv and Dict.switches["articleCheckerManager"] not in sys.argv:
            choice = Dict.make_choice("Wybierze który moduł chcesz uruchomić",
                                      ["articleCheckerV3", "articleCheckerManager", "Wyjście"])

        if Dict.switches["articleCheckerV3"] in sys.argv or choice == 1:

            groupsData = Dict.loadDataFromFile(Dict.metaFileNames["groupFile"])

            gGroup = ""
            for key, value in groupsData.items():
                if key in sys.argv:
                    gGroup = key
                    print("Włącznie grupy " + gGroup)
                    break

            acv3.mainFunc(gGroup)

        elif Dict.switches["articleCheckerManager"] in sys.argv or choice == 2:
            print("Uruchamianie articleCheckerManager")
            acm.mainFunc()

        else:
            print("Zamykanie")
            exit(0)

        # Restartuje program po zakończeniu zdania przed synchronizacją z git
        print("Ponowne uruchamianie przed synchronizacją z git")
        os.execv(sys.executable, ["python"] + [Dict.metaFileNames["boot"]] + [Dict.switches["finisher"]])

    # Zawsze synchronizuje z githubem, po zakończeniu działania programu i restarcie
    if Dict.switches["finisher"] in sys.argv:
        gm.mainFunc(Dict.switches["finisher"])
        Dict.cleanAfterError()

    exit(0)