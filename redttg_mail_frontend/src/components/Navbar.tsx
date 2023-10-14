import { Navbar, Spinner } from "react-bootstrap";
import { UserProp } from "../interfaces/User";
import { Link } from "react-router-dom";

interface NavBarProps extends UserProp {
    className?: string;
}

function NavBar({ user, className }: NavBarProps) {
    return (
        <Navbar className={`border-bottom-2 ${className ? className : ""}`}>
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
                {!user &&
                    <Navbar.Text>
                        <Link to="/login">Login</Link>
                    </Navbar.Text>
                }
            </Navbar.Collapse>
        </Navbar>
    );
}

export default NavBar;