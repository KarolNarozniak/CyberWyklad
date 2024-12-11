from langclass import Translator, Knowledge

pytanie = input("Zadaj pytanie: ")

tlumacz = Translator( )
wiedza = Knowledge( )

question = tlumacz.invoke(pytanie)
print("co wysylam:", question, "\n")
baza = wiedza.invoke(question)
print(baza)