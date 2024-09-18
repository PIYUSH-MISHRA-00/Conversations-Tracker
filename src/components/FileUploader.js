import React from 'react';
import { Form } from 'react-bootstrap';
import * as XLSX from 'xlsx';

const FileUploader = ({ setData, setFilteredData }) => {
    const handleFileUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                const wb = XLSX.read(event.target.result, { type: 'array' });
                const ws = wb.Sheets[wb.SheetNames[0]];
                const data = XLSX.utils.sheet_to_json(ws);
                setData(data);
                setFilteredData(data);
            };
            reader.readAsArrayBuffer(file);
        }
    };

    return (
        <div className="my-4">
            <Form.Group controlId="formFile">
                <Form.Label>Upload Excel File</Form.Label>
                <Form.Control type="file" accept=".xlsx" onChange={handleFileUpload} />
            </Form.Group>
        </div>
    );
};

export default FileUploader;
