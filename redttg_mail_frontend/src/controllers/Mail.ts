import { API } from "../config";
import { Mail, MailPreview } from "../interfaces/Mail";

export const getMails = async (): Promise<MailPreview[]> => {
    return fetch(`${API}/mail/fetch`, {credentials: 'include'}).then((response) => {
        if (!response.ok) throw new Error('Failed to fetch mails');
        return response.json() as unknown as MailPreview[];
    }).catch((error) => {
        console.error(error);
        throw new Error('Failed to fetch mails');
    });
}
export const getMail = async (id: number): Promise<Mail> => {
    return fetch(`${API}/mail/fetch/${id}`, {credentials: 'include'}).then((response) => {
        if (!response.ok) throw new Error('Failed to fetch mails');
        return response.json() as unknown as Mail;
    }).catch((error) => {
        console.error(error);
        throw new Error('Failed to fetch mails');
    });
}