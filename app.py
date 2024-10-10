from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Cambia esto a una clave más segura

CORS(app, resources={r"/add_mantenimiento": {"origins": "http://127.0.0.1:5500"}})
CORS(app, resources={r"/add_equipo": {"origins": "http://127.0.0.1:5500"}})
# Configura las credenciales
SERVICE_ACCOUNT_FILE = 'municipio-438114-f4c7c183ff5c.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SPREADSHEET_ID = '1lxqo2QXPUNl5COMbIJtEQ0_QgqCE84DGiEF4mJc2iFM'

# Credenciales de usuario
USERS = {
    'user': 'ranchos',
    'admin': 'admin1'
}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in USERS and USERS[username] == password:
        session['username'] = username
        if username == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect('http://127.0.0.1:5500/registrar-mantenimiento.html')
    else:
        flash('Credenciales inválidas')
        return redirect(url_for('home'))

@app.route('/admin')
def admin_dashboard():
    return render_template('index.html')

@app.route('/add_mantenimiento', methods=['POST'])
def add_mantenimiento():
    data = request.json
    ubicacion = data.get('ubicacion')
    equipo_id = data.get('equipoId')
    tipo = data.get('tipo')
    modelo = data.get('modelo')
    estado = data.get('estado')
    notas = data.get('notas')

    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()

    # Agrega una nueva fila en la hoja de cálculo "Mantenimiento"
    row = [ubicacion, equipo_id, tipo, modelo, estado, notas]
    body = {
        'values': [row]
    }

    result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range='Mantenimiento!A:F',  # Asegúrate de que este rango coincida con tu hoja
        valueInputOption='RAW',
        body=body
    ).execute()

    return jsonify(result)


@app.route('/add_equipo', methods=['POST'])  # Cambia el endpoint a /add_equipo
def add_equipo():
    data = request.json
    ubicacion = data.get('ubicacion')
    equipo_id = data.get('equipoId')
    tipo = data.get('tipo')
    modelo = data.get('modelo')
    estado = data.get('estado')
    notas = data.get('notas')
    tipo_conexion = data.get('tipo_conexion')
    ip = data.get('ip')  # Obtiene la IP si aplica

    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()

    # Agrega una nueva fila en la hoja de cálculo "Equipos"
    row = [ubicacion, equipo_id, tipo, modelo, estado, notas, tipo_conexion, ip]  # Usa la información del equipo
    body = {
        'values': [row]
    }

    result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range='Equipos!A:H',  # Cambia esto a tu rango correspondiente
        valueInputOption='RAW',
        body=body
    ).execute()

    return jsonify(result)


@app.route('/get_mantenimiento', methods=['GET'])
def get_mantenimiento():
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()

    # Obtiene los datos de la hoja
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='Mantenimiento!A:F').execute()
    values = result.get('values', [])

    # Retorna los datos en formato JSON
    return jsonify(values)
@app.route('/data/<sheet_name>', methods=['GET'])
def get_data(sheet_name):
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()

    # Obtén los datos de la hoja especificada
    range_name = f'{sheet_name}!A:F'  # Cambia esto si tu rango es diferente
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
    values = result.get('values', [])

    return jsonify(values)
if __name__ == '__main__':
    app.run(debug=True)
