import axios from 'axios'

import { defineStore, acceptHMRUpdate } from 'pinia'
import { useCartStore } from "@/stores/counter";

/**
 * Simulate a login
 */
// function apiLogin(a: string, p: string) {
//     if (a === 'ed' && p === 'ed') return Promise.resolve({ isAdmin: true })
//     if (p === 'ed') return Promise.resolve({ isAdmin: false })
//     return Promise.reject(new Error('invalid credentials'))
// }

function postJSON(url: string, data: object) {
    return axios.post(url, data, {
        headers: { 'Content-Type': 'application/json' }
    })
}

export const useUserStore = defineStore({
    id: 'user',
    state: () => ({
        name: 'Eduardo',
        isAdmin: true,
    }),

    actions: {
        async addUser(user: string) {
            debugger;
            this.$patch({
                name: user
            })
            const data = {'username': user}
            try {
                const response = await postJSON('http://localhost:8000/api/register', data)
            } catch (error) {
                console.log('Error registering user:', error)
            }
            const cart = useCartStore()
            await cart.connect(user)
        },
        logout() {
            this.$patch({
                name: '',
                isAdmin: false,
            })

            // we could do other stuff like redirecting the user
        }
    }
})

if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useUserStore, import.meta.hot))
}
