import { Container, Nav, Spinner } from "react-bootstrap";
import { UserProp } from "../interfaces/User";
import SideBar from "../components/SideBar";
import AccountForm from "../components/AccountForm";
import { Link } from "react-router-dom";

function Account({ user }: UserProp) {

    if (!user) return (<Container><Spinner animation="grow" variant="info" /></Container>);
    return (
        <SideBar sideElement={<AccountForm user={user} />}>
            <Nav className="flex-column" variant="tabs" defaultActiveKey="/account">
                <Nav.Link as={Link} to="/account" className="rounded-0">My account</Nav.Link>
                <Nav.Link as={Link} to="/account/mod" className="rounded-0">Add account</Nav.Link>
            </Nav>
        </SideBar>
    );
}

export default Account;