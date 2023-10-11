import { Container, Form } from "react-bootstrap";
import User from "../interfaces/User";

interface AccountFormProps {
    user: User
    method?: string;
    editName?: boolean;
}

function AccountForm({ user, method, editName }: AccountFormProps) {
    return (
        <Container>
            <Form>
                <Form.Group>
                    <h1 className="border-bottom-1 mb-1">Account Settings for{" "}
                        {user.name}@redttg.com</h1>
                    {editName && <>
                        <Form.Label>Name:</Form.Label>
                        <Form.Control type="text" defaultValue={user.name} name="name" />
                    </>}
                </Form.Group>
            </Form>
        </Container>
    );
}

export default AccountForm;