import React, { Component, useContext, useState } from "react";
import { Dropdown } from "react-bootstrap";
import { BACKEND_URL } from "../config";
import { StrategyContext } from "../contexts/StrategyContext";
import useFetch from "../customeHooks/useFetch";

const SelectParamsBackTest = () => {
  const {
    data: strategies,
    error,
    isPending,
  } = useFetch(BACKEND_URL + "strategy");

  const [dropdownValue, setDropdownValue] = useState({
    id: "0",
    name: "All Strategy",
  });

  const { idStrategy, setIDStrategy } = useContext(StrategyContext);

  const handleSelect = (eventKey, event) => {
    //Config Dropdown
    const strategy_name = findSignalName(eventKey);
    setDropdownValue({ id: eventKey, name: strategy_name });
    setIDStrategy(eventKey);
  };

  const findSignalName = (id) => {
    if (id == 0) {
      return "All Coin";
    }
    return strategies.find((x) => x.id == id).name;
  };

  return (
    <div className="mr-auto ml-auto my-3 ">
      {error && <div>{error}</div>}
      {isPending && <div>Loading...</div>}
      {strategies && (
        <div>
          {
            <Dropdown onSelect={handleSelect}>
              <Dropdown.Toggle variant="light" id="dropdown-basic">
                {dropdownValue.name}
              </Dropdown.Toggle>
              <Dropdown.Menu>
                <Dropdown.Item eventKey="0">All Coin</Dropdown.Item>
                <Dropdown.Divider />
                {strategies.map((strategy) => {
                  return (
                    <Dropdown.Item eventKey={strategy.id}>
                      {strategy.name}
                    </Dropdown.Item>
                  );
                })}
              </Dropdown.Menu>
            </Dropdown>
          }
        </div>
      )}
    </div>
  );
};

export default SelectParamsBackTest;
