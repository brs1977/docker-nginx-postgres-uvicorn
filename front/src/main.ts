import './style.css'
import { get_url, server_api } from './api/server_api'
import { app } from './common/app'
//import { toast } from './ctrls/toast'



const root = document.querySelector<HTMLDivElement>('#app')!
//const api = server_api('http://129.200.0.116:8010')
const api = server_api('http://129.200.0.116:8015/api/v1')
//const api = server_api(get_url('api/v1',8020))
app({api,root})