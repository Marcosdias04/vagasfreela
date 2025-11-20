from flask import Flask, request, render_template_string
import feedparser, os

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="utf-8"><title>VagasFreela BR</title>
<style>
    body{font-family:Arial;background:#0d1117;color:white;margin:0;padding:20px;text-align:center}
    .box{max-width:800px;margin:auto;background:#161b22;padding:40px;border-radius:20px}
    input,button{padding:16px;font-size:18px;border:none;border-radius:12px;margin:10px}
    input{width:70%;max-width:500px}
    button{background:#00ff88;color:black;font-weight:bold;cursor:pointer}
    .resultado{background:#1e1e2e;padding:30px;margin-top:30px;border-radius:15px;text-align:left;line-height:2}
    a{color:#58a6ff}
</style>
</head>
<body>
<div class="box">
<h1>VagasFreela BR</h1>
<form><input name="skill" placeholder="python, design, tradução..." required><button>Buscar vagas!</button></form>
<div class="resultado">{{resultado|safe}}</div>
</div>
</body></html>
'''

@app.route("/")
def home():
    skill = request.args.get("skill", "").strip().lower()
    if not skill:
        return render_template_string(HTML, resultado="<br>Digite uma skill e veja as vagas reais aparecerem!")

    urls = [
        f"https://www.workana.com/jobs/rss?country=BR&skills={skill}",
        f"https://www.99freelas.com.br/projects.rss?q={skill}",
        f"https://www.upwork.com/ab/jobs/rss?search={skill}",
        f"https://www.freelancer.com/rss.xml?q={skill}"
    ]

    vagas = []
    for url in urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:20]:
                plat = url.split("/")[2].split(".")[0].title()
                vagas.append(f"• <strong>{entry.title}</strong><br>   {plat} → <a href='{entry.link}' target='_blank'>{entry.link}</a>")
        except: continue

    if not vagas:
        res = "<br>Nenhuma vaga agora. Tenta outra skill!"
    else:
        res = f"<h2>Encontrei {len(vagas)} vagas de <u>{skill.upper()}</u></h2><br>" + "<br>".join(vagas[:15])

    return render_template_string(HTML, resultado=res)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
