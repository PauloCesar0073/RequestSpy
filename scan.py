import argparse
import socket
import re
from colorama import Fore, Style
from urllib.parse import urlparse

def get_domain_from_url(url):
    try:
        parsed_url = urlparse(url)
        return parsed_url.netloc.split(":")[0]  # Remover a parte após ":"
    except:
        return None

def get_domain_from_servers(server_line):
    try:
        return server_line.split("Server:" and"server:")[1].strip()  # Capturar o que vem após "Server:"
    except:
        return None

def get_ip_from_domain(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        return None
    

def get_ip_from_encrypton(text):
    try:
        return text.split("encryption:")[1].strip()  # Capturar o que vem após "encryption:"
    except:
        return None



def scanar(arquivo, output_file=None):
    output_stream = open(output_file, "w") if output_file else None

    with open(arquivo, "r") as f:
        data = f.read()

    # Criamos conjuntos para armazenar os IPs, domínios e servidores verificados
    ips_verificados = set()
    dominios_verificados = set()
    servers_verificados = set()
    encryptaciones = set()

    # Neste exemplo, estamos verificando o IP de cada servidor e URL
    for line in data.splitlines():
        # Utilizamos expressão regular para encontrar URLs no formato http:// ou https://
        urls = re.findall(r"https?://\S+", line)
        for url in urls:
            # Verificamos se a URL já foi verificada anteriormente
            if url in dominios_verificados:
                continue

            dominios_verificados.add(url)

            domain = get_domain_from_url(url)
            if domain:
                # Verificamos se o domínio já foi verificado anteriormente
                if domain in ips_verificados:
                    continue

                ips_verificados.add(domain)

                ip = get_ip_from_domain(domain)
                output_text = f"\n\n{Fore.GREEN}Domínio: {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX}{domain}\n"
                if ip:
                    output_text += f"{Fore.GREEN}IP: {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX}{ip}"
                else:
                    output_text += "IP não encontrado\n\n"

                print(f"{Fore.GREEN}{output_text}{Style.RESET_ALL}")
                if output_stream:
                    output_stream.write(output_text)

        # Verificamos se a linha contém informações sobre o servidor
        if "Server:" in line or "server:" in line:
            server = get_domain_from_servers(line)
            if server:
                # Verificamos se o servidor já foi verificado anteriormente
                if server in servers_verificados:
                    continue

                servers_verificados.add(server)
                output_text = f"{Fore.GREEN}Servidor: {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX}{server}\n\n"
                print(f"{Fore.GREEN}{output_text}{Style.RESET_ALL}")
                if output_stream:
                    output_stream.write(output_text)




        # Verificamos se a linha contém informações sobre a encryption
        if "encryption:" in line:
            ecp = get_ip_from_encrypton(line)
            if ecp:
                # Verificamos se o servidor já foi verificado anteriormente
                if ecp in encryptaciones:
                    continue

                encryptaciones.add(ecp)
                output_text = f"{Fore.GREEN}Encriptação: {Style.RESET_ALL}{Fore.LIGHTYELLOW_EX}{ecp}"
                print(f"{Fore.GREEN}{output_text}{Style.RESET_ALL}")
                if output_stream:
                    output_stream.write(output_text)

















    if output_stream:
        output_stream.close()

def mostrar_ajuda():
    print("Uso: python3 scan.py <arquivo> [-o <arquivo_saida>]")
    print("Descrição: Analisa um arquivo de informações capturadas.")
    print("Exemplo: python3 scan.py arquivo.txt -o saida.txt")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("arquivo", nargs="?", help="Nome do arquivo com as informações capturadas.")
    parser.add_argument("-o", dest="output_file", help="Redirecionar a saída para um arquivo.")
    args, unknown_args = parser.parse_known_args()

    if "--help" in unknown_args or args.arquivo is None:
        mostrar_ajuda()
    else:
        scanar(args.arquivo, args.output_file)
