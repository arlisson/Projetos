type ItemKind = 'Carta' | 'Produto'

interface CarrosselItemProps {
  name: string
  kind: ItemKind
  currentPrice: string
  maxPrice: string
  minPrice: string
}

export function CarrosselItem({
  name,
  kind,
  currentPrice,
  maxPrice,
  minPrice,
}: CarrosselItemProps) {
  return (
    <div className="carousel-item">
      <div className="carousel-item-title">{name}</div>
      <div className="badge-kind">{kind}</div>

      <div style={{ marginTop: 8 }}>
        <div className="carousel-item-row">
          <span>Preço atual</span>
          <strong>{currentPrice}</strong>
        </div>
        <div className="carousel-item-row">
          <span>Maior preço</span>
          <span>{maxPrice}</span>
        </div>
        <div className="carousel-item-row">
          <span>Menor preço</span>
          <span>{minPrice}</span>
        </div>
      </div>
    </div>
  )
}
