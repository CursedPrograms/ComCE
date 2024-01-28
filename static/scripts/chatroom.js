var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('message', function(data) {
    var messageDiv = document.createElement('div');
    messageDiv.innerHTML = '<strong>' + data.nickname + ':</strong> ' + data.content;
    document.getElementById('messages').appendChild(messageDiv);
    scrollToBottom();
});

function sendMessage() {
    var messageContent = document.getElementById('message').value;
    socket.emit('message', { content: messageContent });
    document.getElementById('message').value = '';
    scrollToBottom();
}

function scrollToBottom() {
  var messagesContainer = document.getElementById('messages');
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}