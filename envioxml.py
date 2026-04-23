import argparse
import janelaconfig

VERSION = "v4.0.0rc1"
repo= "Envio_XML"

parser = argparse.ArgumentParser(prog="envioxml")
parser.add_argument("-v","--version",action="version", version=f"%(prog)s {VERSION}")
args = parser.parse_args()

janelaconfig.iniciar_janela(VERSION, repo)
#janelaconfig.inciar_tray(VERSION, repo)