import { Container, Nav, Spinner } from "react-bootstrap";
import User, { UserProp } from "../interfaces/User";
import SideBar from "../components/SideBar";
import AccountForm from "../components/AccountForm";
import { Link, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import CenteredSpinner from "../components/CenteredSpinner";

interface customUserProp {
    currentUser: UserProp["user"]
}

function Account({ currentUser }: customUserProp) {
    const mode = useParams<{ mode?: string | undefined }>().mode;
    const [user, setUser] = useState<User | undefined>(undefined);
    const [formElement, setFormElement] = useState<JSX.Element | undefined>(undefined);

    useEffect(() => {
        if (mode === undefined) setUser(currentUser? currentUser : undefined);
        else if (mode === "mod") setUser({
            "id": -1,
            "name": "NEW",
            "webhook": "",
            "headers": {}
        } as unknown as User);
    }, [mode, currentUser]);


    if (!user) return (<CenteredSpinner animation="border" />);
    
    return (
        <SideBar sideElement={<AccountForm user={user} editName={mode === "mod"} key={user.id}/>}>
            <Nav className="flex-column" variant="tabs" defaultActiveKey="/account">
                <Nav.Link as={Link} to="/account" className="rounded-0">My account</Nav.Link>
                <Nav.Link as={Link} to="/account/mod" className="rounded-0">Add account</Nav.Link>
            </Nav>
        </SideBar>
    );
}

export default Account;