from FilterModule import Filter
from latex_module import Latex_module

text_example = """------>[cos]<------
Wstęp: Czym jest informatyka kwantowa?
Dzień dobry Państwu, cieszę się, że mogę dziś opowiedzieć o jednym z najbardziej ekscytujących obszarów współczesnej
nauki – informatyce kwantowej. Może na początek przypomnę, czym w ogóle jest ta „kwantowość”, o której tak często ostatnio słyszymy.

Mechanika kwantowa opisuje świat na poziomie subatomowym, czyli tam, gdzie klasyczne prawa fizyki przestają działać.
W tym świecie rządzą prawa zupełnie inne, takie jak superpozycja, splątanie czy zasada nieoznaczoności. Informatyka
kwantowa to dziedzina, która wykorzystuje te prawa do przetwarzania informacji.

Klasyczne komputery – te, które wszyscy znamy – opierają się na bitach, które mogą przyjmować wartość 0 albo 1.
Natomiast w komputerze kwantowym pracujemy na kubitach. Kubit to coś, co może być jednocześnie 0 i 1 – i to właśnie
dzięki tej właściwości komputery kwantowe mają potencjał do wykonywania pewnych zadań znacznie szybciej niż tradycyjne.
------>[cos]<------
Superpozycja: Klucz do kwantowej mocy obliczeniowej
Superpozycja to zjawisko, które brzmi niemal jak science fiction, ale jest bardzo realne. Wyobraźmy sobie, że klasyczny
bit jest jak żarówka – może być włączona (1) albo wyłączona (0). Kubit natomiast jest jak taka żarówka, która
jednocześnie świeci i nie świeci. W praktyce oznacza to, że kubit może reprezentować znacznie więcej informacji niż
klasyczny bit.

Co to nam daje? Dzięki superpozycji komputer kwantowy może przetwarzać ogromne ilości danych równocześnie. Przykładem
jest tzw. problem wyszukiwania – klasyczny algorytm przeszukiwałby bazę danych krok po kroku, natomiast komputer
kwantowy, dzięki superpozycji, mógłby sprawdzić wiele możliwości jednocześnie.

Ale uwaga – gdy tylko spróbujemy „zajrzeć”, w jakim stanie jest kubit, jego superpozycja zanika. To właśnie trudność w
pracy z komputerami kwantowymi – stan kwantowy jest niezwykle delikatny i łatwo go zakłócić.
------>[cos]<------
Splątanie: Kwantowy „telepatyczny” efekt
Drugim niesamowitym zjawiskiem, które wykorzystuje informatyka kwantowa, jest splątanie. Jeśli dwa kubity są splątane,
stan jednego zależy od stanu drugiego, niezależnie od odległości między nimi. Einstein nazwał to kiedyś „upiornym
działaniem na odległość”.

W praktyce splątanie może być wykorzystane do błyskawicznej wymiany informacji – choć, od razu dodam, nie oznacza to
przesyłania informacji szybciej niż prędkość światła, co czasem błędnie jest interpretowane w popkulturze.

Splątanie ma jednak ogromny potencjał w dziedzinie kryptografii. Dzięki niemu możemy tworzyć systemy szyfrowania,
które są teoretycznie nie do złamania. Jeśli ktoś próbowałby podsłuchać transmisję opartą na splątaniu, sami odbiorcy
od razu by o tym wiedzieli, ponieważ splątanie zostałoby zakłócone.
------>[cos]<------
Komputery kwantowe w praktyce: Czy zastąpią klasyczne komputery?
Często pojawia się pytanie: „Czy komputery kwantowe zastąpią klasyczne?” Odpowiedź brzmi: nie. Przynajmniej na razie i
prawdopodobnie nie w najbliższej przyszłości. Komputery kwantowe są wyjątkowo dobre w niektórych, bardzo specyficznych
zadaniach, takich jak:

------>[cos]<------
Kryptografia – łamanie kluczy RSA czy generowanie zupełnie losowych liczb.
Symulacje chemiczne – na przykład modelowanie reakcji chemicznych na poziomie molekularnym.
Optymalizacja – rozwiązywanie problemów logistycznych czy harmonogramowych.
Ale w wielu codziennych zastosowaniach, takich jak obsługa przeglądarki internetowej czy gry komputerowe, klasyczne
komputery wciąż będą niezastąpione. Komputery kwantowe są po prostu zbyt skomplikowane i delikatne, by używać ich do
takich zadań.


Wyzwania w budowie komputerów kwantowych
Niestety, budowa komputera kwantowego to ogromne wyzwanie technologiczne. Kubity są niesamowicie wrażliwe na otoczenie
– jakiekolwiek zakłócenia, nawet drobne drgania czy zmiany temperatury, mogą zakłócić ich stan. Dlatego komputery
kwantowe wymagają pracy w ekstremalnie niskich temperaturach, bliskich zeru absolutnemu.

Dodatkowo, im więcej kubitów próbujemy połączyć, tym trudniejsze staje się utrzymanie ich w stabilnym stanie. Obecnie
największe komputery kwantowe mają kilkaset kubitów, co wystarcza do przeprowadzenia pewnych obliczeń, ale daleko im do
tego, co moglibyśmy nazwać „uniwersalnym komputerem kwantowym”.
------>[cos]<------
Podsumowanie: Czy kwantowa rewolucja jest blisko?
Podsumowując, informatyka kwantowa to dziedzina, która ma potencjał, by zmienić świat. Ale, i tu chciałbym podkreślić,
że jesteśmy dopiero na początku tej drogi. To trochę jak z początkami komputerów klasycznych – pierwsze maszyny
zajmowały całe pomieszczenia i były w stanie wykonać tylko proste obliczenia. Dziś każdy z nas ma potężny komputer w
kieszeni.
Czy podobna rewolucja nastąpi w przypadku komputerów kwantowych? Wszystko wskazuje na to, że tak, choć pewnie nie za
naszego życia. Ale już dziś możemy obserwować, jak te technologie zaczynają wpływać na takie dziedziny jak kryptografia,
chemia czy nawet sztuczna inteligencja.

Dziękuję Państwu za uwagę i zachęcam do zadawania pytań!"""
filter_agent = Filter(text_example)
filter_output = filter_agent.run()
print(filter_output)
latex_module = Latex_module(filter_output, "llama3.2", "output", base_url="http://10.244.89.118:11434/v1")
latex_code = latex_module.get_latex()
latex_module.generate_pngs(latex_code)