const WEBSOCKET_PORT = 4032

const socket = new WebSocket(`ws://localhost:${WEBSOCKET_PORT}`)
socket.onopen = () => {
  console.log('Socket was open')
}
socket.onmessage = event => {
  console.dir(event)
}
