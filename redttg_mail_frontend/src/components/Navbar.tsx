import { Navbar, Spinner } from "react-bootstrap";
import User, { UserProp } from "../interfaces/User";
import { Link } from "react-router-dom";

function NavBar({ user }: UserProp) {
    return (
        <Navbar className="border-bottom-2">
            <Navbar.Brand as={Link} to="/">Redttg Mail</Navbar.Brand>

            <Navbar.Collapse className="justify-content-end">
                {user &&
                    <Navbar.Text>
                        Signed in as: <Link to="/account">{user.name}@redttg.com</Link>
                    </Navbar.Text>
                }
                {user === undefined && 
                    <Spinner animation="grow" variant="info"/>
                }
            </Navbar.Collapse>
        </Navbar>
    );
}

export default NavBar;