import type * as cheerio from 'cheerio'

export type ScraperSite = 'mypcards' | 'ligayugioh'
export type ScraperAttribute = 'text' | 'html' | string
export type ScraperTransform = 'text' | 'number' | 'currency-brl' | 'absolute-url'

export interface ScraperFieldConfig {
  selectors: string[]
  attribute: ScraperAttribute
  index?: number | null
  regex?: string | null
  transform?: ScraperTransform
  fallback?: string | number | null
  active?: boolean
}

export interface ScraperSiteConfig {
  site: ScraperSite
  label: string
  baseUrl: string
  fields: Record<string, ScraperFieldConfig>
}

export function normalizeCurrencyBrl(value: unknown): string {
  const text = String(value ?? '').trim()
  if (!text) return '0.00'

  const withCurrency = [
    ...text.matchAll(
      /R\$\s*(\d{1,3}(?:,\d{3})*\.\d{2}|\d{1,3}(?:\.\d{3})*,\d{2}|\d+(?:[.,]\d{2})?)(?![\d.,])/g,
    ),
  ].map((match) => match[1])

  const candidates =
    withCurrency.length > 0
      ? withCurrency
      : text.match(
          /(?:\d{1,3}(?:,\d{3})*\.\d{2}|\d{1,3}(?:\.\d{3})*,\d{2}|\d+(?:[.,]\d{2})?)(?![\d.,])/g,
        )

  if (!candidates || candidates.length === 0) return '0.00'

  const selected = candidates.length >= 2 ? candidates[1] : candidates[0]
  return normalizeDecimalToken(selected)
}

function normalizeDecimalToken(value: string): string {
  const token = String(value || '').trim()
  if (!token) return '0.00'

  const hasComma = token.includes(',')
  const hasDot = token.includes('.')

  if (hasComma && hasDot) {
    if (token.lastIndexOf(',') > token.lastIndexOf('.')) {
      return token.replace(/\./g, '').replace(',', '.')
    }

    return token.replace(/,/g, '')
  }

  if (hasComma) return token.replace(/\./g, '').replace(',', '.')

  if (hasDot) {
    const parts = token.split('.')
    const last = parts[parts.length - 1]

    if (parts.length > 2 || last.length === 3) {
      return token.replace(/\./g, '')
    }

    return token
  }

  return token
}

function normalizeNumber(value: unknown): string {
  const text = String(value ?? '').trim()
  if (!text) return '0'

  const normalized = normalizeCurrencyBrl(text)
  if (normalized !== '0.00') return normalized

  const cleaned = text.replace(/[^\d.,-]/g, '')
  return cleaned ? normalizeDecimalToken(cleaned) : '0'
}

function toAbsoluteUrl(baseUrl: string, value: unknown): string {
  const text = String(value ?? '').trim()
  if (!text) return ''

  try {
    return new URL(text, baseUrl).toString()
  } catch {
    return text
  }
}

function applyRegex(value: string, regex?: string | null): string {
  if (!regex) return value
  const match = value.match(new RegExp(regex))
  return (match?.[1] ?? match?.[0] ?? '').trim()
}

function applyTransform(
  value: string,
  transform: ScraperTransform | undefined,
  baseUrl: string,
): string {
  if (transform === 'currency-brl') return normalizeCurrencyBrl(value)
  if (transform === 'number') return normalizeNumber(value)
  if (transform === 'absolute-url') return toAbsoluteUrl(baseUrl, value)
  return value.trim()
}

export function extractConfiguredData(
  $: cheerio.CheerioAPI,
  config: ScraperSiteConfig,
  baseUrl: string,
): Record<string, string | number | null> {
  const values: Record<string, string | number | null> = {}

  Object.entries(config.fields).forEach(([field, fieldConfig]) => {
    const fallback = fieldConfig.fallback ?? null

    if (fieldConfig.active === false) {
      values[field] = fallback
      return
    }

    const configuredIndex = Number(fieldConfig.index ?? 1)
    const zeroBasedIndex =
      Number.isFinite(configuredIndex) && configuredIndex > 0
        ? Math.floor(configuredIndex) - 1
        : 0

    for (const selector of fieldConfig.selectors || []) {
      const matches = $(selector)
      if (!matches.length) continue

      const element = matches.eq(zeroBasedIndex)
      if (!element.length) continue

      const attribute = fieldConfig.attribute || 'text'
      const raw =
        attribute === 'text'
          ? element.text()
          : attribute === 'html'
            ? element.html()
            : element.attr(attribute)

      const rawValue = String(raw ?? '').trim()
      if (!rawValue) continue

      const matched = applyRegex(rawValue, fieldConfig.regex)
      if (!matched) continue

      values[field] = applyTransform(matched, fieldConfig.transform, baseUrl)
      return
    }

    values[field] = fallback
  })

  return values
}
