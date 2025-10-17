#afficher toutes les informations dans le menu
from library_manager import librarymanager
import sys 
  

def menu():
    print("\n=== Bibliothèque ===")
    print("1. Lister les livres")
    print("2. Ajouter un livre")
    print("3. Modifier un livre")
    print("4. Supprimer un livre")
    print("5. Ajouter un étudiant")
    print("6. Emprunter un livre")
    print("7. Rendre un livre")
    print("8. Rechercher (titre/auteur/genre)")
    print("9. Recherche dichotomique par préfixe de titre")
    print("10. Quitter (sauvegarder)")


def main():
    biblio = librarymanager()
    biblio.load_all()
    print("✅ Données chargées avec succès.")

    try:
        while True:
            menu()
            choix = input("Votre choix : ").strip()

            if choix == "1":
                print("\n--- Liste des livres ---")
                for l in biblio.lister_livres():
                    print(f"{l.id_livre} | {l.titre} - {l.auteur} ({l.genre}) - copies : {l.copies}")

            elif choix == "2":
                titre = input("Titre : ")
                auteur = input("Auteur : ")
                genre = input("Genre : ")
                copies = int(input("Nombre d'exemplaires : "))
                annee = int(input("Année de parution : "))
                l = biblio.ajouter_livre(titre, auteur, genre, copies, annee)
                print(f"Livre ajouté ✅ → ID : {l.id_livre}")

            elif choix == "3":
                lid = input("ID du livre à modifier : ")
                print("Laissez vide pour ne pas modifier un champ.")
                new_titre = input("Nouveau titre : ").strip()
                new_auteur = input("Nouvel auteur : ").strip()
                new_genre = input("Nouveau genre : ").strip()
                new_copies = input("nouveau nombres d'exemplaires: ").strip()
                changements = {}
                if new_titre: changements["titre"] = new_titre
                if new_auteur: changements["auteur"] = new_auteur
                if new_genre: changements["genre"] = new_genre
                if new_copies: changements["copies"] = new_copies
                ok = biblio.modifier_livre(lid, **changements)
                print("✅ Modifié avec succès." if ok else "❌ Livre introuvable.")

            elif choix == "4":
                lid = input("ID du livre à supprimer : ")
                try:
                    biblio.supprimer_livre(lid)
                    print("✅ Livre supprimé.")
                except ValueError as e:
                    print("❌ Erreur :", e)

            elif choix == "5":
                nom = input("Nom de l'étudiant : ")
                classe = input("Classe : ")
                e = biblio.ajouter_etudiant(nom, classe)
                print(f"Étudiant ajouté ✅ → ID : {e.id_etudiant}")

            elif choix == "6":
                eid = input("ID étudiant : ")
                lid = input("ID livre : ")
                try:
                    em = biblio.emprunter_livre(eid, lid)
                    print(f"✅ Emprunt enregistré → ID emprunt : {em.id_etudiant}-{em.id_livre}")
                except Exception as e:
                    print("❌ Erreur :", e)

            elif choix == "7":
                rid = input("ID emprunt : ")
                try:
                    em = biblio.retourner_livre(rid)
                    print("✅ Retour enregistré.")
                except Exception as e:
                    print("❌ Erreur :", e)

            elif choix == "8":
                critere = input("Rechercher par (titre/auteur/genre) : ").strip().lower()
                terme = input("Terme à rechercher : ")
                if critere == "titre":
                    res = biblio.rechercher_par_titre(terme)
                elif critere == "auteur":
                    res = biblio.rechercher_par_auteur(terme)
                else:
                    res = biblio.rechercher_par_genre(terme)

                print("\n--- Résultats ---")
                for l in res:
                    print(f"{l.id_livre} | {l.titre} - {l.auteur} ({l.genre}) - copies : {l.copies}")

            elif choix == "9":
                prefixe = input("Préfixe du titre : ")
                res = biblio.recherche_dichotomique(prefixe)
                print("\n--- Résultats ---")
                for l in res:
                    print(f"{l.id_livre} | {l.titre} - {l.auteur}")

            elif choix == "10":
                print("💾 Sauvegarde des données...")
                biblio.save_all()
                print("👋 Au revoir.")
                break

            else:
                print("❌ Choix invalide, veuillez réessayer.")

    except KeyboardInterrupt:
        print("\n⚠ Interruption détectée. Sauvegarde avant de quitter...")
        biblio.save_all()
        sys.exit(0)

if __name__ == "__main__":
    main()
