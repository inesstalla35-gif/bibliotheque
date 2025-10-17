
from dataclasses import dataclass,field
from typing import Optional,List
from datetime import datetime,timedelta


def now_iso():
    #Retourne la date/heure actuelle au format ISO (UTC)."""
    return datetime.utcnow().isoformat()

def plus_jours_iso(jours: int):
    #Retourne une date ISO après X jours.
    return (datetime.utcnow() + timedelta(days=jours)).isoformat()

#programmation orienté objet(POO)
@dataclass 
class livre:#une classe qui est  un modèle qui définit quel atribut et quelle methode va définir notre objet(les livres crée)
   id_livre: str#les donnees (des attributs)
   titre:str
   auteur:str
   genre:str
   copies:int
   annee:int
 #produire un dictionnaire simple qui va faciliter conversion les objets en  un fichier json et conserver 
def to_dict(self):#les comportements(methodes)
    return{
        "id_livre": self.id_livrre,
        "titre" : self.titre,
        "auteur" : self.auteur,
        "genre" : self.genre,
        "copies" : self.copies,
        "annee" : self.annee,
    }
#transfome le dictionnaire en objet pour recharger depuis le fichier json contrairement à to_dict transforme l'objet en dictionnaire pour sauvegarder dans le json
@classmethod
def from_dict(cls,d):
    return cls(
          id_livre=d["id_livre"],
          titre=d["titre"],
          auteur=d["auteur"],
          genre=d["genre"],
          copies=int(d["copies"]),
          annee=int(d["annee"]),
   )

@dataclass
class etudiant:
    id_etudiant:str
    nom:str
    classe:str
    emprunt_hist:list[str]=field(default_factory=list)

def to_dict(self):
    return{
        "id_etudiant":self.id_etudiant,
        "nom":self.nom,
        "classe":self.classe,
        "emprunt_hist":List(self.emperunt_hist),
 
    }

@classmethod
def from_dict(cls, d):
    return cls(
        id_etudiant=d["id_etudiant"],
        nom=d["nom"],
        classe=d["classe"],
        emprunt_hist=list(d.get("emprunt_hist" ,[])),#prend la clé du emprunt_hist si elle existe et sinon elle est vide

    )
    

    
       
@dataclass
class emprunt:
    id_etudiant:str
    id_livre:str
    date_emprunt:str
    date_limite:str
    date_retour:str

def to_dict(self):
    return{
        "id_etudiant":self.id_etudiant,
        "id_livre":self.id_livre,
        "date_emprunt":self.date_emprunt,
        "date_limite":self.date_limite,
        "date_retour":self.date_retour,
    }

@classmethod
def from_dict(cls, d):
    return cls(
        id_etudiant=d["id_etudiant"],
        id_livre=d["id_livre"],
        date_emprunt=d["date_emprunt"],
        date_limite=d["date_limite"],
        date_retour=d.get("date_retour"),

    )
