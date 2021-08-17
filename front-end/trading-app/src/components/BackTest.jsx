import React, { Component, useEffect, useContext } from "react";
import useFetch from "../customeHooks/useFetch";
import { BACKEND_URL } from "../config";
import { StrategyContext } from "../contexts/StrategyContext";

const BackTest = () => {
  const { data, error, isPending } = useFetch(BACKEND_URL + "test");

  useEffect(() => {
    data && window.Bokeh.embed.embed_item(data, "myplot");
    data && console.log("I'm in!", data);
  }, [data]);

  return (
    <div>
      {error && <div> {error}</div>}
      {isPending && <div> ...loading</div>}
      {<div id="myplot"></div>}
    </div>
  );
};

export default BackTest;
