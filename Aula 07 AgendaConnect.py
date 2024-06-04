from PyQt5 import uic, QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@Julia0408",
    database="agenda"
)

agenda=uic.loadUi('Aula 07 Agenda.ui')

def cadastrarContato():
    campoNome = agenda.letNome.text()
    campoEmail = agenda.letEmail.text()
    campoTelefone = agenda.btnCadastro.text()
    
    if agenda.rbResidencial.isChecked():
        tipoTelefone = "Residencial"
    elif agenda.rbCelular.isChecked():
        tipoTelefone = "Celular"
    else:
        tipoTelefone = "Não informado!"
        
    cursor = banco.cursor()
    comando_SQL = "INSERT INTO contatos (nome, email, telefone, tipoTelefone) VALUES (%s, %s, %s, %s)"
    dados = (str(campoNome), str(campoEmail), str(campoTelefone), tipoTelefone)
    cursor.execute(comando_SQL, dados)
    banco.commit()