import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';

const NavbarComponent = ({ setFilteredData, data }) => {
    const handleSelect = (eventKey) => {
        if (eventKey === "Show All") {
            setFilteredData(data);
        } else if (eventKey === "Called") {
            setFilteredData(data.filter(row => row.Called));
        }
    };

    return (
        <Navbar bg="light" expand="lg">
            <Navbar.Brand href="#">Call Management Platform</Navbar.Brand>
            <Nav className="me-auto">
                <Nav.Link eventKey="Show All" onClick={() => handleSelect("Show All")}>Show All</Nav.Link>
                <Nav.Link eventKey="Called" onClick={() => handleSelect("Called")}>Called</Nav.Link>
            </Nav>
        </Navbar>
    );
};

export default NavbarComponent;
