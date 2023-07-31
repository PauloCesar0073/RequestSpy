import argparse
import socket
from colorama import Fore, Style

def get_ip_from_host(host):
    try:
        ip = socket.gethostbyname(host)
        return ip
    except socket.gaierror:
        return None

def scanar(arquivo):
    with open(arquivo, "r") as f:
        data = f.read()

    # Criamos um conjunto para armazenar os hosts já verificados
    hosts_verificados = set()

    # Realize aqui a lógica de scan desejada
    # Neste exemplo, estamos verificando o IP de cada host
    for line in data.splitlines():
        if "Host" in line:
            host = line.split(":")[1].strip()

            # Verificamos se o host já foi verificado anteriormente
            if host not in hosts_verificados:
                ip = get_ip_from_host(host)
                if ip:
                    print(f"HOST: {Fore.GREEN}{host}{Style.RESET_ALL} - IP: {Fore.BLUE}{ip}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.GREEN}{host}{Style.RESET_ALL} - {Fore.RED}Host não encontrado{Style.RESET_ALL}")

                # Adicionamos o host verificado ao conjunto
                hosts_verificados.add(host)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("arquivo", help="Nome do arquivo com as informações capturadas.")
    args = parser.parse_args()

    scanar(args.arquivo)

