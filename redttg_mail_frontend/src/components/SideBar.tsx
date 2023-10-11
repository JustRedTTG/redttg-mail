import { Col, Row } from 'react-bootstrap';

interface SideBarProps {
    sideElement: React.ReactNode;
    children?: React.ReactNode;
}

function SideBar({ sideElement, children }: SideBarProps) {
    return (
        <Row className="p-0 m-0">
            <Col xs={2} className="p-0 m-0 m-2 h-100">{children}</Col>
            <Col xs="auto" className="p-0 m-0">
                {sideElement}
            </Col>
        </Row>
    );
}

export default SideBar;