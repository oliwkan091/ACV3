"""
Funkcja startuje cały program i poszczególne jego skrypty składowe, do tego restartuje, jeżeli trzeba
"""

if __name__ == "__main__":
    import sys
    import Dictionary
    import gitManager as gm
    import articleCheckerV3 as acv3
    import os

    # Sprawdza, czy przełączniki podane na wejściu się zgadzają
    if len(sys.argv) == 1:
        Dictionary.cleanAfterError()
        # Wywołuje skrypt synchronizacji z git
        if gm.mainFunc("c", "boot"):
            # Dodaje przełącznik potrzebny do ponownego uruchomienia
            argList = sys.argv + ["r"]
            print("Ponowne uruchamianie po synchronizacji z git")
            # Restartuje program
            os.execv(sys.executable, ['python'] + argList)
        else:
            print("Błąd podczas synchronizacji git")
            print("exit")
    # Po restarcie
    elif len(sys.argv) != 1 and sys.argv[1] == "r":
        acv3.mainFunc()
        gm.mainFunc("f", "boot")
        Dictionary.cleanAfterError()




