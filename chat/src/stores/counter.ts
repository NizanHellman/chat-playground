import { defineStore, acceptHMRUpdate } from 'pinia'
import { useUserStore } from './user'

export class MessageObj {
  public name: string = '';
  public message: string = '';
}

export const useCartStore = defineStore({
  id: 'cart',
  state: () => ({
    rawItems: [] as MessageObj[],
    socket: <WebSocket> <unknown> null
  }),
  getters: {
    items: (state): Array<{ name: string; message: string }> =>

        state.rawItems.reduce((items, item) => {
          items.push(item)

          return items
        }, [] as Array<{ name: string; message: string }>),
  },
  actions: {
    addItem(message: string) {
      let item: MessageObj = new MessageObj();
      item.message = message
      const user = useUserStore()
      item.name = user.name
      this.socket.send(JSON.stringify({'sender': item.name, 'message': item.message}));
      // this.rawItems.push(item)
    },

    async purchaseItems() {

      console.log('Purchasing', this.items)
      const n = this.items.length
      this.rawItems = []

      return n
    },

    async connect(user: string) {
      debugger;
      this.socket = new WebSocket(`ws://127.0.0.1:8000/api/chat?user=${user}`);
      this.socket.onmessage = (event) => {
        let data = JSON.parse(event.data)
        let item: MessageObj = new MessageObj();
        item.message = data['message']
        item.name = data['sender']
        this.rawItems.push(item)
      };
    }
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useCartStore, import.meta.hot))
}
