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
    // Em caso de erro, tentar novamente após alguns segundos
    setTimeout(connectToPythonSocket, 1000);
  };

  pythonSocket.onclose = function () {
    console.log("Conexão com o servidor Python fechada.");
    // Lidar com a desconexão, se necessário.
  };
}

// Função para enviar dados pelo WebSocket
function sendData(data) {
  connectToPythonSocket();

  if (pythonSocket.readyState === WebSocket.OPEN) {
    pythonSocket.send(JSON.stringify(data));
  } else {
    // Caso o WebSocket não esteja aberto, tentar novamente após alguns segundos
    setTimeout(function () {
      if (pythonSocket.readyState === WebSocket.OPEN) {
        pythonSocket.send(JSON.stringify(data));
      }
    }, 5000); // Tentar novamente após 5 segundos
  }
}

// Função para capturar e enviar requisições e respostas ao servidor
function capturarDados(details, type) {
  const requestUrl = details.url;
  const requestType = details.method; // Obtém o tipo da requisição (GET, POST, etc.)

  // Verifica a url e se o tipo da requisição é diferente de "OPTIONS"
  if (requestType !== "OPTIONS" && requestUrl.indexOf("ws://127.0.0.1:8888") === -1) {
    // Envia os dados e o tipo para o servidor através do WebSocket
    const data = {
      type: type,
      url: requestUrl,
      requestType: requestType,
      headers: type === "REQUEST" ? details.requestHeaders : details.responseHeaders,
    };
    sendData(data);
  }
}

// Adiciona um ouvinte para capturar todas as requisições e seus cabeçalhos
chrome.webRequest.onBeforeSendHeaders.addListener(
  (details) => capturarDados(details, "REQUEST"),
  { urls: ["<all_urls>"] }, // Intercepta todas as URLs
  ["requestHeaders"] // Especifica que queremos os cabeçalhos das requisições disponíveis na função de callback
);

// Adiciona um ouvinte para capturar todas as respostas e seus cabeçalhos
chrome.webRequest.onHeadersReceived.addListener(
  (details) => capturarDados(details, "RESPONSE"),
  { urls: ["<all_urls>"] }, // Intercepta todas as URLs
  ["responseHeaders"] // Especifica que queremos os cabeçalhos das respostas disponíveis na função de callback
);
