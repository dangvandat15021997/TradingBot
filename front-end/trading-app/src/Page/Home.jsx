import React, { Component } from "react";
import SymbolGrid from "../components/SymbolGrid";
import SignalSelect from "../components/SignalSelect";

const Home = () => {
  return (
    <React.Fragment>
      <SignalSelect />
      <SymbolGrid />
    </React.Fragment>
  );
};

export default Home;
