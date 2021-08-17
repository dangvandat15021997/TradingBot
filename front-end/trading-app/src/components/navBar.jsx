import React, { Component } from "react";
import { Link } from "react-router-dom";
import { Navbar, Container, Nav } from "react-bootstrap";

const NavBar = () => {
  return (
    <Navbar bg="light" variant="light">
      <Container>
        <Navbar.Brand href="/">CoinView</Navbar.Brand>
        <Nav className="me-auto">
          <Nav.Link href="/coin">Coin</Nav.Link>
          <Nav.Link href="/backtest">BackTest</Nav.Link>
        </Nav>
      </Container>
    </Navbar>
  );
};

export default NavBar;
