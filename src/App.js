import React, { useState } from 'react';
import FileUploader from './components/FileUploader';
import DataDisplay from './components/DataDisplay';
import SummaryStats from './components/SummaryStats';
import Navbar from './components/Navbar';

function App() {
    const [data, setData] = useState(null);
    const [filteredData, setFilteredData] = useState(null);

    return (
        <div className="container">
            <Navbar setFilteredData={setFilteredData} data={data} />
            <FileUploader setData={setData} setFilteredData={setFilteredData} />
            {filteredData && (
                <>
                    <DataDisplay data={filteredData} setFilteredData={setFilteredData} />
                    <SummaryStats data={filteredData} />
                </>
            )}
        </div>
    );
}

export default App;
