import os

DOCS_DIR = 'static/docs'
OUTPUT_FILE = 'templates/docs_etudiants.html'

def generate_html():
    html = ["<html><body><h1>📚 Documents par UE</h1>"]

    for master in sorted(os.listdir(DOCS_DIR)):
        master_path = os.path.join(DOCS_DIR, master)
        if not os.path.isdir(master_path):
            continue
        html.append(f"<h2>🎓 Master : {master}</h2>")

        for semestre in sorted(os.listdir(master_path)):
            semestre_path = os.path.join(master_path, semestre)
            if not os.path.isdir(semestre_path):
                continue
            html.append(f"<h3>📘 Semestre : {semestre}</h3>")

            for ue in sorted(os.listdir(semestre_path)):
                ue_path = os.path.join(semestre_path, ue)
                if not os.path.isdir(ue_path):
                    continue
                html.append(f"<h4>📄 UE : {ue}</h4>")

                for sous in sorted(os.listdir(ue_path)):
                    sous_path = os.path.join(ue_path, sous)
                    if not os.path.isdir(sous_path):
                        continue
                    html.append(f"<h5>📁 {sous}</h5><ul>")

                    for fichier in sorted(os.listdir(sous_path)):
                        file_url = os.path.join("static", master, semestre, ue, sous, fichier).replace("\\", "/")
                        html.append('<li><a href="/{}" target="_blank">🔗 {}</a></li>'.format(file_url, fichier))

                    html.append("</ul>")

    html.append("</body></html>")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(html))

if __name__ == '__main__':
    generate_html()
