import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Registros from './pages/Registros'
import NovoRegistro from './pages/NovoRegistro'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/registros" />} />
        <Route path="/registros" element={<Registros />} />
        <Route path="/registros/novo" element={<NovoRegistro />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App