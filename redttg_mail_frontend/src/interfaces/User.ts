interface User {
    id: number;
    name: string;
    date_joined: Date;
    webhook: string;
    headers: object;

    is_staff: boolean;
    is_superuser: boolean;
}

export interface UserProp {
    user: User | undefined | null
}

export default User