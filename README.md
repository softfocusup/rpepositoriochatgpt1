# Lector de correos múltiple

Este proyecto proporciona una aplicación web simple en Flask que permite leer correos electrónicos de distintos servidores IMAP (Gmail, Outlook, etc.) desde un solo lugar.

## Requisitos

- Python 3
- Dependencias listadas en `requirements.txt`

## Uso

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta la aplicación:
   ```bash
   python app.py
   ```
3. Abre `http://localhost:5000` en tu navegador e introduce el servidor IMAP, usuario y contraseña.

> **Nota:** Algunos proveedores como Gmail requieren una contraseña de aplicación o configuraciones especiales para permitir conexiones IMAP.
