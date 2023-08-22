
# RequestSpy - Uma Extensão para Analisar Requisições Web

## Instalação da Extensão

### Google Chrome

1. Abra o Google Chrome e acesse o link `chrome://extensions`.
2. Ative o "Modo de desenvolvedor" no canto superior direito da página.
3. Clique em "Carregar sem compactação".
4. Selecione o diretório da extensão "Ativar_RequestSpy".
5. A extensão será carregada e ativada no navegador.

### Mozilla Firefox

1. Acesse o link [RequestSpy no Firefox Add-ons](https://addons.mozilla.org/pt-BR/firefox/addon/requestspy/).
2. Clique em "Adicionar ao Firefox" para instalar a extensão.







## Modo de Uso

1. Abra um site no seu navegador que deseja analisar as requisições.
2. Inicie o arquivo `RequestSpy.py` escolhendo uma opção de captura.

### Comandos

```bash
./RequestSpy [opção]
```

- `opção`: Escolha o tipo de requisições a serem capturadas.
  - `POST`: Captura as requisições do tipo POST.
  - `GET`: Captura as requisições do tipo GET.
  - `PUT`: Captura as requisições do tipo PUT.
  - `DELETE`: Captura as requisições do tipo DELETE.
  - `all`: Captura todas as requisições.

- `--url` ou `-u`: Filtra a captura para um site específico.

- `-o arquivo_saida`: Redireciona a saída para um arquivo.

## Exemplo de Uso

```bash
python3 RequestSpy.py POST --url https://exemplo.com -o saida.txt
```

Isso capturará apenas as requisições POST do site "https://exemplo.com" e redirecionará a saída para um arquivo chamado "saida.txt".
Lembre-se de ajustar as opções de acordo com suas necessidades e objetivos de análise.
<br>
<br>
<br>
                                                    
## usando o scan.py:


scan.py arquivo_salvo.txt
