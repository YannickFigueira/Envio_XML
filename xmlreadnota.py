import xml.etree.ElementTree as ET
import glob
import relatorio

def ler_dados_notas(caminho, dados):

    #caminho = "/home/yannick/Downloads/23847090000156_202602_0_documentos/*.xml"
    #caminho = "/home/yannick/Documentos/Development/EnviarXMLPython/leitura"

    soma_valores = 0
    soma_valores_nota = 0

    # Namespace da NF-e
    ns = {"nfe": "http://www.portalfiscal.inf.br/nfe"}
    # Variaveis globais
    modelo = 0

    # Variaveis DANFE
    index_danfe = 0
    nota_danfe = ""
    serie = ""
    data_nota_danfe = ""
    cliente = ""
    valor_produto_danfe = ""
    valor_frete_danfe = ""
    valor_desc_danfe = ""
    valor_nota_danfe = ""
    soma_valores_danfe = 0
    soma_desc_danfe = 0
    soma_total_danfe = 0

    # Variaveis NFCE
    index_nfce = 0
    estabelecimento = ""
    data_nota = ""
    data_nota_soma = ""
    nota_numero = ""
    produto = ""
    qtd = ""
    valor_unidade = ""
    valor_total_notas = ""
    nota_numero_soma = ""

    conta_nota = 0
    valor_qtd = ""
    for arquivo in glob.glob(caminho + "/*.xml"):
        tree = ET.parse(arquivo)
        root = tree.getroot()

        # Procurar a tag vNF dentro do namespace
        for elem in root.findall(".//nfe:mod", ns):
            try:
                # soma_valores += float(elem.text)
                modelo = int(elem.text)
                #print(modelo)
                # print(qtd)

            except (TypeError, ValueError):
                pass

        match modelo:
            case 55:
                #print("Lendo DANFE")
                # Procurar a tag nNF dentro do namespace
                for elem in root.findall(".//nfe:nNF", ns):
                    try:
                        match len(elem.text):
                            case 1:
                                nota_danfe += "00000000" + elem.text + ","
                            case 2:
                                nota_danfe += "0000000" + elem.text + ","
                            case 3:
                                nota_danfe += "000000" + elem.text + ","
                            case 4:
                                nota_danfe += "00000" + elem.text + ","
                            case 5:
                                nota_danfe += "0000" + elem.text + ","
                            case 6:
                                nota_danfe += "000" + elem.text + ","
                            case 7:
                                nota_danfe += "00" + elem.text + ","
                            case 8:
                                nota_danfe += "0" + elem.text + ","
                            case _:
                                nota_danfe += elem.text + ","
                    except (TypeError, ValueError):
                        pass

                # Procurar a tag serie dentro do namespace
                for elem in root.findall(".//nfe:serie", ns):
                    try:
                        serie += "00" + elem.text + ","
                    except (TypeError, ValueError):
                        pass

                # Procurar a tag dhEmi dentro do namespace
                for elem in root.findall(".//nfe:dhEmi", ns):
                    try:
                        anomesdia_danfe = elem.text.split("T")
                        ajuste_data_danfe = anomesdia_danfe[0].split("-")
                        montar_data_danfe = ajuste_data_danfe[2] + "/" + ajuste_data_danfe[1] + "/" + ajuste_data_danfe[0]
                        data_nota_danfe += montar_data_danfe + ","
                    except (TypeError, ValueError):
                        pass

                # Procurar a tag xNome dentro do namespace
                for dest in root.findall(".//nfe:emit", ns):
                    try:
                        if dest is not None:
                            xnome_dest = dest.find(".//nfe:xNome", ns)
                            estabelecimento = xnome_dest.text
                    except (TypeError, ValueError):
                        pass

                # Procurar a tag xNome dentro do namespace
                for dest in root.findall(".//nfe:dest", ns):
                    try:
                        if dest is not None:
                            xnome_dest = dest.find(".//nfe:xNome", ns)
                            cliente += xnome_dest.text + ","
                    except (TypeError, ValueError):
                        pass

                # Procurar a tag vProd dentro do namespace
                for total in root.findall(".//nfe:total", ns):
                    try:
                        if total is not None:
                            xprod_total = total.find(".//nfe:vProd", ns)
                            valor_produto_danfe += xprod_total.text + ","
                            soma_valores_danfe += float(xprod_total.text)

                            vfrete_total = total.find(".//nfe:vFrete", ns)
                            valor_frete_danfe += vfrete_total.text + ","

                            vdesc_total = total.find(".//nfe:vDesc", ns)
                            valor_desc_danfe += vdesc_total.text + ","
                            soma_desc_danfe += float(vdesc_total.text)

                            nota_total = total.find(".//nfe:vNF", ns)
                            valor_nota_danfe += nota_total.text + ","
                            soma_total_danfe += float(nota_total.text)

                    except (TypeError, ValueError):
                        pass
                index_danfe += 1


            case 65: ##### Cupom fiscal #####
                #print("Lendo Cupom")
                # Procurar a tag xNome dentro do namespace
                for elem in root.findall(".//nfe:xNome", ns):
                    try:
                        estabelecimento = elem.text
                    except (TypeError, ValueError):
                        pass

                # Procurar a tag vNF dentro do namespace
                for elem in root.findall(".//nfe:nNF", ns):
                    try:
                        nota_numero = elem.text + ","
                    except (TypeError, ValueError):
                        pass

                # Procurar a tag dhEmi dentro do namespace
                for elem in root.findall(".//nfe:dhEmi", ns):
                    try:
                        anomesdia = elem.text.split("T")
                        ajuste_data = anomesdia[0].split("-")
                        montar_data = ajuste_data[2] + "/" + ajuste_data[1] + "/" + ajuste_data[0]
                        data_nota = montar_data + ","
                    except (TypeError, ValueError):
                        pass

                # Procurar a tag qCom dentro do namespace
                for elem in root.findall(".//nfe:qCom", ns):
                    try:
                        qtd += elem.text + ","
                    except (TypeError, ValueError):
                        pass

                # Procurar a tag xProd dentro do namespace
                for elem in root.findall(".//nfe:xProd", ns):
                    try:
                        produto += elem.text + ","
                    except (TypeError, ValueError):
                        pass

                valor_qtd = qtd.split(",")
                conta_nota = 0

                # Procurar a tag vUnCom dentro do namespace
                for elem in root.findall(".//nfe:vUnCom", ns):
                    try:
                        soma_valores_nota = str(float(elem.text) * float(valor_qtd[index_nfce]))
                        valor_unidade += str(float(elem.text)) + ","
                        valor_total_notas += soma_valores_nota + ","
                        index_nfce += 1
                        conta_nota += 1
                    except (TypeError, ValueError):
                        pass

                nota_numero = conta_nota*nota_numero
                nota_numero_soma += nota_numero
                data_nota = conta_nota*data_nota
                data_nota_soma += data_nota

                # Procurar a tag vNF dentro do namespace
                for elem in root.findall(".//nfe:vNF", ns):
                    try:
                        soma_valores += float(elem.text)
                    except (TypeError, ValueError):
                        pass

    #separador da DANFE
    nota_danfe_array = nota_danfe.split(",")
    serie_array = serie.split(",")
    data_array = data_nota_danfe.split(",")
    cliente_array = cliente.split(",")
    valor_produto_array =valor_produto_danfe.split(",")
    valor_frete_array = valor_frete_danfe.split(",")
    valor_desc_array = valor_desc_danfe.split(",")
    valor_nota_array =valor_nota_danfe.split(",")

    sortear_danfe = ""
    for i in range(index_danfe):
        sortear_danfe += (f"{nota_danfe_array[i]} -> {serie_array[i]} -> {data_array[i]} -> {cliente_array[i]} -> {valor_produto_array[i]} "
                          f"-> {valor_frete_array[i]} -> {valor_desc_array[i]} -> {valor_nota_array[i]};")

    nota_danfe_relatorio = ""
    serie_relatorio = ""
    data_relatorio= ""
    cliente_relatorio = ""
    valor_produto_relatorio = ""
    valor_frete_relatorio = ""
    valor_desc_relatorio = ""
    valor_nota_relatorio = ""

    sorteardf = sortear_danfe.split(";")
    sorteardf = sorted(sorteardf, key=lambda x: str(x).lower())

    for sortear_item in sorteardf:
        if sortear_item != "":
            separar = sortear_item.split("->")

            nota_danfe_relatorio += separar[0] + ","
            #print(separar[0])
            serie_relatorio += separar[1] + ","
            data_relatorio += separar[2] + ","
            cliente_relatorio += separar[3] + ","
            valor_produto_relatorio += separar[4] + ","
            valor_frete_relatorio += separar[5] + ","
            valor_desc_relatorio += separar[6] + ","
            valor_nota_relatorio += separar[7] + ","

    if index_danfe != 0:
        faltantes = ""
        nota = nota_danfe_relatorio.split(",")
        notas_totais = int(nota[len(nota)-2]) - int(nota[0]) + 1
        #print(notas_totais)
        #print(len(nota) - 1)
        #print(nota[len(nota) - 2]) # Notas registradas
        if nota != notas_totais:
            contador = notas_totais
            valor_nota = int(nota[0])
            lista1 = list(range(valor_nota, valor_nota + contador))

            # Converter para inteiros, ignorando strings vazias
            lista2 = [int(x) for x in nota if x.strip().isdigit()]

            # Guardar todos os faltantes em uma lista
            faltantes = [x for x in lista1 if x not in lista2]

            #print(faltantes)

        dados.config["notas"]["ultima_nota_danfe"] = nota[len(nota) - 2].replace(" ", "")
        dados.gravar()

        relatorio.htm_danfe(estabelecimento, nota_danfe_relatorio.split(","), serie_relatorio.split(","), data_relatorio.split(","), cliente_relatorio.split(","),
                        valor_produto_relatorio.split(","),valor_frete_relatorio.split(","), valor_desc_relatorio.split(","),
                        valor_nota_relatorio.split(","), soma_valores_danfe, soma_desc_danfe, soma_total_danfe, faltantes)

    # separador do NFCE
    valor = produto.split(",")
    nota_fiscal = nota_numero_soma.split(",")
    qtds = qtd.split(",")
    valor_unidades = valor_unidade.split(",")
    valor_total_notassplit = valor_total_notas.split(",")
    sortear = ""

    for i in range(index_nfce):
        sortear += f"{nota_fiscal[i]} -> {valor[i]} -> {qtds[i]} -> {valor_unidades[i]} -> {valor_total_notassplit[i]};"

    nf_numero = ""
    p_nome= ""
    qtd_produto = ""
    valor_produto = ""
    valor_total_produto = ""

    sortears = sortear.split(";")
    sortears = sorted(sortears, key=lambda x: str(x).lower())
    cupom = ""
    for sortear_item in sortears:
        if sortear_item != "":
            separar = sortear_item.split("->")
            match len(separar[0].replace(" ","")):
                case 1:
                    nf_numero += "00000" + separar[0] + ","
                case 2:
                    nf_numero += "0000" + separar[0] + ","
                case 3:
                    nf_numero += "000" + separar[0] + ","
                case 4:
                    nf_numero += "00" + separar[0] + ","
                case 5:
                    nf_numero += "0" + separar[0] + ","
                case _:
                    nf_numero += separar[0] + ","

            #print(separar[0])
            if cupom != separar[0]:
                cupom = separar[0]
                #print(cupom)
            p_nome += separar[1] + ","
            qtd_produto += separar[2] + ","
            valor_produto += separar[3] + ","
            valor_total_produto += separar[4] + ","

    if index_nfce != 0:
        faltantes = ""
        nota = nf_numero.split(",")
        notas_totais = int(nota[len(nota) - 2]) - int(nota[0]) + 1
        # print(notas_totais)
        # print(len(nota) - 1)
        # print(nota[len(nota) - 2]) # Notas registradas
        if nota != notas_totais:
            contador = notas_totais
            valor_nota = int(nota[0])
            lista1 = list(range(valor_nota, valor_nota + contador))

            # Converter para inteiros, ignorando strings vazias
            lista2 = [int(x) for x in nota if x.strip().isdigit()]

            # Guardar todos os faltantes em uma lista
            faltantes = [x for x in lista1 if x not in lista2]

            #print(faltantes)

        nota = nf_numero.split(",")
        #print(nota[len(nota)-2])
        dados.config["notas"]["ultima_nota_nfce"] = nota[len(nota) - 2].replace(" ", "")
        dados.gravar()

        relatorio.htm_nfce(estabelecimento, data_nota_soma.split(","), nf_numero.split(","), p_nome.split(","), qtd_produto.split(","),
                       valor_produto.split(","), valor_total_produto.split(","), soma_valores, faltantes)


#ler_dados_notas("texto")