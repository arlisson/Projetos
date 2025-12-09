// src/App.tsx
import { Routes, Route } from 'react-router-dom'
import { Main } from './views/Main'
import { CadastrarCarta } from './views/Cartas/CadastrarCarta'
import { CadastrarProduto } from './views/Produtos/CadastrarProduto'
import { initLogs } from './services/logger'
import { useEffect } from 'react'
import { ListarCartas } from './views/Cartas/ListarCartas'
import { testDbConnection } from './Database/db'
import { ListarProdutos } from './views/Produtos/ListarProdutos'

export default function App() {

  useEffect(() => {
    
    initLogs() 

    testDbConnection().then((res) => {
      console.log(res.message)
    })
  }, [])
  

  return (
    <Routes>
      <Route path="/" element={<Main />} />

      {/* Cartas */}
      <Route path="/cartas/cadastrar" element={<CadastrarCarta />} />
      <Route path="/cartas/listar" element={<ListarCartas />} />

      {/* Produtos */}
      <Route path="/produtos/cadastrar" element={<CadastrarProduto />} />
      <Route path="/produtos/listar" element={<ListarProdutos />} />

    </Routes>
  )
}
