import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Recommendations from './Recommendations';

const App = () => {
  const [userId, setUserId] = useState<number>(1);

  return (
    <Router>
      <div>
        <h1>Findir.ai</h1>
        <button onClick={() => setUserId(1)}>User 1</button>
        <button onClick={() => setUserId(2)}>User 2</button>
        <Switch>
          <Route path="/recommendations">
            <Recommendations userId={userId} />
          </Route>
        </Switch>
      </div>
    </Router>
  );
};

export default App;