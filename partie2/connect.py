def reseau(numero:str) :
   

   if numero.startswith("+237"):
        numero = numero[4:]
   elif numero.startswith("00237"):
        numero = numero[5:]

    # Vérification de la longueur du numéro
   if len(numero) != 9 or not numero.isdigit():
        return("numero incorrect")
    

   else:
    prefixe2 = numero[:2]
    prefixe3 = numero[:3]

    # Détermination du réseau
    if prefixe2 == "69":
        return"Le réseau appartient à Orange"
    elif prefixe2 == "65" or prefixe2 == "68":
        if int(prefixe3) in [655, 656, 657, 658, 659, 687, 688, 689]:
           return "Le réseau appartient à Orange"
        else:
         return "Le réseau appartient à MTN"
    elif prefixe2 == "67":
       return "Le réseau appartient à MTN"
    elif prefixe2 == "66":
        return "Le réseau appartient à Nexttel"
    elif prefixe2 == "62":
        return "Le réseau appartient à Camtel"
    else:
        return "Réseau inconnu ou non pris en charge"

numero_saisi=input("entrer un numero de télephone:")
result=reseau(numero_saisi)
print(result)