
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime, timedelta


# ============================================================================
# FONCTIONS UTILITAIRES POUR LES DATES
# ============================================================================

def now_iso():
    """Retourne la date/heure actuelle au format ISO (UTC)."""
    return datetime.utcnow().isoformat()


def plus_jours_iso(jours: int):
    """
    Retourne une date ISO après X jours.
    
    Args:
        jours (int): Nombre de jours à ajouter
    
    Returns:
        str: Date au format ISO
    """
    return (datetime.utcnow() + timedelta(days=jours)).isoformat()


# ============================================================================
# CLASSE LIVRE
# ============================================================================

@dataclass
class livre:
    """
    Représente un livre dans la bibliothèque.
    
    Attributs:
        id_livre (str): Identifiant unique (ex: "L-a1b2c3d4")
        titre (str): Titre du livre
        auteur (str): Nom de l'auteur
        genre (str): Genre littéraire (Roman, Sci-Fi, etc.)
        copies (int): Nombre d'exemplaires disponibles
        annee (int): Année de parution
    """
    id_livre: str
    titre: str
    auteur: str
    genre: str
    copies: int
    annee: int
    
    def to_dict(self):
        """Convertit l'objet Livre en dictionnaire pour la sauvegarde JSON."""
        return {
            "id_livre": self.id_livre,  # ← CORRIGÉ (était "id_livrre")
            "titre": self.titre,
            "auteur": self.auteur,
            "genre": self.genre,
            "copies": self.copies,
            "annee": self.annee,
        }
    
    @classmethod
    def from_dict(cls, d):
        """Crée un objet Livre à partir d'un dictionnaire (chargement JSON)."""
        return cls(
            id_livre=d["id_livre"],
            titre=d["titre"],
            auteur=d["auteur"],
            genre=d["genre"],
            copies=int(d["copies"]),
            annee=int(d["annee"]),
        )
    
    def __str__(self):
        """Affichage personnalisé du livre."""
        return f"📚 {self.titre} par {self.auteur} ({self.annee}) - {self.copies} dispo"


# ============================================================================
# CLASSE ÉTUDIANT
# ============================================================================

@dataclass
class etudiant:
    """
    Représente un étudiant de la bibliothèque.
    
    Attributs:
        id_etudiant (str): Identifiant unique (ex: "E-x1y2z3w4")
        nom (str): Nom complet de l'étudiant
        classe (str): Classe/niveau (ex: "Terminale S")
        emprunt_hist (List[str]): Historique des IDs d'emprunts
    """
    id_etudiant: str
    nom: str
    classe: str
    emprunt_hist: List[str] = field(default_factory=list)
    
    def to_dict(self):
        """Convertit l'objet Étudiant en dictionnaire."""
        return {
            "id_etudiant": self.id_etudiant,
            "nom": self.nom,
            "classe": self.classe,
            "emprunt_hist": self.emprunt_hist,  # ← CORRIGÉ
        }
    
    @classmethod
    def from_dict(cls, d):
        """Crée un objet Étudiant à partir d'un dictionnaire."""
        return cls(
            id_etudiant=d["id_etudiant"],
            nom=d["nom"],
            classe=d["classe"],
            emprunt_hist=list(d.get("emprunt_hist", [])),
        )


# ============================================================================
# CLASSE EMPRUNT
# ============================================================================

@dataclass
class emprunt:
    """
    Représente un emprunt de livre.
    
    Attributs:
        id_etudiant (str): ID de l'étudiant emprunteur
        id_livre (str): ID du livre emprunté
        date_emprunt (str): Date d'emprunt (format ISO)
        date_limite (str): Date de retour prévue (format ISO)
        date_retour (Optional[str]): Date de retour effectif (None si non rendu)
    """
    id_etudiant: str
    id_livre: str
    date_emprunt: str
    date_limite: str
    date_retour: Optional[str]
    
    def to_dict(self):
        """Convertit l'objet Emprunt en dictionnaire."""
        return {
            "id_etudiant": self.id_etudiant,
            "id_livre": self.id_livre,
            "date_emprunt": self.date_emprunt,
            "date_limite": self.date_limite,
            "date_retour": self.date_retour,
        }
    
    @classmethod
    def from_dict(cls, d):
        """Crée un objet Emprunt à partir d'un dictionnaire."""
        return cls(
            id_etudiant=d["id_etudiant"],
            id_livre=d["id_livre"],
            date_emprunt=d["date_emprunt"],
            date_limite=d["date_limite"],
            date_retour=d.get("date_retour"),
        )
    
    def est_en_retard(self):
        """Vérifie si l'emprunt est en retard."""
        if self.date_retour is not None:
            return False
        limite = datetime.fromisoformat(self.date_limite)
        return datetime.utcnow() > limite
    
    def jours_restants(self):
        """Calcule le nombre de jours avant la date limite."""
        if self.date_retour is not None:
            return 0
        limite = datetime.fromisoformat(self.date_limite)
        delta = limite - datetime.utcnow()
        return max(0, delta.days)