from googletrans import Translator



with open('db.txt', 'r', encoding = 'utf8') as file:
    translator=Translator()
    outinfo = file.read()
    strip = outinfo.replace("{","").replace("}","")
    transstring = translator.translate(strip, src='ja')
    print(transstring)