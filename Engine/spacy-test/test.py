import spacy

nlp = spacy.load("pl_core_news_lg")
doc = nlp(
    "Warszawa, dnia 02-06-2020 Jan Kowalski ul. Adama Mickiewicza 23/14 01-230 Warszawa Tel. 665 444 333 Email: jan.kowalski@gmail.com Sąd Rejonowy dla Warszawy-Woli w  Warszawie III Wydział Karny  ul. Kocjana 3 01-473 Warszawa Sygnatura akt: III K 1144/20 Sygnatura oskarżyciela: PO III Ds. 2.2020 WNIOSEK DOWODOWY Ja, niżej podpisany, oskarżony w sprawie o sygnaturze III K 1144/20 , wnoszę o dopuszczenie następujących dowodów:  • Potwierdzenie przelewu z dnia 10 lutego 2020 r. na rachunek Zarządu Transportu Miejskiego 94 1030 1508 0000 0005 5104 1409 w kwocie 350,00 zł.  • Fragment korespondencji pocztą elektroniczną z dnia 17 marca 2020 r. z Panem Andrzejem Nowakiem oraz Panem Tomaszem Adamowiczem, którzy są pracownikami Działu Nadzoru Handlowego w Zarządzie Transportu Miejskiego.  Uzasadnienie  W dniu 10 lutego 2020 r. uregulowałem w całości należność w mojej sprawie w wysokości 350,00 zł na rzecz Miasta Stołecznego Warszawy, reprezentowanego przez Zarząd Transportu Miejskiego. Takie potwierdzenie przesłał mi Pan Tomasz Adamowicz z Działu Nadzoru Handlowego w dniu 17 marca 2020 r. potwierdzając, że ta wpłata wyczerpuje roszczenia Zarząd Transportu Miejskiego względem mojej osoby. ………………………….   Załączniki:  - Potwierdzenie przelewu PKO BP z dnia 10 lutego 2020 r.; - Wiadomość mailowa od Pana Tomasza Adamowicza z dnia 10 stycznia 2020 r.;   podpis")

for index, phraseToAnon in enumerate(doc.ents):

    print(index)
    print(phraseToAnon[0].text)
    assert phraseToAnon[0].text is "Warszawa"

    print(phraseToAnon.text, phraseToAnon.start_char, phraseToAnon.end_char, phraseToAnon.label_)
