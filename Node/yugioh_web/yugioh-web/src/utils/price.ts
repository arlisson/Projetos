export function normalizePriceText(value: string | number | null | undefined): string {
  if (typeof value === 'number') {
    return Number.isFinite(value) ? value.toFixed(2) : '0.00'
  }

  const text = String(value ?? '').trim()
  if (!text) return '0.00'

  const token = text
    .replace(/\s+/g, '')
    .replace(/^R\$/i, '')
    .replace(/[^\d.,-]/g, '')

  if (!token) return '0.00'

  const hasComma = token.includes(',')
  const hasDot = token.includes('.')

  if (hasComma && hasDot) {
    const normalized =
      token.lastIndexOf(',') > token.lastIndexOf('.')
        ? token.replace(/\./g, '').replace(',', '.')
        : token.replace(/,/g, '')

    return normalizeNumericString(normalized)
  }

  if (hasComma) {
    return normalizeNumericString(token.replace(/\./g, '').replace(',', '.'))
  }

  if (hasDot) {
    const parts = token.split('.')
    const last = parts[parts.length - 1]

    if (parts.length > 2 || last.length === 3) {
      return normalizeNumericString(token.replace(/\./g, ''))
    }

    return normalizeNumericString(token)
  }

  return normalizeNumericString(token)
}

export function parsePriceNumber(
  value: string | number | null | undefined,
): number {
  const numberValue = Number(normalizePriceText(value))
  return Number.isFinite(numberValue) ? numberValue : 0
}

function normalizeNumericString(value: string): string {
  const numberValue = Number(value)
  return Number.isFinite(numberValue) ? numberValue.toFixed(2) : '0.00'
}
