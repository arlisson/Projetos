// scraping-server/src/server.ts
import express from 'express'
import { buscarProdutoLiga } from './buscarProdutoLiga'



const app = express()

app.get('/produto', async (req, res) => {
  const url = String(req.query.url || '')
  if (!url) {
    return res.status(400).json({ error: 'Parâmetro url é obrigatório' })
  }

  try {
    const produto = await buscarProdutoLiga(url)
    if (!produto) {
      return res.status(404).json({ error: 'Produto não encontrado' })
    }
    return res.json(produto)
  } catch (e) {
    console.error('Erro ao buscar produto:', e)
    return res.status(500).json({ error: String(e) })
  }
})

const PORT = 3001
app.listen(PORT, () => {
  console.log(`Scraping server rodando em http://localhost:${PORT}`)
})
