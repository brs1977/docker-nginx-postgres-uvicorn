import { WorkspaceProps } from "../PageTypes";
import { ViewModel } from "../ViewModel"

export class WorkspaceViewModel<T extends WorkspaceProps> extends ViewModel<T> {
    get kod() { return this.getProp('kod') }
    get pic() { return this.getProp('pic') }
}