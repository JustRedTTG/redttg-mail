import { Button, Container, Form } from "react-bootstrap";
import User from "../interfaces/User";
import { Editor } from "react-draft-wysiwyg";
import "react-draft-wysiwyg/dist/react-draft-wysiwyg.css";
import HeadersInput from "./HeadersInput";
import { useRef } from "react";
import { API } from "../config";

interface AccountFormProps {
    user: User
    method?: string;
    editName?: boolean;
}

function AccountForm({ user, method, editName }: AccountFormProps) {
    const headersInputRef = useRef<HTMLInputElement>(null);

    return (
        <Container>
            <Form>
                <Form.Group className="mb-2">
                    <h1 className="border-bottom-1 mb-1">Account Settings for{" "}
                        {user.name}@redttg.com</h1>
                    {editName && <>
                        <Form.Label>Name:</Form.Label>
                        <Form.Control type="text" defaultValue={user.name} name="name" />
                    </>}
                    <Form.Control type="hidden" defaultValue={user.id} name="id" />
                </Form.Group>
                <Form.Group className="mb-2">
                    <Form.Label>Email Webhook:</Form.Label>
                    <Form.Control type="url" defaultValue={user.webhook} name="webhook" />
                </Form.Group>
                <Form.Group className="mb-2">
                    <Form.Control ref={headersInputRef} type="hidden" required defaultValue={JSON.stringify(user.headers)} name="headers" />
                    <Form.Label>Headers:</Form.Label>
                    <HeadersInput headersInputRef={headersInputRef} />
                </Form.Group>

                <Button variant="primary" type="submit" onClick={ (e) => {
                    if (headersInputRef.current === null) return;
                    if (headersInputRef.current.value === "") e.preventDefault();
                }}>
                    Submit
                </Button>
            </Form>
        </Container>
    );
}

export default AccountForm;