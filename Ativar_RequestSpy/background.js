// Variável global para armazenar o WebSocket
let pythonSocket;

// Função para conectar ao WebSocket Python
function connectToPythonSocket() {
  if (pythonSocket && pythonSocket.readyState === WebSocket.OPEN) {
    // Se o WebSocket já estiver aberto, não é necessário fazer nada
    return;
  }

  pythonSocket = new WebSocket("ws://127.0.0.1:8888");

  pythonSocket.onopen = function (event) {
    console.log("Conexão com o servidor Python estabelecida.");
  };

  pythonSocket.onerror = function (error) {
    console.error("Erro na conexão com o servidor Python:", error);
    // Em caso de erro, tente novamente
    setTimeout(connectToPythonSocket, 1000);
  };

  pythonSocket.onclose = function () {
    console.log("Conexão com o servidor Python fechada.");
    // Lidar com a desconexão, se necessário.
  };
}

// Função para capturar e enviar requisições ao servidor
function capturarRequisicoes(details) {
  const requestUrl = details.url;
  const requestType = details.method; // Obtém o tipo da requisição (GET, POST, etc.)

  // Verifica a url e se o tipo da requisição é diferente de "OPTIONS"
  if (requestType !== "OPTIONS" && requestUrl.indexOf("ws://127.0.0.1:8888") === -1) {
    // Envia a requisição e o tipo para o servidor através do WebSocket
    connectToPythonSocket();
    if (pythonSocket.readyState === WebSocket.OPEN) {
      const requestData = {
        type: requestType,
        url: requestUrl,
        headers: details.requestHeaders, // Inclui o cabeçalho completo na mensagem
      };
      pythonSocket.send(JSON.stringify(requestData));
    } else {
      // Caso o WebSocket não esteja aberto, tenta novamente em alguns segundos
      setTimeout(function () {
        if (pythonSocket.readyState === WebSocket.OPEN) {
          const requestData = {
            type: requestType,
            url: requestUrl,
            headers: details.requestHeaders, // Inclui o cabeçalho completo na mensagem
          };
          pythonSocket.send(JSON.stringify(requestData));
        }
      }, 5000); // Tentar novamente após 5 segundos
    }
  }
}

// Adiciona um ouvinte para capturar todas as requisições e seus cabeçalhos
chrome.webRequest.onBeforeSendHeaders.addListener(
  capturarRequisicoes,
  { urls: ["<all_urls>"] }, // Intercepta todas as URLs
  ["requestHeaders"] // Especifica que queremos os cabeçalhos das requisições disponíveis na função de callback
);
