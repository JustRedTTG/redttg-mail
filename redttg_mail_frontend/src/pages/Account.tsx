import { Container, Nav, Spinner } from "react-bootstrap";
import { UserProp } from "../interfaces/User";
import SideBar from "../components/SideBar";
import AccountForm from "../components/AccountForm";

function Account({ user }: UserProp) {

    if (!user) return (<Container><Spinner animation="grow" variant="info" /></Container>);
    return (
        <SideBar sideElement={<AccountForm user={user} />}>
            <Nav className="flex-column" variant="tabs" defaultActiveKey="/account">
                <Nav.Link to="/account" className="rounded-0">My account</Nav.Link>
            </Nav>
        </SideBar>
    );
}

export default Account;