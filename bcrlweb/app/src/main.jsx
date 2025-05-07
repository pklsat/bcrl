import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import App from "./App"
import Home from "./pages/Home"
import Jobs from "./pages/Jobs"
import Result from "./pages/Result"
import Submit from "./pages/Submit"
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} >
          <Route index element={<Home />} />
          <Route path="jobs" element={<Jobs />} />
          <Route path="jobs/:req_id" element={<Result />} />
          <Route path="submit" element={<Submit />} />
        </Route>
      </Routes>
    </BrowserRouter> 
  </React.StrictMode>
)