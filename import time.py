import time
from datetime import datetime

# VARIABLES GLOBALES


# Variable pour stocker l'heure de l'alarme (None si pas d'alarme définie)
alarme = None

# Variable pour le mode d'affichage (True = 24h, False = 12h)
mode_24h = True

# Variable pour mettre en pause l'horloge (True = en marche, False = en pause)
horloge_en_marche = True

# Variable pour stocker l'heure personnalisée (None = heure système)
heure_personnalisee = None


# FONCTION PRINCIPALE : AFFICHER L'HEURE


def afficher_heure(heure_tuple=None):
    """
    Fonction qui affiche l'heure au format hh:mm:ss
    
    Paramètres:
        heure_tuple : tuple (heures, minutes, secondes) - optionnel
                      Si None, utilise l'heure système
    """
    global heure_personnalisee
    
    # Si on passe un tuple en paramètre, on utilise cette heure
    if heure_tuple is not None:
        heures, minutes, secondes = heure_tuple
        heure_personnalisee = heure_tuple
    # Sinon, si on a une heure personnalisée stockée, on l'utilise
    elif heure_personnalisee is not None:
        heures, minutes, secondes = heure_personnalisee
    # Sinon, on prend l'heure actuelle du système
    else:
        maintenant = datetime.now()
        heures = maintenant.hour
        minutes = maintenant.minute
        secondes = maintenant.second
    
    # Formatage de l'heure selon le mode choisi (12h ou 24h)
    if mode_24h:
        # Mode 24 heures : affichage simple
        heure_formatee = f"{heures:02d}:{minutes:02d}:{secondes:02d}"
    else:
        # Mode 12 heures : il faut convertir et ajouter AM/PM
        periode = "AM"  # Par défaut, c'est le matin
        heures_12h = heures
        
        # Si c'est l'après-midi ou le soir (>= 12h)
        if heures >= 12:
            periode = "PM"
            # Si c'est après midi (13h-23h), on soustrait 12
            if heures > 12:
                heures_12h = heures - 12
        
        # Cas spécial : minuit (0h) devient 12h AM
        if heures == 0:
            heures_12h = 12
        
        heure_formatee = f"{heures_12h:02d}:{minutes:02d}:{secondes:02d} {periode}"
    
    return heure_formatee


# FONCTION : RÉGLER L'ALARME


def regler_alarme(heure_alarme):
    """
    Fonction pour régler l'alarme
    
    Paramètres:
        heure_alarme : tuple (heures, minutes, secondes)
    """
    global alarme
    alarme = heure_alarme
    heures, minutes, secondes = heure_alarme
    print(f"\n⏰ Alarme réglée à {heures:02d}:{minutes:02d}:{secondes:02d}")


# ============================================
# FONCTION : VÉRIFIER L'ALARME
# ============================================

def verifier_alarme(heure_actuelle):
    """
    Vérifie si l'heure actuelle correspond à l'alarme
    
    Paramètres:
        heure_actuelle : tuple (heures, minutes, secondes)
    """
    global alarme
    
    # Si une alarme est définie et qu'elle correspond à l'heure actuelle
    if alarme is not None and heure_actuelle == alarme:
        print("\n" + "="*50)
        print(" DRING DRING DRING ! ALARME !" )
        print("="*50 + "\n")
        # On désactive l'alarme après qu'elle a sonné
        alarme = None



# FONCTION : CHANGER LE MODE D'AFFICHAGE


def changer_mode_affichage(mode_12_heures=False):
    """
    Change le mode d'affichage entre 12h et 24h
    
    Paramètres:
        mode_12_heures : True pour 12h, False pour 24h
    """
    global mode_24h
    mode_24h = not mode_12_heures
    mode_texte = "24 heures" if mode_24h else "12 heures"
    print(f"\n📺 Mode d'affichage changé : {mode_texte}")



# FONCTION : METTRE EN PAUSE


def mettre_en_pause():
    """
    Met l'horloge en pause (pour faire des farces à mamie !)
    """
    global horloge_en_marche
    horloge_en_marche = not horloge_en_marche
    
    if horloge_en_marche:
        print("\n▶️  Horloge relancée !")
    else:
        print("\n⏸️  Horloge en pause (hehe, mamie va être confuse !)")



# FONCTION : OBTENIR L'HEURE ACTUELLE


def obtenir_heure_actuelle():
    """
    Retourne l'heure actuelle sous forme de tuple
    """
    if heure_personnalisee is not None:
        return heure_personnalisee
    else:
        maintenant = datetime.now()
        return (maintenant.hour, maintenant.minute, maintenant.second)



# FONCTION : INCRÉMENTER L'HEURE


def incrementer_heure():
    """
    Incrémente l'heure d'une seconde (pour l'heure personnalisée)
    """
    global heure_personnalisee
    
    if heure_personnalisee is not None:
        heures, minutes, secondes = heure_personnalisee
        
        # Ajouter une seconde
        secondes += 1
        
        # Gérer le passage à la minute suivante
        if secondes >= 60:
            secondes = 0
            minutes += 1
        
        # Gérer le passage à l'heure suivante
        if minutes >= 60:
            minutes = 0
            heures += 1
        
        # Gérer le passage à minuit (retour à 0)
        if heures >= 24:
            heures = 0
        
        heure_personnalisee = (heures, minutes, secondes)



# FONCTION PRINCIPALE : LANCER L'HORLOGE

def lancer_horloge():
    """
    Lance l'horloge et l'affiche en continu
    """
    print("\n" + "="*50)
    print("🕰️  HORLOGE DE MAMIE JEANNINE 🕰️")
    print("="*50)
    print("\nCommandes disponibles pendant l'exécution :")
    print("  - Ctrl+C pour arrêter l'horloge")
    print("\n" + "="*50 + "\n")
    
    try:
        # Boucle infinie pour afficher l'heure
        while True:
            # Si l'horloge est en marche
            if horloge_en_marche:
                # Obtenir l'heure actuelle
                heure_actuelle = obtenir_heure_actuelle()
                
                # Vérifier si l'alarme doit sonner
                verifier_alarme(heure_actuelle)
                
                # Afficher l'heure
                heure_formatee = afficher_heure()
                
                # Utiliser \r pour réafficher sur la même ligne
                print(f"\r🕐 {heure_formatee}", end="", flush=True)
                
                # Attendre 1 seconde
                time.sleep(1)
                
                # Incrémenter l'heure si on utilise une heure personnalisée
                if heure_personnalisee is not None:
                    incrementer_heure()
            else:
                # Si l'horloge est en pause, on n'incrémente pas
                time.sleep(0.1)
    
    except KeyboardInterrupt:
        # Quand l'utilisateur appuie sur Ctrl+C
        print("\n\n👋 Horloge arrêtée. Mamie Jeannine vous remercie !")


# EXEMPLE D'UTILISATION


if __name__ == "__main__":
    # Vous pouvez décommenter les lignes ci-dessous pour tester
    
    # 1. Régler une heure personnalisée (optionnel)
    # afficher_heure((16, 30, 0))  # Règle l'horloge à 16:30:00
    
    # 2. Régler une alarme (optionnel)
    # regler_alarme((16, 30, 10))  # Alarme à 16:30:10
    
    # 3. Changer le mode d'affichage (optionnel)
    # changer_mode_affichage(True)  # Passer en mode 12 heures
    
    # 4. Lancer l'horloge
    lancer_horloge()
    
    # Note : Pour mettre en pause pendant l'exécution, vous devriez
    # implémenter une gestion des entrées clavier en parallèle
    # (par exemple avec le module threading)