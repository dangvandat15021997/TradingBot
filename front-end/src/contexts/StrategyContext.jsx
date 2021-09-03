import React, { Component, createContext, useState } from "react";

export const StrategyContext = createContext();

const StrategyContextProvider = (props) => {
  const [idStrategy, setIDStrategy] = useState("");

  return (
    <StrategyContext.Provider value={(idStrategy, setIDStrategy)}>
      {props.children}
    </StrategyContext.Provider>
  );
};

export default StrategyContextProvider;
