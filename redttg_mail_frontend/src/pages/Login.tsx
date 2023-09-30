import { Button, Card, Container, Form } from "react-bootstrap";

function Login() {
    return (
        <Container className="d-flex align-items-center justify-content-center h-100">
            <Card className="w-50">
                <Card.Header>
                    <Card.Title>Login</Card.Title>
                </Card.Header>
                <Card.Body>
                    <Form action="/api/auth/login/" method="POST">
                        <Form.Group className="mb-3" controlId="formBasicEmail">
                            <Form.Label>Email address</Form.Label>
                            <Form.Control type="email" placeholder="Enter email" />
                        </Form.Group>

                        <Form.Group className="mb-3" controlId="formBasicPassword">
                            <Form.Label>Password</Form.Label>
                            <Form.Control type="password" placeholder="Password" />
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