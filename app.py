from flask import Flask, request, render_template_string
import imaplib
import email

app = Flask(__name__)

HTML = '''
<!doctype html>
<title>Lector de Correo</title>
<h1>Conectar a un servidor IMAP</h1>
<form method="post">
  <label>Servidor IMAP: <input name="server" value="{{ server }}" required></label><br>
  <label>Usuario: <input name="username" value="{{ username }}" required></label><br>
  <label>Contraseña: <input type="password" name="password" required></label><br>
  <button type="submit">Leer correos</button>
</form>
{% if error %}
<p style="color:red;">{{ error }}</p>
{% endif %}
{% if messages %}
<h2>Últimos correos</h2>
<ul>
  {% for msg in messages %}
  <li><strong>{{ msg['subject'] }}</strong> - {{ msg['from'] }}</li>
  {% endfor %}
</ul>
{% endif %}
'''


def fetch_messages(server, username, password, limit=10):
    """Conecta a un servidor IMAP y obtiene los últimos correos."""
    mail = imaplib.IMAP4_SSL(server)
    mail.login(username, password)
    mail.select('inbox')
    status, data = mail.search(None, 'ALL')
    if status != 'OK':
        raise RuntimeError('No se pudo buscar en la bandeja de entrada')
    ids = data[0].split()
    messages = []
    for num in ids[-limit:]:
        status, msg_data = mail.fetch(num, '(RFC822)')
        if status != 'OK':
            continue
        msg = email.message_from_bytes(msg_data[0][1])
        messages.append({'subject': msg.get('subject', ''), 'from': msg.get('from', '')})
    return list(reversed(messages))


@app.route('/', methods=['GET', 'POST'])
def index():
    server = ''
    username = ''
    if request.method == 'POST':
        server = request.form['server']
        username = request.form['username']
        password = request.form['password']
        try:
            messages = fetch_messages(server, username, password)
            return render_template_string(HTML, messages=messages, server=server, username=username)
        except Exception as exc:
            return render_template_string(HTML, error=str(exc), messages=None, server=server, username=username)
    return render_template_string(HTML, messages=None, server=server, username=username)


if __name__ == '__main__':
    app.run(debug=True)
