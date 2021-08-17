import React, { Component, useContext } from "react";
import { CoinPairContext } from "../contexts/CoinPairContext";
import SymbolRow from "./SymbolRow";
import { Table } from "react-bootstrap";
import { v4 as uuidv4 } from "uuid";

const SymbolGrid = () => {
  const { coinPair, errorCoinPair, isPendingCoinPair } =
    useContext(CoinPairContext);
  return (
    <div className="mr-auto ml-auto my-3 ">
      {
        <Table striped bordered hover size="md">
          <thead className="thead-dark">
            <tr>
              <th className="col-sm-6">Symbol</th>
              <th className="col-sm-6">Detail</th>
            </tr>
          </thead>
          <tbody>
            {errorCoinPair && <div>{errorCoinPair}</div>}
            {isPendingCoinPair && <div>Loading...</div>}
            {coinPair &&
              coinPair.map((cp) => <SymbolRow symbol={cp} key={uuidv4()} />)}
          </tbody>
        </Table>
      }
    </div>
  );
};

export default SymbolGrid;
