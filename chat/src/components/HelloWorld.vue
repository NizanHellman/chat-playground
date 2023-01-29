<script lang="ts">
import { defineComponent, ref } from 'vue'

import { useCartStore } from '@/stores/counter'
import { useUserStore } from "@/stores/user";

export default defineComponent({

  setup() {
    const cart = useCartStore()
    const user = useUserStore()

    const itemName = ref('')

    function addItemToCart() {
      if (!itemName.value) return
      cart.addItem(itemName.value)
      itemName.value = ''
    }

    async function buy() {
      const n = await cart.purchaseItems()

      console.log(`Bought ${n} items`)

      cart.rawItems = []
    }

    return {
      itemName,
      addItemToCart,
      cart,
      buy,
      user
    }

  }
})



</script>

<template>
  <div class="chat-body card">
    <div class="card-body">
      <strong id="profile">{{ user.name }}</strong>
      <h4 class="card-title text-center"> Chat App </h4>
      <hr>
      <div id="messages">
          <ul data-testid="items">
            <p v-for="item in cart.items" :key="item.name">
              <strong>{{ item.name }}: </strong>
              <span>{{ item.message }}</span>
            </p>
          </ul>
      </div>
      <form @submit.prevent="addItemToCart" data-testid="add-items" id="chat-form" class="form-inline">
        <input type="text" class="form-control" v-model="itemName" placeholder="Write your message" />
        <button id="send" class="btn btn-primary">Add</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.card {
  /*position: absolute;*/
  /*width: 95%;*/
  /*height: 80%;*/
  /*box-shadow: 0 0 5px gray;*/
  /*left: 2.5%;*/
  /*top: 5%;*/
}
#chat-form {
}
#messages {
  /*padding-bottom: 10%;*/
  /*padding-left: 20px;*/
  /*padding-top: 20px;*/
  /*max-height: 80%;*/
  /*overflow: auto;*/
  min-height: 500px;
  box-shadow: 0 0 5px gray;;
}
#chat-form input {
  /*width: 400px;*/
  /*padding-right: 20%;*/
}
#chat-form button {
  /*position: absolute;*/
  /*left: 85%;*/
}
#profile {
  /*position: absolute;*/
  /*top: 20px;*/
  /*left: 20px;*/
}
</style>
