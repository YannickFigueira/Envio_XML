# novo_projeto.py
import platform
import os

if platform.system() == "Windows":
    destino_dir = "C:\\temp\\XMLs\\relatorio"
    if not os.path.exists(destino_dir):
        os.makedirs(destino_dir)
elif platform.system() == "Linux":
    destino_dir = "/tmp/XMLs/relatorio"
    if not os.path.exists(destino_dir):
        os.makedirs(destino_dir)

# Relatório DANFE
def htm_danfe(estabelecimento, nota, serie, data_nota_danfe, cliente, valor_produto_danfe, valor_frete_danfe, valor_desc_danfe, valor_nota_danfe,
              soma_valores_danfe, soma_desc_danfe, soma_total_danfe, faltantes):

    soma_valores_danfe_formatado = f"{soma_valores_danfe:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    soma_desc_danfe_formatado = f"{soma_desc_danfe:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    soma_total_danfe_formatado = f"{soma_total_danfe:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    produto = ""
    for i in range(len(nota) - 1):
        valor_produto_danfe_formatado = f"{float(valor_produto_danfe[i]):,.2f}".replace(",", "X").replace(".", ",").replace("X",".")
        valor_frete_danfe_formatado = f"{float(valor_frete_danfe[i]):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        valor_desc_danfe_formatado = f"{float(valor_desc_danfe[i]):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        valor_nota_danfe_formatado = f"{float(valor_nota_danfe[i]):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        produto += f"""<tr>
            <td nowrap valign=top bgcolor=#FFFFFF align=left><font face="Microsoft Sans Serif" size=1>{nota[i]}/{serie[i]}<br></font></td>
            <td nowrap valign=top bgcolor=#FFFFFF align=left><font face="Microsoft Sans Serif" size=1>{data_nota_danfe[i]}<br></font></td>
            <td nowrap valign=top bgcolor=#FFFFFF align=left><font face="Microsoft Sans Serif" size=1>{cliente[i]}<br></font></td>
            <td nowrap valign=top bgcolor=#FFFFFF align=right><font face="Microsoft Sans Serif" size=1>   {valor_produto_danfe_formatado}<br></font></td>
            <td nowrap valign=top bgcolor=#FFFFFF align=right><font face="Microsoft Sans Serif" size=1>       0,00<br></font></td>
            <td nowrap valign=top bgcolor=#FFFFFF align=right><font face="Microsoft Sans Serif" size=1>       {valor_frete_danfe_formatado}<br></font></td>
            <td nowrap valign=top bgcolor=#FFFFFF align=right><font face="Microsoft Sans Serif" size=1>       {valor_desc_danfe_formatado}<br></font></td>
            <td nowrap valign=top bgcolor=#FFFFFF align=right><font face="Microsoft Sans Serif" size=1>       0,00<br></font></td>
            <td nowrap valign=top bgcolor=#FFFFFF align=right><font face="Microsoft Sans Serif" size=1>   {valor_nota_danfe_formatado}<br></font></td>
            <td nowrap valign=top bgcolor=#FFFFFF align=right><font face="Microsoft Sans Serif" size=1>       0,00<br></font></td>
           </tr>"""

    registrar_notas = ""
    if faltantes != "":
        registrar_notas = f"<br><font size=4 color=#000000><b>Notas faltando nos XMLs {faltantes}</b></font><br></center><br>"
    conteudo_htm = f"""<html><head><title>{estabelecimento} - Relatório de vendas</title></head>
    <body bgcolor="#FFFFFF" vlink="#FF0000" leftmargin="0"><center>
    <br>Relatório gerado a partir dos XMLs emitidos
    <br><img src="logotip.jpg" alt="{estabelecimento}">
    <br><font size=3 color=#000000><b>{estabelecimento}</b></font>
    <br><font size=4 color=#000000><b>Relatório de vendas</b></font>
    {registrar_notas}
    <center>
    <table border=0>
     <tr>
      <td>
       <table border=1 style="border-collapse:Collapse" cellspacing=0 cellpadding=4>
        <tr bgcolor=EBEBEB align=left>
         <th nowrap><font face="Microsoft Sans Serif" size=1>Nota</font></th>
         <th nowrap><font face="Microsoft Sans Serif" size=1>Data</font></th>
         <th nowrap><font face="Microsoft Sans Serif" size=1>Cliente</font></th>
         <th nowrap><font face="Microsoft Sans Serif" size=1>Produtos R$</font></th>
         <th nowrap><font face="Microsoft Sans Serif" size=1>Serviços R$</font></th>
         <th nowrap><font face="Microsoft Sans Serif" size=1>Frete R$</font></th>
         <th nowrap><font face="Microsoft Sans Serif" size=1>Desconto R$</font></th>
         <th nowrap><font face="Microsoft Sans Serif" size=1>Outras R$</font></th>
         <th nowrap><font face="Microsoft Sans Serif" size=1>Total R$</font></th>
         <th nowrap><font face="Microsoft Sans Serif" size=1>ICMS R$</font></th>
        </tr>
        {produto}
        <tr bgcolor=EBEBEB align=left>
         <td nowrap valign=top align=left><font face="Microsoft Sans Serif" size=1><br></font></td>
         <td nowrap valign=top align=left><font face="Microsoft Sans Serif" size=1><br></font></td>
         <td nowrap valign=top align=left><font face="Microsoft Sans Serif" size=1><br></font></td>
         <td nowrap valign=top align=right><font face="Microsoft Sans Serif" size=1><b>  {soma_valores_danfe_formatado}<br></font></td>
         <td nowrap valign=top align=right><font face="Microsoft Sans Serif" size=1><b>       0,00<br></font></td>
         <td nowrap valign=top align=right><font face="Microsoft Sans Serif" size=1><b>       0,00<br></font></td>
         <td nowrap valign=top align=right><font face="Microsoft Sans Serif" size=1><b>       {soma_desc_danfe_formatado}<br></font></td>
         <td nowrap valign=top align=right><font face="Microsoft Sans Serif" size=1><b>       0,00<br></font></td>
         <td nowrap valign=top align=right><font face="Microsoft Sans Serif" size=1><b>  {soma_total_danfe_formatado}<br></font></td>
         <td nowrap valign=top align=right><font face="Microsoft Sans Serif" size=1><b>       0,00<br></font></td>
        </tr>
       </table></center>
       </td>
      </table>
      <font face="Microsoft Sans Serif" size=1><br>Período analisado, de 01/03/2021 até 31/03/2021<br></center>
    <center><br><font face="Microsoft Sans Serif" size=1>Gerado em Itaguaí, 08 de Abril de 2021 às 16:09:53</font><br>
    <font face="verdana" size=1><center>Relatório gerado pelo sistema XMLEnvio, <a href="https://github.com/YannickFigueira"> github.com/YannickFigueira</a><font>
    <font face="Microsoft Sans Serif" size=1><center>Tempo para gerar este relatório: 00:00:00</center>
    </html>"""

    # grava o conteúdo no arquivo
    with open(f"{destino_dir}/danfe.htm", "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo_htm)

# Relatório NFCE
def htm_nfce(estabelecimento, data_nota, nota_numero,produto_nome, qtd, valor_unidade, total_notas, total, faltantes):

    total_formatado = f"{total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    produto = ""
    for i in range(len(total_notas) - 1):
        qtd_formatado = f"{float(qtd[i]):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        valor_unidade_formatado = f"{float(valor_unidade[i]):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        total_notas_formatado = f"{float(total_notas[i]):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        produto += f"""<tr>
            <td nowrap valign=top bgcolor=#FFFFFF align=left><font face="Microsoft Sans Serif" size=1>{nota_numero[i]}<br></font></td>
            <td nowrap valign=top bgcolor=#FFFFFF align=left><font face="Microsoft Sans Serif" size=1>{data_nota[i]}<br></font></td>
            <td nowrap valign=top bgcolor=#FFFFFF align=left><font face="Microsoft Sans Serif" size=1>{produto_nome[i]}<br></font></td>
            <td nowrap valign=top bgcolor=#FFFFFF align=right><font face="Microsoft Sans Serif" size=1>{qtd_formatado}<br></font></td>
            <td nowrap valign=top bgcolor=#FFFFFF align=right><font face="Microsoft Sans Serif" size=1>{valor_unidade_formatado}<br></font></td>
            <td nowrap valign=top bgcolor=#FFFFFF align=right><font face="Microsoft Sans Serif" size=1>{total_notas_formatado}<br></font></td>
           </tr>"""

    registrar_notas = ""
    if faltantes != "":
        registrar_notas = f"<br><font size=4 color=#000000><b>Notas faltando nos XMLs {faltantes}</b></font><br></center><br>"
    conteudo_htm = f"""<html><head><title>{estabelecimento} - Relatório de vendas (Cupom Fiscal)</title></head>
    <body bgcolor="#FFFFFF" vlink="#FF0000" leftmargin="0"><center>
    <br>Relatório gerado a partir dos XMLs emitidos
    <br><img src="logotip.jpg" alt="{estabelecimento}">
    <br><font size=3 color=#000000><b>{estabelecimento}</b></font>
    <br><font size=4 color=#000000><b>Relatório de vendas (Cupom Fiscal)</b></font>
    {registrar_notas}
    <center>
    <table border=1 style="border-collapse:Collapse" cellspacing=0 cellpadding=4>
     <tr  bgcolor=#EBEBEB   align=left>
      <th nowrap><font face="Microsoft Sans Serif" size=1>Cupom</font></th>
      <th nowrap><font face="Microsoft Sans Serif" size=1>Data</font></th>
      <th nowrap><font face="Microsoft Sans Serif" size=1>Descrição do item</font></th>
      <th nowrap><font face="Microsoft Sans Serif" size=1>Quantidade</font></th>
      <th nowrap><font face="Microsoft Sans Serif" size=1>Unitário R$</font></th>
      <th nowrap><font face="Microsoft Sans Serif" size=1>Total R$</font></th>
     </tr>
        {produto}
       <tr bgcolor=#EBEBEB >
         <td nowrap valign=top align=left><font face="Microsoft Sans Serif" size=1><br></font></td>
         <td nowrap valign=top align=left><font face="Microsoft Sans Serif" size=1><br></font></td>
         <td nowrap valign=top align=left><font face="Microsoft Sans Serif" size=1><br></font></td>
         <td nowrap valign=top align=left><font face="Microsoft Sans Serif" size=1><br></font></td>
         <td nowrap valign=top align=left><font face="Microsoft Sans Serif" size=1><br></font></td>
         <td nowrap valign=top bgcolor=#FFFFFF align=right><font face="Microsoft Sans Serif" size=1><b>  {total_formatado}<br></font></td>
        </tr>
       </table>
    <font face="Microsoft Sans Serif" size=1><br>Período analisado, de 01/03/2021 até 31/03/2021<br>
    </center>
    <center><br><font face="Microsoft Sans Serif" size=1>Gerado em Itaguaí, 08 de Abril de 2021 às 16:14:08</font><br>
    <font face="verdana" size=1><center>Relatório gerado pelo sistema XMLEnvio, <a href="https://github.com/YannickFigueira"> github.com/YannickFigueira</a><font>
    <font face="Microsoft Sans Serif" size=1><center>Tempo para gerar este relatório: 00:00:00</center>
    </html>"""

    # grava o conteúdo no arquivo
    with open(f"{destino_dir}/nfce.htm", "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo_htm)
