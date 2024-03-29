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

const PACKETS_SCHEMA = Object.freeze({
  ether: {
    image: 'ethernet.png',
    color: '#91291c',
  },
  ip: {
    image: 'ip.png',
    color: '#914f1c',
  },
  tcp: {
    image: 'tcp.png',
    color: '#8c6a1b',
  },
  udp: {
    image: 'udp',
    color: '#878518',
  },
  icmp: {
    image: 'icmp.png',
    color: '#6d8f1d',
  },
  dns: {
    image: 'dns.png',
    color: '#3a8a1a',
  },
  raw: {
    image: 'raw.png',
    color: '#1a8a68',
  },
  arp: {
    image: 'arp.png',
    color: '#185d85',
  },
  dhcp: {
    image: 'dhcp.png',
    color: '#451885',
  },
  default: {
    image: 'packet-icon.png',
    color: 'grey',
  }
})

const makeTogglable = (parent, container, opened = false) => {
  parent.onclick = event => {
    event.stopPropagation()
    for (let i = 0; i < container.children.length; i++) {
      const child = container.children[i]
      child.style.display = opened 
        ? 'none'
        : 'block'
    }
    opened = !opened
  }
}

// class that will be used
// for DOM elements creation
class Creator {
  createPacketElement = packet => {
    console.dir(packet)

    const container = document.createElement('div')
    container.classList.add('packet')
    
    const header = this.createPacketHeader(packet)
    container.appendChild(header)

    const layersContainer = document.createElement('div')
    layersContainer.classList.add('packet-layers')
    makeTogglable(header, layersContainer)
    container.appendChild(layersContainer)

    const layers = Object.entries(packet.layers)
    for (const [layer, fields] of layers) {
      const layerElement = this.createLayer(layer, fields)
      layerElement.style.display = 'none'
      layersContainer.appendChild(layerElement)
    }

    return container
  }

  createLayer = (layer, fieldsObject) => {
    const container = document.createElement('div')
    container.classList.add('packet-layer')
    
    const title = document.createElement('h4')
    title.classList.add('packet-layer-title')
    title.textContent = layer
    container.appendChild(title)

    const fieldsContainer = document.createElement('div')
    fieldsContainer.classList.add('packet-fields')
    makeTogglable(title, fieldsContainer)
    container.appendChild(fieldsContainer)

    const fields = Object.entries(fieldsObject)
    for (const [key, value] of fields) {
      const wrapper = document.createElement('div')
      wrapper.style.width = '100%'
      wrapper.style.display = 'none'
      fieldsContainer.appendChild(wrapper)

      const field = document.createElement('div')
      field.classList.add('packet-field')
      wrapper.appendChild(field)

      const keyElement = document.createElement('p')
      keyElement.textContent = key
      field.appendChild(keyElement)

      const valueElement = document.createElement('p')
      valueElement.textContent = value
      field.appendChild(valueElement)
    }
    
    return container
  }

  createPacketHeader = packet => {
    const packetTitle = packet.packet_title
    const packetSize = packet.packet_size

    const header = document.createElement('div')
    header.classList.add('packet-header')

    let { image, color } = (() => {
      const key = packetTitle.toLowerCase()
      if (key in PACKETS_SCHEMA) {
        return PACKETS_SCHEMA[key]
      }
      return PACKETS_SCHEMA.default
    })()

    const icon = document.createElement('img')
    icon.classList.add('packet-icon')
    icon.src = `/icons/${image}`
    header.appendChild(icon)

    const title = document.createElement('h3')
    title.classList.add('packet-title')
    title.textContent = packetTitle
    title.style.color = color
    header.appendChild(title)

    const size = document.createElement('p')
    size.classList.add('packet-size')
    size.textContent = packetSize
    header.appendChild(size)

    return header
  }
}

// singleton with logic
export default new class Logic {
  constructor() {
    this.creator = new Creator()
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
    const element = this.creator.createPacketElement(packet)
    this.layout.packetsList.appendChild(element)
  }
}
