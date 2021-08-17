import logo from './logo.svg';
import './App.css';
import NavBar from './components/navBar';
import { BrowserRouter as Router, Link, Route, Switch } from 'react-router-dom';
import BackTest from './components/BackTest';
import { Container } from 'react-bootstrap';
import  CoinPairContextProvider  from './contexts/CoinPairContext';
import CoinDetail from './Page/CoinDetail';
import Home from './Page/Home';
import StrategyContextProvider from './contexts/StrategyContext';
import SelectParamsBackTest from './components/SelectParamsBackTest';

function App() {
  return (
    <Container>
    <Router>
      <div className="cointainer">
      <CoinPairContextProvider>
          <NavBar/>
          <Switch>
              <div className="row">
                <div className = "mr-auto ml-auto mt-2 mb-2">
                  <Switch>
                      <Route exact path="/">
                        <Home/>
                      </Route>
                      <Route path = "/coin/:symbol">
                        <CoinDetail/>
                      </Route>
                      <Route path = "/backtest">
                        <StrategyContextProvider>
                          <SelectParamsBackTest/>
                          <BackTest/>
                        </StrategyContextProvider>
          
                      </Route>
                  </Switch>
                </div>
              </div>
          </Switch>
      </CoinPairContextProvider>
      </div>
    </Router>
    </Container>
  );
}

export default App;
