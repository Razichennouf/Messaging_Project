function deleteMessage(messageId) {
  fetch("/delete-message", {
    method: "POST",
    body: JSON.stringify({ messageId: messageId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
