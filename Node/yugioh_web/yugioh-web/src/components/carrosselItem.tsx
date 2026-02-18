/**
 * Renders a carousel item displaying Yu-Gi-Oh card or product information.
 * 
 * Shows the item name, type badge, product image, and price information
 * (current, maximum, and minimum prices).
 * 
 * @param {CarrosselItemProps} props - The carousel item properties
 * @param {string} props.name - The name of the card or product
 * @param {ItemKind} props.kind - The type of item: 'Carta' (Card) or 'Produto' (Product)
 * @param {string} props.currentPrice - The current price formatted as a string
 * @param {string} props.maxPrice - The maximum price formatted as a string
 * @param {string} props.minPrice - The minimum price formatted as a string
 * @param {string | null} props.imageUrl - The URL of the item image, or null if not available
 * 
 * @returns {JSX.Element} A carousel item component displaying all item details
 */
type ItemKind = 'Carta' | 'Produto'

interface CarrosselItemProps {
  name: string
  kind: ItemKind
  currentPrice: string
  maxPrice: string
  minPrice: string
  imageUrl: string | null
  rarity?: string // Optional rarity field, only relevant for 'Carta' kind
}

export function CarrosselItem({
  name,
  kind,
  currentPrice,
  maxPrice,
  minPrice,
  imageUrl,
  rarity
}: CarrosselItemProps) {
  return (
    <div className="carousel-item">
      <div className="carousel-item-title">{name}</div>
      {kind === 'Carta' && <div className="carousel-item-title">{rarity}</div>}
      {/* <div className="badge-kind">{kind}</div> */}

      <div style={{ marginTop: 8 }}>
        <div className="carousel-item-media">
          <img className="carrousel-item-image" src={imageUrl || ''} alt={name} />
        </div>
              
        <div className="carousel-item-row" style={{ marginTop: 8 }}>
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
