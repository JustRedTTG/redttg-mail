import { Button, Container, Form, Spinner } from "react-bootstrap";
import User from "../interfaces/User";
// import { Editor } from "react-draft-wysiwyg";
import "react-draft-wysiwyg/dist/react-draft-wysiwyg.css";
import HeadersInput from "./HeadersInput";
import { useRef, useState } from "react";
import { deleteUser, updateUser } from "../controllers/User";

interface AccountFormProps {
    user: User
    editName?: boolean;
    onUpdate?: (user: User) => void;
    onDelete?: (id: number) => void;
}

interface formProps {
    id: HTMLInputElement,
    name: HTMLInputElement,
    webhook: HTMLInputElement,
    body: HTMLInputElement,
    headers: HTMLInputElement
}

function AccountForm({ user, editName, onUpdate, onDelete }: AccountFormProps) {
    const headersInputRef = useRef<HTMLInputElement>(null);
    const [submitting, setSubmitting] = useState<boolean>(false);

    return (
        <Container>
            <Form onSubmit={(e) => {
                e.preventDefault();
                const { id, name, webhook, body, headers }: formProps = e.target as unknown as formProps;
                const finalUser: User = {
                    id: parseInt(id.value),
                    name: name.value ? name.value : user.name,
                    webhook: webhook.value,
                    body: body.value,
                    headers: JSON.parse(headers.value)
                };
                setSubmitting(true);
                updateUser(finalUser).then((user) => {
                    setSubmitting(false);
                    if (onUpdate) {
                        onUpdate(user);
                    }
                });
            }}>
                <Form.Group className="mb-2">
                    <h1 className="border-bottom-1 mb-1">Account Settings for{" "}
                        {user.name}@redttg.com</h1>
                    {editName && <>
                        <Form.Label>Name:</Form.Label>
                        <Form.Control type="text" defaultValue={user.name} name="name" required />
                    </>}
                    {user.id > -1 &&
                        <Form.Control type="hidden" defaultValue={user.id} name="id" />
                    }
                </Form.Group>
                <Form.Group className="mb-2">
                    <Form.Label>Email Webhook:</Form.Label>
                    <Form.Control type="url" defaultValue={user.webhook} name="webhook" />
                </Form.Group>
                <Form.Group className="mb-2">
                    <Form.Label>Webhook Body:</Form.Label>
                    <Form.Control as="textarea" defaultValue={user.body} name="body" style={{minHeight: "200px"}}/>
                </Form.Group>
                <Form.Group className="mb-2">
                    <Form.Control ref={headersInputRef} type="hidden" required defaultValue={JSON.stringify(user.headers)} name="headers" />
                    <Form.Label>Webhook Headers:</Form.Label>
                    <HeadersInput headersInputRef={headersInputRef} />
                </Form.Group>

                <Button
                    variant={submitting ? "warning" : "primary"}
                    type="submit"
                    disabled={submitting}
                    onClick={(e) => {
                        if (headersInputRef.current?.value === "") e.preventDefault();
                    }}
                >
                    Submit
                    {submitting && <Spinner className="ms-2" animation="border" role="status" size="sm" />}
                </Button>
                {(!user.is_superuser && user.id > -1) &&
                    <Button variant="danger" className="ms-2" onClick={() => {
                        deleteUser(user.id).then(() => {
                            if (onDelete) {
                                onDelete(user.id)
                            }
                        }).catch((e) => document.location.reload());
                    }}>
                        Delete
                    </Button>
                }
            </Form>
        </Container>
    );
}

export default AccountForm;