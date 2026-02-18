// src/App.tsx
import { Routes, Route } from 'react-router-dom'
import { Main } from './views/Main'
import { CadastrarCarta } from './views/Cartas/CadastrarCarta'
import { CadastrarProduto } from './views/Produtos/CadastrarProduto'
import { ListarCartas } from './views/Cartas/ListarCartas'
import { ListarProdutos } from './views/Produtos/ListarProdutos'
import { ListarVendasCartas } from './views/Cartas/ListarVendasCartas'
import { ListarVendasProdutos } from './views/Produtos/ListarVendasProdutos'
import { EditarCarta } from './views/Cartas/EditarCarta'
import { EditarProduto } from './views/Produtos/EditarProduto'
import { EditarVendasCartas } from './views/Cartas/EditarVendasCartas'

export default function App() {

  

  return (
    <Routes>
      <Route path="/" element={<Main />} />
      

      {/* Cartas */}
      <Route path="/cartas/cadastrar" element={<CadastrarCarta />} />
      <Route path="/cartas/listar" element={<ListarCartas />} />
      <Route path="/cartas/vendas/listar" element={<ListarVendasCartas />} />
      <Route path="/cartas/vendas/editar" element={<EditarVendasCartas />} />
      <Route path="/cartas/editar" element={<EditarCarta />} />

      {/* Produtos */}
      <Route path="/produtos/cadastrar" element={<CadastrarProduto />} />
      <Route path="/produtos/listar" element={<ListarProdutos />} />
      <Route path='/produtos/vendas/listar' element={<ListarVendasProdutos />} />
      <Route path="/produtos/editar" element={<EditarProduto />} />

    </Routes>
  )
}
