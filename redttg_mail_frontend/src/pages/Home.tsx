import { useEffect, useState } from "react";
import { Badge, Card, Container, Stack } from "react-bootstrap";
import { MailPreview } from "../interfaces/Mail";
import { getMails } from "../controllers/Mail";
import { useNavigate } from "react-router-dom";
import { LinkContainer } from "react-router-bootstrap";

function Home() {
    const navigate = useNavigate()
    const [mails, setMails] = useState<MailPreview[]>([]);

    useEffect(() => {
        getMails().then(setMails).catch((err) => navigate('/login', { replace: true }));
    }, [navigate]);

    return (
        <Container>
            {mails.length < 1 &&
                <p className="w-100 text-center">No mail yet</p>
            }
            {mails.map((mail) => (
                <LinkContainer to={`/mail/${mail.id}`}>
                    <a className="text-decoration-none" href={`/mail/${mail.id}`}>
                        <Card role="button" className="my-3 p-0 btn btn-incoming">
                            <Card.Header>
                                <Stack direction="vertical" gap={1}>
                                    <Stack direction="horizontal" gap={1}>
                                        <p className="my-auto">From:</p>
                                        <Badge className="mt-auto" bg={mail.read ? 'thirdly' : 'primary'}>{mail.envelope.from}</Badge>
                                    </Stack>
                                    {mail.attachments.length > 0 &&
                                        <Stack direction="horizontal" gap={1}>
                                            <Badge pill bg="info" className="attachment_badge">{mail.attachments[0].filename}</Badge>
                                            {mail.attachments.length > 1 &&
                                                <Badge pill bg="info" className="attachment_badge">+{mail.attachments.length - 1}</Badge>
                                            }
                                        </Stack>
                                    }
                                </Stack>
                            </Card.Header>
                            <Card.Body>
                                <Card.Title className="mb-0">
                                    {mail.subject}
                                </Card.Title>

                            </Card.Body>
                        </Card>
                    </a>
                </LinkContainer>
            ))}

        </Container>
    );
}

export default Home;