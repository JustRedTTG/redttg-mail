export type Headers = { [key: string]: string };

interface User {
    id: number;
    name: string;
    date_joined?: Date;
    webhook: string;
    body: string;
    headers: Headers;

    is_staff?: boolean;
    is_superuser?: boolean;
}

export interface UserProp {
    user: User | undefined | null
}

export default User