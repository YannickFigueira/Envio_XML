# estilo.py
import os
from pathlib import Path

# Versão e repositório
VERSION = "v4.1.4rc2"
REPO= "Envio_XML"
NOME_PROGRAMA = "Envio XML"

# Pastas do programa
home_dir = os.path.expanduser('~')
programa_dir = f"{home_dir}/.envio xml"
notas = f"{home_dir}/.envio xml/notas"
log_files = Path(f"{home_dir}/.envio xml/logs")

if not os.path.exists(programa_dir):
    os.mkdir(programa_dir)
if not os.path.exists(notas):
    os.mkdir(notas)
if not os.path.exists(log_files):
    os.mkdir(log_files)

# Margens padrão para janelas e frames
# Medidas
ESPACO = 5
LINHA_PAINEL_ESQUERDO = 0

# Margens padrão para janelas e frames
PADX_JANELA = 20
PADY_JANELA = 20

# Margens padrão para componentes menores (botões, inputs, labels)
PADX_COMPONENTE = 10
PADY_COMPONENTE = 5

# Estilo
FONTE_VAZIA=("", 11, "normal")
FONTE_ARIAL=("Arial", 11, "normal")

# Arquivo de log
ARQUIVO_ERRO = "envio_xml.log"

# Variáveis gerais
# Caminho dos sistemas
PASTA_PROGRAMAS = "C:\\Program Files (x86)"
SMALL_COMMERCE = f"{PASTA_PROGRAMAS}\\SmallSoft\\Small Commerce"
COMERCIAL = f"{PASTA_PROGRAMAS}\\Comercial"
# Strings
MES_STR = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro",
               "Novembro", "Dezembro"]