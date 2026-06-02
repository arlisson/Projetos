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
import { EditarVendasProdutos } from './views/Produtos/EditarVendasProdutos'
import { CadastrarCartasColecao } from './views/Cartas/CadastrarCartasColecao'
import RaridadeQualidade from './views/Gestao/RaridadeQualidade'
import {Logs} from './views/Sistema/Logs'
import { ScraperConfigs } from './views/Sistema/ScraperConfigs'
import BancoDeDados from './views/Gestao/BancoDeDados'
import Colecoes from './views/Gestao/Colecoes'

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
      <Route path="/cartas/cadastrar/cadastrar-colecao" element={<CadastrarCartasColecao/>}/>
      
      {/* Produtos */}
      <Route path="/produtos/cadastrar" element={<CadastrarProduto />} />
      <Route path="/produtos/listar" element={<ListarProdutos />} />
      <Route path='/produtos/vendas/listar' element={<ListarVendasProdutos />} />
      <Route path="/produtos/vendas/editar" element={<EditarVendasProdutos />} />
      <Route path="/produtos/editar" element={<EditarProduto />} />

      {/*Sistema*/}
      <Route path="/log/visualizar" element={<Logs/>}/>
      <Route path="/scrapers/gestao" element={<ScraperConfigs/>}/>
      <Route path="/raridade-qualidade/gestao" element={<RaridadeQualidade/>}/>
      <Route path="/colecoes/gestao" element={<Colecoes/>}/>
      <Route path='/database/gestao' element={<BancoDeDados/>}/>

    </Routes>
  )
}
