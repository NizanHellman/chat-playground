<template>
  <div>
    <div v-for="message in messages" :key="message.id">
      {{ message.text }}
    </div>
    <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="Type your message here...">
  </div>
</template>

<script>
export default {
  data() {
    return {
      messages: [],
      newMessage: ''
    }
  },
  methods: {
    sendMessage() {
      if (!this.newMessage) {
        return
      }
      this.messages.push({
        id: Date.now(),
        text: this.newMessage
      })
      this.newMessage = ''
    }
  }
}
</script>


