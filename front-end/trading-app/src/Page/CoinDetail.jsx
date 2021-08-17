import React, { useEffect, useContext, useState } from "react";
import { useParams } from "react-router-dom/cjs/react-router-dom.min";
import { TradingViewStockChartWidget } from "react-tradingview-components";
import { CoinPairContext } from "../contexts/CoinPairContext";
import useFetch from "../customeHooks/useFetch";
import { BACKEND_URL } from "../config";

const CoinDetail = () => {
  const { symbol } = useParams();
  const { idSignal } = useContext(CoinPairContext);
  const [input, setInput] = useState([]);

  const {
    data: signalIndicator,
    errorIndicator,
    isPendingIndicator,
  } = useFetch(BACKEND_URL + "indicator/" + idSignal);

  useEffect(() => {
    console.log("I'm in Indicator", signalIndicator);
    const new_input = [];
    if (signalIndicator !== null && signalIndicator.length >= 1) {
      signalIndicator.forEach((element) => {
        console.log("Element: ", element);
        let new_obj = {
          id: element["id_indicator"] + "@tv-basicstudies",
          inputs: {},
        };

        for (let inner in element) {
          inner !== "id_indicator" && (new_obj.inputs[inner] = element[inner]);
        }
        new_input.push(new_obj);
      });
    }

    setInput(new_input);
  }, [signalIndicator]);

  return (
    <div id="coindetail-container" style={{ height: 510 }}>
      {errorIndicator && <div>errorIndicator</div>}
      {isPendingIndicator && <div>...Loading</div>}
      {signalIndicator && (
        <TradingViewStockChartWidget
          symbol={"BINANCE:" + symbol}
          theme="Dark"
          interval="D"
          studies={[]}
          autosize
        />
      )}
    </div>
  );
};

export default CoinDetail;
