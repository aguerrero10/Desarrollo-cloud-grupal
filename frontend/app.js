const routes=[
    {path:'/',component:usuario},
    {path:'/usuario',component:usuario},
    {path:'/tarea',component:tarea}
]


const router = VueRouter.createRouter({
    history: VueRouter.createWebHashHistory(),
    routes, 
})

const app = Vue.createApp({})
app.use(router)
app.mount('#app')

