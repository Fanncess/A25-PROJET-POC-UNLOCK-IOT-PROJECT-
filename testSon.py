import subprocess

text = "Je t'aime"
commande = [
    "espeak",
    "-v", "fr+f1",
    "-s", "140",
    "-a", "200",
    text
]

subprocess.run(commande)