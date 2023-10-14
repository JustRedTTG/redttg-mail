import { Spinner, SpinnerProps } from "react-bootstrap";

function CenteredSpinner({variant, animation }: SpinnerProps) {
    return ( 
    <div className="w-100 my-3 d-flex justify-content-center">
        <Spinner animation={animation? animation : "grow"} variant={variant? variant : "primary"} />
    </div> );
}

export default CenteredSpinner;