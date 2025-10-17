def isgood(numero: str):
    # Le cas de l'indicatif international
    if numero.startswith("+237"):
        numero = numero[4:]
    elif numero.startswith("00237"):
        numero = numero[5:]

    # Vérification de la longueur du numéro
    if len(numero) != 9 or not numero.isdigit():
        return False
    else:
        return True
    
        

# On demande à l'utilisateur d'entrer son numéro
numero = input("Entrez votre numero de téléphone: ")

# Nettoyage éventuel de l'indicatif
if numero.startswith("+237"):
    numero = numero[4:]
elif numero.startswith("00237"):
    numero = numero[5:]

#result = isgood(numero)

if isgood(numero):
    prefixe2 = numero[:2]
    prefixe3 = numero[:3]

    # Détermination du réseau
    if prefixe2 == "69":
        print("Le réseau appartient à Orange")
    elif prefixe2 == "65" or prefixe2 == "68":
        if int(prefixe3) in [655, 656, 657, 658, 659, 687, 688, 689]:
            print("Le réseau appartient à Orange")
        else:
            print("Le réseau appartient à MTN")
    elif prefixe2 == "67":
        print("Le réseau appartient à MTN")
    elif prefixe2 == "66":
        print("Le réseau appartient à Nexttel")
    elif prefixe2 == "62":
        print("Le réseau appartient à Camtel")
    else:
        print("Réseau inconnu ou non pris en charge")
else:
    print("Numéro incorrect")
