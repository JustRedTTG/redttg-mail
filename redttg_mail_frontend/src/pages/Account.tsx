import { Nav } from "react-bootstrap";
import User, { UserProp } from "../interfaces/User";
import SideBar from "../components/SideBar";
import AccountForm from "../components/AccountForm";
import { Link, useNavigate, useParams } from "react-router-dom";
import { useCallback, useEffect, useState } from "react";
import CenteredSpinner from "../components/CenteredSpinner";
import { getUser, getUsers } from "../controllers/User";

interface customUserProp {
    currentUser: UserProp["user"]
    onUpdate: (user: User) => void;
}

function Account({ currentUser, onUpdate }: customUserProp) {
    const mode = useParams<{ mode?: string | undefined }>().mode;
    const [user, setUser] = useState<User | undefined>(undefined);
    const [users, setUsers] = useState<User[]>([]);
    const navigate = useNavigate();
    const setUserFromId = useCallback(() => {
        if (mode === undefined) return;
        const id = parseInt(mode);
        if (id === undefined) return;
        if (users.length === 0) return;
        const existing_user = users.find((u) => u.id === id && u.date_joined !== undefined);
        if (existing_user) {
            setUser(existing_user);
            return;
        }
        getUser(id).then((user) => {
            setUsers(users.map(u => u.id === id ? user : u));
            setUser(user);
        }).catch(() => {
            navigate('/account', { replace: true });
        });
    }, [mode, users, navigate]);

    useEffect(() => {
        if (currentUser === null) navigate('/login', { replace: true });
        if (!currentUser?.is_superuser) return;
        getUsers().then(setUsers);
    }, [currentUser, navigate]);

    useEffect(() => {
        if (mode === undefined) setUser(currentUser ? currentUser : undefined);
        else if (mode === "mod") setUser({
            "id": -1,
            "name": "",
            "webhook": "",
            "headers": {}
        } as unknown as User);
        else setUserFromId()
    }, [mode, currentUser, setUserFromId]);

    useEffect(() => {
        if (user === undefined) setUserFromId();
    }, [users, user, setUserFromId]);

    if (!user) return (<CenteredSpinner animation="border" />);

    const form = (<AccountForm
        user={user}
        editName={mode === "mod"}
        key={user.id}
        onUpdate={(user) => {
            setUser(user);
            if (user.id === currentUser?.id) onUpdate(user);
            else {
                setUsers(users.map(u => u.id === user.id ? user : u));
                if (mode === "mod") navigate(`/account/${user.id}`)
            }
        }}
        onDelete={(id) => {
            setUsers(users.filter(u => u.id !== id));
            if (id === currentUser?.id) navigate('/login', { replace: true });
            else navigate('/account', { replace: true });
        }}
    />)

    if (!currentUser?.is_superuser) return form;

    return (
        <SideBar sideElement={form}>
            <Nav className="flex-column" variant="tabs" defaultActiveKey="/account">
                <Nav.Link as={Link} to="/account" className="rounded-0">My account</Nav.Link>
                {users.map((user) => (
                    user.id !== currentUser?.id && <Nav.Link as={Link} to={`/account/${user.id}`} className="rounded-0" key={user.id}>{user.name}</Nav.Link>
                ))}
                <Nav.Link as={Link} to="/account/mod" className="rounded-0">Add account</Nav.Link>
            </Nav>
        </SideBar>
    );
}

export default Account;