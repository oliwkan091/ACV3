Lokalizacja głównego pliku vbs:
C:\Users\Oliwier Kania\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
Ogólnie
C:\Users\[user name]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

--------------------------------------------------------------------------------------------------------------
Instrukcja działania (przechuj trochę)

W folderze który aktywuje swoje wszystkie swoje pliki przy starcie windowsa:
C:\Users\[user name]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
Znajduje się skrót do pliku (bo blik ten musi się znajdować koło pliku bat):
ArticleCheckerBootWindowsStarter.vbs
Aktywuje on plik bat w sposób niewidoczny czyli nie wyświetla konsoli

Plik bat:
articleCheckerStarter.bat
znajdujący się w folderze:
D:\Desktop\Moje Pliki\Nauka\Code\Python\ARTICLES\articleChecker

Jest on odpowiedzialny za aktywowanie skryptu pythona w kosoli cmd ale ponieważ sam wyświetla konsolę musi byc poprzedzony plikiem vbs
Skrypt pythona: 
articleChecker.py
Skrypt ten wykonuje całą logikę programu wczytuje i zapisuje dwa pliki tekstowe

Pierwszy zaspisuje datę ostatniej sesji i znajduje się w tym samym folderze:
articlesMetadata.txt

Drugi zapisuje wyniki wyszukiwania:
New Articles.txt
i znajduje się w folderze:
D:\Documents\Dysk Google\Schengen

Kolejność działania:

Boot Winowsa -> skrót pliku vbs -> plik vbs -> plik bat -> plik py

Wszystkie pliki można edytować tekstowo i dostosowaywać do potrzeba lokalizacji

Pliki nie wymienione tutaj nie mają wpływu na boot
----------------------------------------------------------------------------------------------------------------
Na wszelki wypadek kod pliku vs:

Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c articleCheckerStarter.bat"
oShell.Run strArgs, 0, false

Plik ten musi znajdować się w folderze pliku bat

Kod pliku bat:

::D:
:: Ponizej wkleic lokalizacje tego pliku bat
::cd D:\Desktop\Moje Pliki\Nauka\Code\Python\ARTICLES\articleChecker
python articleChecker.py

:: - oznacza komentarz
Ponieważ plik ten uruchamiając konsolę autoamtycznie podaje swoją lokajizację nie trzeba jej szczunie ustawiać co jest bardzo wygodne i wystarczy włączyć program:

-------------------------------------------------------------------------------------------------------------------
Na laptopie za uruchamianie odpowiedzialny jest harmonogram windows 
W folderze 	Biblioteka Harmonogramu Zadań znajduje się zdarzenie 
ArticleCheckerAfterHibernation
które uruchamiane jest codziennie o 9 


