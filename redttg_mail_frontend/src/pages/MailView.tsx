import { useNavigate, useParams } from "react-router-dom";
import { Mail } from "../interfaces/Mail";
import { useEffect, useState } from "react";
import { getMail } from "../controllers/Mail";
import { Badge, Card, Container, Row } from "react-bootstrap";
import DOMPurify from 'dompurify';

function MailView() {
    const mailId: number = parseInt(useParams().mailId!!);
    const navigate = useNavigate()
    const [mail, setMail] = useState<Mail>({
        id: 1,
        subject: "",
        created: new Date(),
        envelope: { from: "", to: [""] },
        read: false,
        text: "loading email information...",
        html: "",
        from_sender: "",
        star: false,
        deleted: false,
        attachments: []
    });

    useEffect(() => {
        getMail(mailId).then(setMail).catch((err) => navigate('/login'));
    }, [mailId])


    return (
        <Container className="h-100">
            <Card className="h-100 m-2">
                <Card.Header>
                    <Card.Title>
                        <h1>{mail.subject}</h1>
                    </Card.Title>
                    <Container>
                        <Row>
                            <Badge className="w-auto my-2">
                                from: <Badge pill bg="success">{mail.envelope.from}</Badge>
                            </Badge>
                        </Row>
                        <Row>
                            <Badge className="w-auto my-2">
                                to:
                                {mail.envelope.to.map((to) => (
                                    <Badge pill bg="success">{to}</Badge>
                                ))}
                            </Badge>
                        </Row>
                    </Container>
                </Card.Header>

                <Card.Body>
                    {mail.html && <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(mail.html) }}></div>}
                    {!mail.html && <Card.Text>{mail.text}</Card.Text>}
                </Card.Body>
            </Card>
        </Container>
    );
}

export default MailView;