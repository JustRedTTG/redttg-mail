import { useEffect, useState } from "react";
import { Table, Spinner, Modal, Button, Form } from "react-bootstrap";
import { Headers } from "../interfaces/User";

interface HeadersInputProps {
    headersInputRef: React.RefObject<HTMLInputElement>;
}

function HeadersInput({ headersInputRef }: HeadersInputProps) {
    const [headers, setHeaders] = useState<Headers | undefined>(undefined);
    const [indexes, setIndexes] = useState<string[] | undefined>(undefined);
    const [focus, setFocus] = useState<number | undefined>(undefined);
    const [error, setError] = useState<string | undefined>(undefined);
    const [inputError, setInputError] = useState<boolean>(false);
    const [deselected, setDeselected] = useState<string | undefined>(undefined);

    useEffect(() => {
        if (headersInputRef.current?.value) {
            let newHeaders: Headers = JSON.parse(headersInputRef.current?.value);
            setHeaders(newHeaders);
            setIndexes(Object.keys(newHeaders));
        }
    }, [headersInputRef.current]);

    if (headers === undefined || indexes === undefined) return (<div className="w-100 m-3 d-flex justify-content-center"><Spinner variant="warning" /></div>);

    function newHeader(e: React.ChangeEvent<HTMLInputElement>) {
        if (headers === undefined || indexes === undefined) return;
        if (indexes.includes(e.target.value)) {
            setInputError(true);
            return;
        } else setInputError(false);
        setFocus(Object.keys(headers).length);
        setHeaders({ ...headers, [e.target.value]: "" });
        setIndexes([...indexes, e.target.value]);
        e.target.value = "";
    }

    function setHeaderKey(e: React.ChangeEvent<any>, key: string) {
        if (headers === undefined || indexes === undefined) return;
        if (key === e.target.value) return;
        let newHeaders = { ...headers };
        let newIndexes = [...indexes];
        e.target.value = e.target.value.replace(/[^a-zA-Z0-9-]/g, "");
        if (e.target.value) {
            if (newHeaders[e.target.value] !== undefined) {
                return;
            }
            newHeaders[e.target.value] = headers[key];
            newIndexes[newIndexes.indexOf(key)] = e.target.value;
            if (key === error) {
                setError(undefined);
            }
        } else {
            setError(key);
            return;
        }
        delete newHeaders[key];
        setHeaders(newHeaders);
        setIndexes(newIndexes);
    }

    function setHeaderValue(e: React.ChangeEvent<any>, key: string) {
        if (headers === undefined) return;
        let newHeaders = { ...headers };
        newHeaders[key] = e.target.value;
        setHeaders(newHeaders);
    }

    function removeHeaderKey(key: string, dialog?: boolean) {
        if (headers === undefined || indexes === undefined) return;
        let newHeaders = { ...headers };
        let newIndexes = [...indexes];
        delete newHeaders[key];
        newIndexes.splice(newIndexes.indexOf(key), 1);
        setError(undefined);
        setFocus(undefined);
        setDeselected(undefined);
        if (!dialog) {
            setHeaders(newHeaders);
            setIndexes(newIndexes);
            return;
        }
        setTimeout(() => { setHeaders(newHeaders); setIndexes(newIndexes); }, 100);
    }

    function cancelSelectHeaderKey(index: number) {
        setError(undefined);
    }

    return (
        <Table className="m-0">
            {indexes.map((key, index) => (
                <tr>
                    <td className="pe-1 pb-2">
                        <Form.Control
                            value={error === key ? "" : key}
                            isValid={error !== key}
                            isInvalid={error === key}
                            onChange={(e) => setHeaderKey(e, key)}
                            autoFocus={index === focus}
                            onBlur={() => setDeselected(key)}
                            onFocus={() => setDeselected(undefined)}
                        /></td>
                    <td className="ps-1 pb-2"><Form.Control
                        value={headers[key]}
                        onChange={(e) => setHeaderValue(e, key)}
                    /></td>
                    <Modal
                        show={error === key && deselected === key}
                        onHide={() => removeHeaderKey(key, true)}>
                        <Modal.Header closeButton>
                            <Modal.Title>Delete header?</Modal.Title>
                        </Modal.Header>

                        <Modal.Body>
                            <p>Do you wish to discard this header and it's value?</p>
                        </Modal.Body>

                        <Modal.Footer>
                            <Button variant="secondary" onClick={() => cancelSelectHeaderKey(index)}>Cancel</Button>
                            <Button variant="warning" onClick={() => removeHeaderKey(key)}>Delete</Button>
                        </Modal.Footer>
                    </Modal>
                </tr>
            ))}
            <tr>
                <td className="pe-1"><Form.Control
                    placeholder="Start typing to add a new Header"
                    onChange={newHeader}
                    isInvalid={inputError}
                    isValid={false}
                    onBlur={(e) => { setInputError(false); e.target.value = ""; }}
                /></td>
                <td className="ps-1"><Form.Control disabled /></td>
            </tr>
        </Table>
    );
}

export default HeadersInput;