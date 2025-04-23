import os

DOCS_DIR = 'static/docs'
OUTPUT_FILE = 'templates/docs_etudiants.html'

def generate_html():
    html = ["<html><body><h1>📚 Documents par UE</h1>"]

    print(f"[DEBUG] Parcours de : {DOCS_DIR}")
    for master in sorted(os.listdir(DOCS_DIR)):
        master_path = os.path.join(DOCS_DIR, master)
        if not os.path.isdir(master_path):
            continue
        html.append(f"<h2>🎓 Master : {master}</h2>")
        print(f"[DEBUG] → Master : {master}")

        for semestre in sorted(os.listdir(master_path)):
            semestre_path = os.path.join(master_path, semestre)
            if not os.path.isdir(semestre_path):
                continue
            html.append(f"<h3>📘 Semestre : {semestre}</h3>")
            print(f"  [DEBUG] → Semestre : {semestre}")

            for ue in sorted(os.listdir(semestre_path)):
                ue_path = os.path.join(semestre_path, ue)
                if not os.path.isdir(ue_path):
                    continue
                html.append(f"<h4>📄 UE : {ue}</h4>")
                print(f"    [DEBUG] → UE : {ue}")

                for sous in sorted(os.listdir(ue_path)):
                    sous_path = os.path.join(ue_path, sous)
                    if not os.path.isdir(sous_path):
                        continue
                    html.append(f"<h5>📁 {sous}</h5><ul>")
                    print(f"      [DEBUG] → Dossier : {sous}")

                    for fichier in sorted(os.listdir(sous_path)):
                        file_url = f"/static/docs/{master}/{semestre}/{ue}/{sous}/{fichier}".replace(' ', '%20')
                        html.append(f'<li><a href="{file_url}" target="_blank">🔗 {fichier}</a></li>')
                        print(f"        [FICHIER] {fichier}")
                    html.append("</ul>")

    html.append("</body></html>")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(html))

    print(f"[✅] HTML généré dans : {OUTPUT_FILE}")

if __name__ == '__main__':
    generate_html()
