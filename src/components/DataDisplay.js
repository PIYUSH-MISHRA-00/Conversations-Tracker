import React, { useState } from 'react';
import { Table, Button, Form } from 'react-bootstrap';
import { saveAs } from 'file-saver';
import * as XLSX from 'xlsx';

const DataDisplay = ({ data, setFilteredData }) => {
    const [updatedData, setUpdatedData] = useState(data);

    const handleCheckboxChange = (index) => {
        const newData = [...updatedData];
        newData[index].Called = !newData[index].Called;
        setUpdatedData(newData);
    };

    const handleNotesChange = (index, notes) => {
        const newData = [...updatedData];
        newData[index].Notes = notes;
        setUpdatedData(newData);
    };

    const handleDownload = () => {
        const ws = XLSX.utils.json_to_sheet(updatedData);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
        const wbout = XLSX.write(wb, { bookType: "xlsx", type: "array" });
        saveAs(new Blob([wbout], { type: "application/octet-stream" }), "updated_call_data.xlsx");
    };

    return (
        <div>
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>Phone Number</th>
                        <th>Called</th>
                        <th>Notes</th>
                    </tr>
                </thead>
                <tbody>
                    {updatedData.map((row, index) => (
                        <tr key={index}>
                            <td>{row['Phone Number']}</td>
                            <td>
                                <Form.Check
                                    type="checkbox"
                                    checked={row.Called}
                                    onChange={() => handleCheckboxChange(index)}
                                />
                            </td>
                            <td>
                                <Form.Control
                                    as="textarea"
                                    value={row.Notes}
                                    onChange={(e) => handleNotesChange(index, e.target.value)}
                                />
                            </td>
                        </tr>
                    ))}
                </tbody>
            </Table>
            <Button variant="primary" onClick={handleDownload}>Download Updated Data</Button>
        </div>
    );
};

export default DataDisplay;
