#ajouter un livre,modifier un livre,ajouter un etudiant,lister les livres,etc
from models import livre,etudiant,emprunt
from utils import save_json,load_json
from datetime import datetime,timedelta
import uuid
import bisect
 
def _now_iso():
    return datetime.utcnow().isoformat()
#pour ajouter le temps definit au temps à l'instant t
def _iso_plus_days(days: int):
    return (datetime.utcnow() + timedelta(days=days)).isoformat()

def _generate_id(prefix: str = ""):
    return prefix + str(uuid.uuid4())[:8]

class librarymanager:

    def __init__(self, livres_file="livres.json", etudiants_file="etudiants.json", emprunts_file="emprunts.json"):
        self.livres_file = livres_file
        self.etudiants_file = etudiants_file
        self.emprunts_file = emprunts_file

        self.livres = {}
        self.etudiants = {}
        self.emprunts = {}

        self.load_all()

    # la sauvegarde et le chargement/sauvegarde 
    def save_all(self):
        save_json(self.livres_file, {lid: l.to_dict() for lid, l in self.livres.items()})
        save_json(self.etudiants_file, {eid: e.to_dict() for eid, e in self.etudiants.items()})
        save_json(self.emprunts_file, {rid: r.to_dict() for rid, r in self.emprunts.items()})
    #chargement
    def load_all(self):
        livres_data = load_json(self.livres_file) or {}
        etudiants_data = load_json(self.etudiants_file) or {}
        emprunts_data = load_json(self.emprunts_file) or {}

        self.livres = {lid: livre.from_dict(d) for lid, d in livres_data.items()}
        self.etudiants = {eid: etudiant.from_dict(d) for eid, d in etudiants_data.items()}
        self.emprunts = {rid: emprunt.from_dict(d) for rid, d in emprunts_data.items()}
    

    # les différentes option d'operation  qui pourront etre effectuer sur les livres
    #ajouter un livre
    def ajouter_livre(self, titre: str, auteur: str, genre: str, copies: int, annee: int) -> livre:
        lid = _generate_id("L-")
        l = livre(id_livre=lid, titre=titre, auteur=auteur, genre=genre, copies=copies, annee=annee)
        self.livres[lid] = l
        return l
    #modifier un livre
    def modifier_livre(self, id_livre: str, **changements) -> bool:
        l = self.livres.get(id_livre)
        if not l:
            return False
        for k, v in changements.items():
            if hasattr(l, k):
                setattr(l, k, v)
        return True
    #supprimer un livre 
    def supprimer_livre(self, id_livre: str) -> bool:
        if id_livre not in self.livres:
            return False
        actif = any(e.id_livre == id_livre and e.date_retour is None for e in self.emprunts.values())
        if actif:
            raise ValueError("Impossible de supprimer : exemplaires encore empruntés.")
        del self.livres[id_livre]
        return True
    #lister les livres 
    def lister_livres(self) -> list[livre]:
        return list(self.livres.values())

    # les differentes options sur etudiant 
    #ajouter un etudiant
    def ajouter_etudiant(self, nom: str, classe: str) -> etudiant:
        eid = _generate_id("E-")
        e = etudiant(id_etudiant=eid, nom=nom, classe=classe)
        self.etudiants[eid] = e
        return e
    #modifier les informations d'un etudiant
    def modifier_etudiant(self, id_etudiant: str, **changements) -> bool:
        e = self.etudiants.get(id_etudiant)
        if not e:
            return False
        for k, v in changements.items():
            if hasattr(e, k):
                setattr(e, k, v)
        return True

    # les differantes options pour l'emprunt de livre
    #emprunter un livre en entrant l'id de l'etudiant et l'id du livre
    def emprunter_livre(self, id_etudiant: str, id_livre: str, jours: int = 14) -> emprunt:
        e = self.etudiants.get(id_etudiant)
        l = self.livres.get(id_livre)

        if e is None:
            raise ValueError("Étudiant introuvable.")
        if l is None:
            raise ValueError("Livre introuvable.")
        if l.copies <= 0:
            raise ValueError("Aucun exemplaire disponible.")

        rid = _generate_id("R-")
        em = emprunt(
            id_etudiant=id_etudiant,
            id_livre=id_livre,
            date_emprunt=_now_iso(),
            date_limite=_iso_plus_days(jours),
            date_retour=None
        )
        self.emprunts[rid] = em
        e.emprunt_hist.append(rid)
        l.copies -= 1
        return em
    #retourner un livre en entrant l'id de l'emprunt qui est l'id de l'etudiant suivi de l'id du livre
    def retourner_livre(self, id_emprunt: str) -> emprunt:
        em = self.emprunts.get(id_emprunt)
        if not em:
            raise ValueError("Emprunt introuvable.")
        if em.date_retour is not None:
            raise ValueError("Livre déjà rendu.")

        em.date_retour = _now_iso()
        l = self.livres.get(em.id_livre)
        if l:
            l.copies += 1
        return em

    # ---------- Recherche ----------
    def rechercher_par_titre(self, mot: str) -> list[livre]:
        q = mot.lower().strip()
        return [l for l in self.livres.values() if q in l.titre.lower()]

    def rechercher_par_auteur(self, mot: str) -> list[livre]:
        q = mot.lower().strip()
        return [l for l in self.livres.values() if q in l.auteur.lower()]

    def rechercher_par_genre(self, mot: str) -> list[livre]:
        q = mot.lower().strip()
        return [l for l in self.livres.values() if q == l.genre.lower()]

    # ---------- Recherche dichotomique ----------
    def _titres_tries(self):
        arr = sorted([(l.titre.lower(), l.id_livre) for l in self.livres.values()], key=lambda x: x[0])
        titres = [t for t, _ in arr]
        ids = [i for _, i in arr]
        return titres, ids

    def recherche_dichotomique(self, prefixe: str) -> list[livre]:
        prefixe = prefixe.lower().strip()
        titres, ids = self._titres_tries()
        gauche = bisect.bisect_left(titres, prefixe)
        resultats = []
        n = len(titres)
        while gauche < n and titres[gauche].startswith(prefixe):
            resultats.append(self.livres[ids[gauche]])
            gauche += 1
        return resultats
