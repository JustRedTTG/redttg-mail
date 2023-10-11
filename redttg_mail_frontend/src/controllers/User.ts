import { API } from "../config";
import User from "../interfaces/User";

export const getUser = async (id?: number): Promise<User> => {
    if (!id) {
        return fetch(`${API}/auth`, {credentials: 'include'}).then(async (response) => {
            if (!response.ok) throw new Error('User not logged in');
            return getUser(await response.text().then((id) => parseInt(id)));
        }).catch((error) => {
            console.error(error);
            throw new Error('Failed to fetch authenticated user id');
        });
    }
    return fetch(`${API}/auth/info/${id}`, {credentials: 'include'}).then((response) => {
        if (!response.ok) throw new Error('Failed to fetch user');
        return response.json() as unknown as User;
    }).catch((error) => {
        console.error(error);
        throw new Error('Failed to fetch user');
    });
}