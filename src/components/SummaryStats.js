import React from 'react';
import { Card } from 'react-bootstrap';
import Plot from 'react-plotly.js';

const SummaryStats = ({ data }) => {
    const totalCalls = data.filter(row => row.Called).length;
    const totalRecords = data.length;
    const toBeCalled = totalRecords - totalCalls;

    const chartData = [
        {
            type: 'pie',
            labels: ['Called', 'To be Called'],
            values: [totalCalls, toBeCalled],
        }
    ];

    return (
        <div className="my-4">
            <Card>
                <Card.Body>
                    <Card.Title>Summary</Card.Title>
                    <Card.Text>
                        Total Records: {totalRecords}<br />
                        Total Calls Made: {totalCalls}<br />
                        Pending Calls: {toBeCalled}
                    </Card.Text>
                    <Plot data={chartData} />
                </Card.Body>
            </Card>
        </div>
    );
};

export default SummaryStats;
