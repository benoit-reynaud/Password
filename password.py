import json
import hashlib

# Vérifie si un mot de passe est déjà présent dans le fichier
def is_password_already_saved(password, filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            for saved_password in data['passwords']:
                if saved_password == hashlib.sha256(password.encode()).hexdigest():
                    return True
            return False
    except FileNotFoundError:
        return False

# Enregistre un mot de passe haché dans le fichier
def save_password(password_hash, filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            data['passwords'].append(password_hash)
    except FileNotFoundError:
        data = {'passwords': [password_hash]}

    with open(filename, 'w') as f:
        json.dump(data, f)

# Demande à l'utilisateur de saisir un mot de passe et l'enregistre dans le fichier si il est valide
def add_password(filename):
    while True:
        password = input("Entrez un mot de passe : ")
        if len(password) < 8:
            print("Le mot de passe doit contenir au moins 8 caractères.")
        elif not any(c.isupper() for c in password):
            print("Le mot de passe doit contenir au moins une lettre majuscule.")
        elif not any(c.islower() for c in password):
            print("Le mot de passe doit contenir au moins une lettre minuscule.")
        elif not any(c.isdigit() for c in password):
            print("Le mot de passe doit contenir au moins un chiffre.")
        elif not any(c in '!@#$%^&*' for c in password):
            print("Le mot de passe doit contenir au moins un caractère spécial (!, @, #, $, %, ^, &, *).")
        elif is_password_already_saved(password, filename):
            print("Le mot de passe est déjà enregistré.")
        else:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            save_password(password_hash, filename)
            print("Le mot de passe a été enregistré avec succès.")
            break

# Affiche tous les mots de passe enregistrés dans le fichier
def show_passwords(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            for password_hash in data['passwords']:
                print(password_hash)
    except FileNotFoundError:
        print("Aucun mot de passe enregistré.")

# Programme principal
filename = "passwords.json"
while True:
    choice = input("Choisissez une option : \n 1) Ajouter un mot de passe \n 2) Afficher les mots de passe enregistrés \n 3) Quitter\n")
    if choice == "1":
        add_password(filename)
    elif choice == "2":
        show_passwords(filename)
    elif choice == "3":
        break
    else:
        print("Choix invalide.")