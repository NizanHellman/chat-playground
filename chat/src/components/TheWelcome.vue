<script lang="ts">
import { defineComponent, ref } from "vue";
import { useUserStore } from "@/stores/user";

export default defineComponent({

  setup() {
    const user = useUserStore()

    const userName = ref('')

    function onSubmit(e: any) {
      e.preventDefault()
      console.log(e)
      if (!userName.value) return
      user.addUser(userName.value)
      userName.value
      //   TODO: data = {"username": current_user}; $.postJSON('/api/register', JSON.stringify(data), function(response)
      //   TODO: notify Pinia, Pinia need to open the websocket
    }

    return {
      onSubmit,
      userName
    }
  }
})
</script>

<template>
  <div class="chat-body card">
    <div class="card-body">
      <form @submit.prevent="onSubmit" class="form-inline" id="user-form">
        <div class="row">
            <input type="text" class="form-control" id="user_input" v-model="userName" placeholder="Enter your name">
            <button id="start" type="submit" class="btn btn-primary">Start</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style>
  .card {
  }
  #user-form {
  }
  #user-form input {
    width: 400px;
    padding-right: 30%;
  }
  #user-form button {
  }
</style>