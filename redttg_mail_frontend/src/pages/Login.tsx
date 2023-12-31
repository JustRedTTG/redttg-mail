import { Button, Card, Container, Form } from "react-bootstrap";
import { API } from "../config";

function Login() {
    return (
        <Container className="d-flex align-items-center justify-content-center h-100">
            <Card className="w-50">
                <Card.Header>
                    <Card.Title>Login</Card.Title>
                </Card.Header>
                <Card.Body>
                    <Form action={`${API}/auth/login/`} method="POST">
                        <Form.Group className="mb-3" controlId="formBasicEmail">
                            <Form.Label>Email address</Form.Label>
                            <Form.Control type="email" placeholder="mail@redttg.com" name="username" />
                        </Form.Group>

                        <Form.Group className="mb-3" controlId="formBasicPassword">
                            <Form.Label>Password</Form.Label>
                            <Form.Control type="password" placeholder="Password" name="password"/>
                        </Form.Group>
                        <div className="d-flex justify-content-end">
                        <Button variant="primary" type="submit">
                            Login
                        </Button>
                        </div>
                    </Form>
                </Card.Body>
            </Card>
        </Container>
    );
}

export default Login;