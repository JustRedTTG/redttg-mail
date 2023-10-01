import { useEffect, useState } from "react";
import { Badge, Card, Col, Container, Row } from "react-bootstrap";
import { MailPreview } from "../interfaces/Mail";
import { getMails } from "../controllers/Mail";
import { useNavigate } from "react-router-dom";
import { LinkContainer } from "react-router-bootstrap";

function Home() {
    const navigate = useNavigate()
    const [mails, setMails] = useState<MailPreview[]>([]);

    useEffect(() => {
        getMails().then(setMails).catch((err) => navigate('/login'));
    }, []);

    return (
        <Container>
            {mails.map((mail) => (
                <LinkContainer to={`/mail/${mail.id}`}>
                    <a className="text-decoration-none">
                    <Card role="button" className="my-3 p-1 btn btn-danger">
                        <Row>
                            <Col xs="auto">
                                <div className="m-1">
                                    <Row>
                                        <Col xs="auto">
                                            <Badge bg={mail.read ? 'secondary' : 'primary'}>{mail.envelope.from}</Badge>
                                        </Col>
                                        <Col>
                                            <Card.Title className="mb-0">
                                                {mail.subject}
                                            </Card.Title>
                                        </Col>
                                    </Row>
                                </div>
                            </Col>

                        </Row>
                    </Card>
                    </a>
                </LinkContainer>
            ))}

        </Container>
    );
}

export default Home;