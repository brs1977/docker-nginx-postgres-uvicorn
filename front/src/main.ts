import './style.css'
import { server_api } from './api/server_api'
import { app } from './common/app'
//import { toast } from './ctrls/toast'



const root = document.querySelector<HTMLDivElement>('#app')!
const api = server_api('http://129.200.0.116:8010')
app({api,root})


