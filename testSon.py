import subprocess

text = "Voici l'énigme ultime pour déverouiller la porte. " \
"Quelle est la date de création du Cégep Beauce Appalaches?"
commande = [
    "espeak",
    "-v", "mb-fr1",
    "-s", "150",
    "-a", "200",
    text
]

subprocess.run(commande)