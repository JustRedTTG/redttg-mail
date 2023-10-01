import { Mail, MailPreview } from "../interfaces/Mail";

export const getMails = async (): Promise<MailPreview[]> => {
    return fetch('/api/mail/fetch', {credentials: 'include'}).then((response) => {
        return response.json() as unknown as MailPreview[];
    }).catch((error) => {
        console.error(error);
        throw new Error('Failed to fetch mails');
    });
}
export const getMail = async (id: number): Promise<Mail> => {
    return fetch(`/api/mail/fetch/${id}`, {credentials: 'include'}).then((response) => {
        return response.json() as unknown as Mail;
    }).catch((error) => {
        console.error(error);
        throw new Error('Failed to fetch mails');
    });
}