import { Col, Row } from 'react-bootstrap';

interface SideBarProps {
    sideElement: React.ReactNode;
    children?: React.ReactNode;
}

function SideBar({ sideElement, children }: SideBarProps) {
    return (
        <Row className="p-0 m-0">
            <Col xs={3} className="p-2 m-0 h-100">{children}</Col>
            <Col xs={9} className="p-0 m-0 pe-5">
                {sideElement}
            </Col>
        </Row>
    );
}

export default SideBar;