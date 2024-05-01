from PyQt5 import uic, QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    password ="",
    database = "agenda"
)

def CadastrarContato():
    campoNome = agenda.leNome.text()
    campoEmail = agenda.leEmail.text()
    campoTelefone = agenda.leTelefone.text()
    
    if agenda.rbResidencial.isChecked():
        tipoTelefone = "Residencial"
    elif agenda.rbCelular.isChecked():
        tipoTelefone = "Celular"
    else:
        tipoTelefone = "Não informado"
        
    cursor = banco.cursor()
    comando_SQL = "INSERT INTO contatos (nome, email, telefone, tipoTelefone) VALUES (%s, %s, %s, %s)"
    dados = (str(campoNome), str(campoEmail), str(campoTelefone), tipoTelefone)
    cursor.execute(comando_SQL, dados)
    banco.commit()

# def main():
# print ("Etec")

app =  QtWidgets.QApplication([])
agenda=uic.loadUi("Agendamento.ui")
agenda.btn_cadastro.clicked.connect(CadastrarContato)

agenda.show()
app.exec()