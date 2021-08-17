import React, { Component } from "react";
import { Link } from "react-router-dom";

const SymbolRow = ({ symbol }) => {
  return (
    <tr>
      <td>{symbol.symbol}</td>

      <td>
        <Link to={"/coin/" + symbol.symbol}>Detail</Link>
      </td>
    </tr>
  );
};

export default SymbolRow;
