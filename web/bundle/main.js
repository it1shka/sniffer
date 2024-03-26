/*
 * Using something like React
 * is definitely an overkill here,
 * so I prefer plain simple JavaScript
 * language without any add-ons
 */

const getLayout = () => {
  const schema = {
    startButton:   '#btn-start',
    stopButton:    '#btn-stop',
    toggleButton:  '#btn-toggle',
    clearButton:   '#btn-clear',
    controlStatus: '.control-status',
    packetsList:   '.packets-list',
  }
  const mapped = Object.entries(schema).map(([key, selector]) => {
    const maybeElement = document.querySelector(selector)
    if (!maybeElement) {
      throw new Error(`Failed to find element "${selector}"`)
    }
    return [key, maybeElement]
  })
  return Object.fromEntries(mapped)
}

const useRemoteConnection = handler => {
  const WEBSOCKET_PORT = 4032
  const RECONNECTION_TIME = 3000

  let socket
  const connect = () => {
    socket = new WebSocket(`ws://localhost:${WEBSOCKET_PORT}`)
    socket.onopen = () => {
      console.log('Connection established')
    }
    socket.onclose = () => {
      console.log('Connection lost. Trying to re-establish...')
      setTimeout(connect, RECONNECTION_TIME)
    }
    socket.onmessage = event => {
      try {
        const data = JSON.parse(event.data)
        handler(data)
      } catch (error) {
        console.error(error)
      }
    }
  }
  connect()
}

export default new class Logic {
  constructor() {
    this.sniffing = false
    this.bindLayout()
    useRemoteConnection(this.handlePacket)
  }

  bindLayout = () => {
    this.layout = getLayout()
    this.layout.startButton.onclick = this.startSniffing
    this.layout.stopButton.onclick = this.stopSniffing
    this.layout.toggleButton.onclick = this.toggleSniffing
    this.layout.clearButton.onclick = this.clearPackets
  }

  startSniffing = () => {
    this.sniffing = true
    this.layout.controlStatus.textContent = 'On'
  }

  stopSniffing = () => {
    this.sniffing = false
    this.layout.controlStatus.textContent = 'Off'
  }

  toggleSniffing = () => {
    if (this.sniffing) {
      this.stopSniffing()
      return
    }
    this.startSniffing()
  }

  clearPackets = () => {
    let firstChild
    while (firstChild = this.layout.packetsList.firstChild) {
      this.layout.packetsList.removeChild(firstChild)
    }
  }

  handlePacket = packet => {
    if (!this.sniffing) return
    const packetElement = this.constructPacketElement(packet)
    this.layout.packetsList.appendChild(packetElement)
  }

  constructPacketElement = packet => {
    const container = document.createElement('div')
    container.classList.add('packet')
    const title = document.createElement('h3')
    title.textContent = packet.packet_title
    container.appendChild(title)
    return container
  }
}
