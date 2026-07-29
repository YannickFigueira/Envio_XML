import glob
import os, shutil
import xml.etree.ElementTree as ET


def separar_notas(pasta_origem, pasta_destino, estado):
    global root
    ns = {"nfe": "http://www.portalfiscal.inf.br/nfe"}

    # Criar pasta destino se não existir
    os.makedirs(pasta_destino, exist_ok=True)

    match estado:
        case "cancelado":
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
        case "contingencia":
            # Busca por todos os arquivos .xml na pasta de origem
            for arquivo in glob.glob(os.path.join(pasta_origem, "*.xml")):
                try:
                    tree = ET.parse(arquivo)
                    root = tree.getroot()

                    # Procura a tag xJust no XML
                    xjust_element = root.find(".//nfe:xJust", ns)

                    if xjust_element is None:
                        for elem in root.iter():
                            if elem.tag.endswith("xJust"):
                                xjust_element = elem
                                break

                    # CONDIÇÃO: Se xJust foi encontrado
                    if xjust_element is not None and xjust_element.text:
                        #print(f"[{os.path.basename(arquivo)}] xJust encontrado: {xjust_element.text}")

                        # Procura a tag infNFe
                        inf_nfe = root.find(".//nfe:infNFe", ns)

                        if inf_nfe is None:
                            for elem in root.iter():
                                if elem.tag.endswith("infNFe"):
                                    inf_nfe = elem
                                    break

                        if inf_nfe is not None and "Id" in inf_nfe.attrib:
                            # Extrai a chave de 44 dígitos
                            chave_nfe = inf_nfe.attrib["Id"].replace("NFe", "")

                            # Define o caminho de destino salvando com a chave extraída (ex: 3521...-nfe.xml)
                            caminho_destino = os.path.join(pasta_destino, f"{chave_nfe}-nfe.xml")

                            # Copia o arquivo atual para a pasta de destino
                            shutil.move(arquivo, caminho_destino)
                            #print(f"Copiado com sucesso -> {caminho_destino}")

                except ET.ParseError:
                    return
                    #print(f"Erro ao ler o XML: {arquivo}")
                except Exception as e:
                    return
                    #print(f"Erro ao processar {arquivo}: {e}")