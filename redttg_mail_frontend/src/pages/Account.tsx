import { Container, Spinner } from "react-bootstrap";
import { UserProp } from "../interfaces/User";

function Account({user}: UserProp) {

    if (!user) return (<Container><Spinner animation="grow" variant="info"/></Container>);
    return (
        <Container>
            <h1 className="border-bottom-1 mb-1">Account Settings for {user.name}@redttg.com</h1>

        </Container>
    );
}

export default Account;