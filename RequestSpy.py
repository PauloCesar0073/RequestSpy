import asyncio
import websockets
import argparse
from colorama import Fore, Style
import re
def show_usage():
    print(Fore.LIGHTYELLOW_EX + "Modo de Usar:", Style.RESET_ALL, "\n\n", Fore.LIGHTGREEN_EX,
          "python3 RequestSpy.py", Style.RESET_ALL,"[opção]\n\n",
          Fore.LIGHTYELLOW_EX + "Opções:\n\n", Style.RESET_ALL +
          "POST\t\t\t Captura as requisições do tipo POST\n",
          "GET\t\t\t Captura as requisições do tipo GET\n",
          "PUT\t\t\t Captura as requisições do tipo PUT\n",
          "DELETE\t\t\t Captura as requisições do tipo DELETE\n",
          "all\t\t\t Captura todas as requisições\n\n",
          "--url ou -u\tFiltra a captura para determinado site especificado\n\n",
          "Opção para redirecionar saída:\n\n",
          "-o arquivo_saida\t Redireciona a saída para um arquivo"
          )

def remove_color_sequences(text):
    # Remove as sequências de escape do Colorama do texto
    color_pattern = re.compile(r'\x1b\[\d{1,2}m')
    return color_pattern.sub('', text)





# Restante do código, incluindo a função handle_client (não modifique a função handle_client)

async def handle_client(websocket, path):
    solicitation_data = None  # Armazena os dados da solicitação pendente

    while True:
        try:
            # Recebe uma mensagem do cliente
            message = await websocket.recv()
            data = eval(message)

            if "url" in data and "type" in data and "headers" in data and "requestType" in data:
                url = data["url"]
                req_type = data["type"]
                headers = data["headers"]
                tyype = data["requestType"]

                if args.url and args.url not in url:
                    continue  # Ignorar solicitações cuja URL não contém a URL fornecida pelo usuário

                if isinstance(headers, list):
                    # Se os cabeçalhos forem uma lista, convertê-los para um único dicionário
                    headers_dict = {}
                    for header in headers:
                        headers_dict[header["name"]] = header["value"]
                    headers = headers_dict

                formatted_headers = "\n".join(
                    f"{header}: {value}" for header, value in headers.items()
                )

                if "REQUEST" in req_type:
                    TIPO = str(req_type).replace("REQUEST", f"{Fore.GREEN}SOLICITAÇÃO{Style.RESET_ALL}")
                elif "RESPONSE" in req_type:
                    TIPO = str(req_type).replace("RESPONSE", f"{Fore.YELLOW}RESPOSTA{Style.RESET_ALL}")

                p = f"{TIPO} do tipo {tyype} para: {Fore.BLUE}{url}{Style.RESET_ALL}\n\n\n:::::::::: CABEÇALHO ::::::::::\n\n\n{formatted_headers}\n\n"

                if solicitation_data and solicitation_data["url"] == url:
                    # Imprime a solicitação e a resposta juntas
                    print(f"+{'=' * 60}+\n{solicitation_data['p']}{p}+{'=' * 48}+\n")
                    solicitation_data = None
                else:
                    solicitation_data = {"url": url, "p": p}
                if "GET: ws://127.0.0.1:8888/" not in p:
                    print(p)
                    if args.output:
                        with open(args.output, "a") as f:
                            f.write(remove_color_sequences(p) + "\n")

        except websockets.exceptions.ConnectionClosedOK:
            print("Cliente fechou a conexão.\n")
            break
















def get_capture_info(option):
    options_map = {
        None: "Capturando Todas Requisições.",
        "all": "Capturando Todas Requisições.",
        "POST": "Capturando Requisições do tipo POST",
        "DELETE": "Capturando Requisições do tipo DELETE",
        "PUT": "Capturando Requisições do tipo PUT",
        "GET": "Capturando Requisições do tipo GET"
    }
    return options_map.get(option, "Opção inválida")

import asyncio
import websockets
import argparse
from colorama import Fore, Style
import re


# Restante do código, incluindo a função handle_client (não modifique a função handle_client)

def main():
    try:
        # Configuração e inicialização do servidor WebSocket
        start_server = websockets.serve(handle_client, "127.0.0.1", 8888)
        print(Fore.LIGHTYELLOW_EX + f"☠️ {get_capture_info(args.option)}\n\nPARA SAIR DIGITE",
              Fore.RED + "CTRL+C", Style.RESET_ALL)

        # Executa o servidor no loop de eventos assíncronos
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    except websockets.exceptions.ConnectionClosedError as e:
        print(Fore.RED + f"Erro durante a execução: {e}\n", Style.RESET_ALL)

    except OSError:
        print(Fore.RED + "Porta 8888 está em uso! Certifique-se de matar todos os processos na porta 8888", Style.RESET_ALL)
    except KeyboardInterrupt:
        print(Fore.RED + "\nCaptura finalizada !\n", Style.RESET_ALL)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("option", choices=["all", "GET", "POST", "PUT", "DELETE"], nargs='?', help="Tipo de requisição a ser capturada.")
    parser.add_argument("-o", "--output", help="Nome do arquivo para redirecionar a saída.")
    parser.add_argument("-u", "--url", help="Filtrar captura por URL.")
    args, unknown_args = parser.parse_known_args()

    if "--help" in unknown_args:
        show_usage()
    elif args.option is None:
        show_usage()
    else:
        main()
