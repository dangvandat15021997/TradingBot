import React, {
  Component,
  useContext,
  useState,
  useEffect,
  useRef,
} from "react";
import { Dropdown, Container } from "react-bootstrap";
import { BACKEND_URL } from "../config";
import useFetch from "../customeHooks/useFetch";
import { CoinPairContext } from "../contexts/CoinPairContext";

const SignalSelect = () => {
  // fetch data for signal dropdown
  const { data: signals, error, isPending } = useFetch(BACKEND_URL + "signal");
  const [dropdownValue, setDropdownValue] = useState({
    id: "0",
    name: "All Coin",
  });

  const { setIDSignal } = useContext(CoinPairContext);

  const handleSelect = (eventKey, event) => {
    //Config Dropdown
    const signal_name = findSignalName(eventKey);
    setDropdownValue({ id: eventKey, name: signal_name });
    setIDSignal(eventKey);
  };

  const findSignalName = (id) => {
    if (id == 0) {
      return "All Coin";
    }
    return signals.find((x) => x.id == id).name;
  };

  return (
    <div className="mr-auto ml-auto my-3 ">
      {error && <div>{error}</div>}
      {isPending && <div>Loading...</div>}
      {signals && (
        <div>
          {
            <Dropdown onSelect={handleSelect}>
              <Dropdown.Toggle variant="light" id="dropdown-basic">
                {dropdownValue.name}
              </Dropdown.Toggle>
              <Dropdown.Menu>
                <Dropdown.Item eventKey="0">All Coin</Dropdown.Item>
                <Dropdown.Divider />
                {signals.map((signal) => {
                  return (
                    <Dropdown.Item eventKey={signal.id}>
                      {signal.name}
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

export default SignalSelect;
