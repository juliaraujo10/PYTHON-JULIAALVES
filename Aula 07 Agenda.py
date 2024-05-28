from PyQt5 import uic, QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="agenda"
)

def cadastrarContato():
    campoNome = agenda.labelNome.text()
    campoEmail = agenda.labelEmail.text()
    campoTelefone = agenda.labelTelefone.text()
    
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
    
def consultarContatos():
    listarContatos.show()
    
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM contatos"
    cursor.execute(comando_SQL)
    contatosLidos = cursor.fetchall()
    
    listarContatos.tabelaContatos.setRowCount(len(contatosLidos))
    listarContatos.tabelaContatos.setColumnCount(5)
    
    for i in range(0, len(contatosLidos)):
        for f in range(0, 5):
            listarContatos.tabelaContatos.setItem(i, f, QtWidgets.QTableWidgetItem(str(contatosLidos[i][f])))

def excluirContato():
    linhaContato = listarContatos.tabelaContatos.currentRow()
    listarContatos.tabelaContatos.removeRow(linhaContato)
    
    cursor = banco.cursor()
    comando_SQL = "SELECT id FROM contatos"
    cursor.execute(comando_SQL)
    contatos_lidos = cursor.fetchall()
    valorId = contatos_lidos[linhaContato][0]
    cursor.execute("DELETE FROM contatos WHERE id=" + str(valorId))
    banco.commit()

def gerarPdf():
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM contatos"
    cursor.execute(comando_SQL)
    contatos_lidos = cursor.fetchall()
    
    y = 0
    pdf = canvas.Canvas("listarContatos.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200, 800, "Lista de Contatos")
    
    pdf.setFont("Times-Bold", 10)
    pdf.drawString(10, 750, "ID")
    pdf.drawString(110, 750, "NOME")
    pdf.drawString(210, 750, "EMAIL")
    pdf.drawString(350, 750, "TELEFONE")
    pdf.drawString(450, 750, "TIPO DE CONTATO")
    
    for i in range(0,len(contatos_lidos)):
        y = y + 50
        pdf.drawString(10, 750 -y, str(contatos_lidos[i][0]))
        pdf.drawString(110, 750 -y, str(contatos_lidos[i][1]))
        pdf.drawString(210, 750 -y, str(contatos_lidos[i][2]))
        pdf.drawString(350, 750 -y, str(contatos_lidos[i][3]))
        pdf.drawString(450, 750 -y, str(contatos_lidos[i][4]))
        
    pdf.save()
    print("PDF gerado com sucesso!")
    
app = QtWidgets.QApplication([])
agenda = uic.loadUi("Aula 07 Agenda.ui")
listarContatos = uic.loadUi("Aula 07 Contatos.ui")

agenda.btnCadastro.clicked.connect(cadastrarContato)
agenda.btnListar.clicked.connect(consultarContatos)

listarContatos.btnGerarPdf.clicked.connect(gerarPdf)
listarContatos.btnExcluirContato.clicked.connect(excluirContato)

agenda.show()
app.exec()