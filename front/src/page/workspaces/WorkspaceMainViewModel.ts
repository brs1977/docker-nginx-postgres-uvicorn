import { WorkspaceMainProps } from "../PageTypes";
import { WorkspaceViewModel } from "./WorkspaceViewModel";

export class WorkspaceMainViewModel extends WorkspaceViewModel<WorkspaceMainProps> {
    get title() { return this.getProp('title') }
    get picpic() { return this.getProp('picpic') }
    get n_par() { return this.getProp('n_par') ?? []}
    get m_par() { return this.getProp('m_par') ?? []}
}