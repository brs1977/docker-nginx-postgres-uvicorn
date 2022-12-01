export type User = {
    id: number,
    name: string,
}
export type Users = Array<User>

export interface API {
    users():Promise<Users>
}