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
    
    agenda.btn_consultar.clicked.connect(consultarContatos)
def consultarContatos():
    listarContatos.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM contatos"
    cursor.execute(comando_SQL)
    contatosLidos = cursor.fetchall()

    listarContatos.tabelaContatos.setRowCount(len(contatosLidos))
    listarContatos.tabelaCOntatos.setColunCount(5)

    for i in range (0, len(contatosLidos)):
        for f in range(0,5):
            listarContatos.tabelaCOntatos.setItem(i, f, QtWidgets.QTableWidgetItem(str(contatosLidos[i][f])))

# def main():
app =  QtWidgets.QApplication([])
agenda=uic.loadUi("Agendamento.ui")
listarContatos = uic.loadUi ("ListaContatos.ui")

# agenda.btn_cadastro.clicked.connect(cadastrarContato)

# listarContatos.btn_GeraPdf.clicked.connect(gerarPdf)
def gerarPdf():
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM contatos"
    cursor.execute(comando_SQL)
    contatosLidos = cursor.fetchall()

# listarContatos.btn_ExcluirContato.clicked.connect(excluirContato)
def excluirContato():
    linhaContato = listarContatos.tabelaContatos.currentRow()
    listarContatos.tabelaContatos.removeRow(linhaContato)
    
    cursor = banco.cursor()
    comando_SQL = "SELECT id FROM contatos"
    cursor.execute(comando_SQL)
    contatosLidos = cursor.fetchall()
    valorId = contatosLidos[linhaContato][0]
    cursor.execute("DELETE FROM contatos WHERE id=" + str(valorId))
    banco.commit()

agenda.show()
app.exec()