import { PageView } from './page/PageView'
import { PageViewModel } from './page/PageViewModel'
import { getURL, ServerAPI } from './page/ServerAPI'
import { PageModelAPI } from './page/PageModelAPI'
import './style.css'

// import { get_url, server_api } from './api/server_api'
// import { app } from './common/app'
//import { toast } from './ctrls/toast'



const root = document.querySelector<HTMLDivElement>('#app')!
//const api = server_api('http://129.200.0.116:8010')
// const api = server_api('http://129.200.0.116:8015/api/v1')
//const api = server_api(get_url('api/v1',8020))
//app({api,root})

const api = new ServerAPI(getURL('api/v1',8020))
const model = new PageModelAPI(api)
const viewModel = new PageViewModel(model)
const view = new PageView(viewModel)
root.appendChild(view.root)

