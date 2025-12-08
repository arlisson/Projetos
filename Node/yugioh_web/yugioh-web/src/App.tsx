// src/App.tsx
import { Routes, Route } from 'react-router-dom'
import { Main } from './views/Main'
import { CadastrarCarta } from './views/CadastrarCarta'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Main />} />

      {/* Cartas */}
      <Route path="/cartas/cadastrar" element={<CadastrarCarta />} />
      {/* depois você cria /cartas/listar, /cartas/colecao/cadastrar, etc. */}
    </Routes>
  )
}
