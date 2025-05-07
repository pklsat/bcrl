import React from 'react';
import { Link, Outlet } from 'react-router-dom';

function App() {
  return (
    <div>
      <header>
        <div><Link to="/">Home</Link></div>
        <div><Link to="/jobs">Job一覧</Link></div>
        <div><Link to="/submit">Job登録</Link></div>
      </header>
      <main>
        <Outlet />
      </main>
    </div>
  );
}
export default App;