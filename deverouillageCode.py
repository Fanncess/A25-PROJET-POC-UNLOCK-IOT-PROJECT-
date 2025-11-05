CODE_SECRET = "1234"

while True:
    code = input("Entrez le code secret à 4 chiffres : ")

    if code == CODE_SECRET:
        print("Code correct — la serrure se déverrouille !")
    else:
        print("Code incorrect — accès refusé.")