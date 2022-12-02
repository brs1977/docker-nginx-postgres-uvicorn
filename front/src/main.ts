import './style.css'
import { server_api } from './api/server_api'
import { app } from './common/app'
//import { toast } from './ctrls/toast'



const root = document.querySelector<HTMLDivElement>('#app')!
const api = server_api('api/v1',8015)
app({api,root})


