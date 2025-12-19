// scraping-server/src/cli.ts
import { buscarProdutoLiga } from './buscarProdutoLiga'

async function main() {
  const url = process.argv[2]
  if (!url) {
    console.error('URL obrigatória')
    process.exit(1)
  }

  try {
    const produto = await buscarProdutoLiga(url)
    // imprime JSON no stdout, que o Tauri vai ler
    console.log(JSON.stringify(produto ?? null))
  } catch (e) {
    console.error('Erro no scraping:', e)
    process.exit(1)
  }
}

void main()
