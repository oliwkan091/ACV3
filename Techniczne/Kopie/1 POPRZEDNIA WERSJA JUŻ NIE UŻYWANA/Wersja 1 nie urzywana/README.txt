Lokalizacja głównego pliku vbs:
C:\Users\Oliwier Kania\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
Ogólnie
C:\Users\[user name]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

--------------------------------------------------------------------------------------------------------------
Instrukcja działania (przechuj trochę)

W folderze który aktywuje swoje wszystkie swoje pliki przy starcie windowsa:
C:\Users\[user name]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
Znajduje się skrót do pliku (bo blik ten musi się znajdować koło pliku bat):
articleCheckerStarter.bat
Aktywuje on plik bat w sposób niewidoczny czyli nie wyświetla konsoli

Plik bat:
ArticleCheckerStarter.bat
znajdujący się w folderze:
D:\Desktop\Moje Pliki\Nauka\Code\Python\ARTICLES\Articles Checker v3

Jest on odpowiedzialny za aktywowanie skryptu pythona w kosoli cmd ale ponieważ sam wyświetla konsolę musi byc poprzedzony plikiem vbs
Skrypt pythona: 
ArticleChecker.py
Skrypt ten wykonuje całą logikę programu 

W folderze znajdują się też pliki trekstowe niezbędne do działanie programu

Pierwszy 
Metadata.txt
posiada dane niezbędne do działania programu czyli dane o nazwach plików i ich lokalizacjach
Plik ten można edytować w celu dostosowania do lokalicaji plików

Drugi 
PagesToCheck.txt
Posiada linki do wszystklich stron które należy sprawdzić 
Plik ten można edytować w celu dodawania i usuwania stron

Ostani plik to New Articles.txt który znajduje się w innym foldrze 
D:\Documents\Dysk Google\Schengen
Zapisywane są tu wszystkie wyniki działania programu 

Kolejność działania:

Boot Winowsa -> skrót pliku vbs -> plik vbs -> plik bat -> plik py

Wszystkie pliki można edytować tekstowo i dostosowaywać do potrzeba lokalizacji

Pliki nie wymienione tutaj nie mają wpływu na boot
----------------------------------------------------------------------------------------------------------------
Na wszelki wypadek kod pliku vs:

Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c ArticleCheckerStarter.bat"
oShell.Run strArgs, 0, false

Plik ten musi znajdować się w folderze pliku bat

Kod pliku bat:

::D:
:: Ponizej wkleic lokalizacje tego pliku bat
::cd D:\Desktop\Moje Pliki\Nauka\Code\Python\ARTICLES\articleChecker
python ArticleChecker.py

:: - oznacza komentarz
Ponieważ plik ten uruchamiając konsolę autoamtycznie podaje swoją lokajizację nie trzeba jej szczunie ustawiać co jest bardzo wygodne i wystarczy włączyć program:



