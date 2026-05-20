import os, shutil
import xml.etree.ElementTree as ET


def separar_notas(pasta_origem, pasta_destino):
    ns = {"nfe": "http://www.portalfiscal.inf.br/nfe"}

    # Criar pasta destino se não existir
    os.makedirs(pasta_destino, exist_ok=True)

    for arquivo in os.listdir(pasta_origem):
        caminho = os.path.join(pasta_origem, arquivo)

        # Apenas arquivos sem extensão e terminando com "procEventoNFe"
        nome, ext = os.path.splitext(arquivo)
        if os.path.isfile(caminho) and ext == "" and arquivo.endswith("procEventoNFe"):
            try:
                tree = ET.parse(caminho)
                root = tree.getroot()

                # Extrair a chave NFe
                chave = root.find(".//nfe:chNFe", ns)
                if chave is not None and chave.text:
                    chave_nome = chave.text + ".xml"
                    origem_chave = os.path.join(pasta_origem, chave_nome)
                    destino_chave = os.path.join(pasta_destino, chave_nome)

                    # Verificar se o arquivo da chave existe
                    if os.path.exists(origem_chave):
                        shutil.move(origem_chave, destino_chave)
                        #print(f"Movido: {chave_nome}")
                    else:
                        print(f"Arquivo {chave_nome} não encontrado na pasta origem")
                else:
                    print(f"Chave não encontrada em {arquivo}")

            except Exception as e:
                print(f"Erro ao processar {arquivo}: {e}")