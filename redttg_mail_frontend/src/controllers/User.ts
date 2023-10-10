import { API } from "../config";
import User from "../interfaces/User";

export const getUser = async (): Promise<User> => {
    return fetch(`${API}/auth/info`, {credentials: 'include'}).then((response) => {
        if (!response.ok) throw new Error('Failed to fetch user');
        return response.json() as unknown as User;
    }).catch((error) => {
        console.error(error);
        throw new Error('Failed to fetch user');
    });
}