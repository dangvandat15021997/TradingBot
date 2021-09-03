import React, { useState, createContext, useEffect } from "react";
import useFetch from "../customeHooks/useFetch";
import { BACKEND_URL } from "../config";

export const CoinPairContext = createContext();

const CoinPairContextProvider = (props) => {
  const [idSignal, setIDSignal] = useState(0);

  // fetch data for symbol CoinPairContext
  const {
    data: coinPair,
    errorCoinPair,
    isPendingCoinPair,
  } = useFetch(BACKEND_URL + "signal/" + idSignal);

  useEffect(() => {
    console.log("I'm in Signal context", coinPair);
  }, [coinPair]);

  useEffect(() => {
    console.log("I'm in SignalID: ", idSignal);
  }, [idSignal]);

  return (
    <CoinPairContext.Provider
      value={{
        coinPair,
        errorCoinPair,
        isPendingCoinPair,
        setIDSignal,
        idSignal,
      }}
    >
      {props.children}
    </CoinPairContext.Provider>
  );
};

export default CoinPairContextProvider;
