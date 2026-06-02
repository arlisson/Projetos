import type * as cheerio from 'cheerio'

export type ScraperSite = 'mypcards' | 'ligayugioh'

export type ScraperAttribute = 'text' | 'html' | string

export type ScraperTransform =
  | 'text'
  | 'number'
  | 'currency-brl'
  | 'absolute-url'

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

export interface FieldExtractionResult {
  field: string
  found: boolean
  selectorUsed: string | null
  rawValue: string | null
  normalizedValue: string | number | null
  fallbackApplied: boolean
  indexUsed: number | null
  matchCount: number
  error: string | null
}

export interface ConfiguredExtractionResult {
  site: ScraperSite
  values: Record<string, string | number | null>
  diagnostics: Record<string, FieldExtractionResult>
}

export interface FieldOccurrenceResult {
  occurrence: number
  selectorUsed: string
  rawValue: string | null
  normalizedValue: string | number | null
  error: string | null
}

const VALID_TRANSFORMS = new Set<ScraperTransform>([
  'text',
  'number',
  'currency-brl',
  'absolute-url',
])

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

  const pattern = new RegExp(regex)
  const match = value.match(pattern)
  if (!match) return ''

  return (match[1] ?? match[0] ?? '').trim()
}

function applyTransform(
  value: string,
  transform: ScraperTransform | undefined,
  baseUrl: string,
): string | number {
  const selected = transform || 'text'

  if (!VALID_TRANSFORMS.has(selected)) {
    throw new Error(`Transformacao nao permitida: ${selected}`)
  }

  if (selected === 'currency-brl') return normalizeCurrencyBrl(value)
  if (selected === 'number') return normalizeNumber(value)
  if (selected === 'absolute-url') return toAbsoluteUrl(baseUrl, value)

  return value.trim()
}

export function extractField(
  $: cheerio.CheerioAPI,
  field: string,
  config: ScraperFieldConfig,
  baseUrl: string,
): FieldExtractionResult {
  const fallback = config.fallback ?? null

  if (config.active === false) {
    return {
      field,
      found: false,
      selectorUsed: null,
      rawValue: null,
      normalizedValue: fallback,
      fallbackApplied: fallback !== null,
      indexUsed: null,
      matchCount: 0,
      error: 'Campo inativo',
    }
  }

  const selectors = Array.isArray(config.selectors)
    ? config.selectors.map((selector) => selector.trim()).filter(Boolean)
    : []

  if (selectors.length === 0) {
    return {
      field,
      found: false,
      selectorUsed: null,
      rawValue: null,
      normalizedValue: fallback,
      fallbackApplied: fallback !== null,
      indexUsed: null,
      matchCount: 0,
      error: 'Nenhum seletor configurado',
    }
  }

  const configuredIndex = Number(config.index ?? 1)
  const zeroBasedIndex =
    Number.isFinite(configuredIndex) && configuredIndex > 0
      ? Math.floor(configuredIndex) - 1
      : 0

  for (const selector of selectors) {
    try {
      const matches = $(selector)
      const matchCount = matches.length
      if (!matchCount) continue

      const element = matches.eq(zeroBasedIndex)
      if (!element.length) {
        return {
          field,
          found: false,
          selectorUsed: selector,
          rawValue: null,
          normalizedValue: fallback,
          fallbackApplied: fallback !== null,
          indexUsed: zeroBasedIndex + 1,
          matchCount,
          error: `Indice ${zeroBasedIndex + 1} fora do total encontrado (${matchCount})`,
        }
      }

      const attribute = config.attribute || 'text'
      const raw =
        attribute === 'text'
          ? element.text()
          : attribute === 'html'
            ? element.html()
            : element.attr(attribute)

      const rawValue = String(raw ?? '').trim()
      if (!rawValue) continue

      const matchedValue = applyRegex(rawValue, config.regex)
      if (!matchedValue) continue

      const normalizedValue = applyTransform(
        matchedValue,
        config.transform,
        baseUrl,
      )

      return {
        field,
        found: true,
        selectorUsed: selector,
        rawValue,
        normalizedValue,
        fallbackApplied: false,
        indexUsed: zeroBasedIndex + 1,
        matchCount,
        error: null,
      }
    } catch (error) {
      return {
        field,
        found: false,
        selectorUsed: selector,
        rawValue: null,
        normalizedValue: fallback,
        fallbackApplied: fallback !== null,
        indexUsed: zeroBasedIndex + 1,
        matchCount: 0,
        error: String(error),
      }
    }
  }

  return {
    field,
    found: false,
    selectorUsed: null,
    rawValue: null,
    normalizedValue: fallback,
    fallbackApplied: fallback !== null,
    indexUsed: zeroBasedIndex + 1,
    matchCount: 0,
    error: 'Nenhum valor encontrado',
  }
}

export function extractConfiguredData(
  $: cheerio.CheerioAPI,
  config: ScraperSiteConfig,
  baseUrl: string,
): ConfiguredExtractionResult {
  const diagnostics: Record<string, FieldExtractionResult> = {}
  const values: Record<string, string | number | null> = {}

  Object.entries(config.fields).forEach(([field, fieldConfig]) => {
    const result = extractField($, field, fieldConfig, baseUrl)
    diagnostics[field] = result
    values[field] = result.normalizedValue
  })

  return {
    site: config.site,
    values,
    diagnostics,
  }
}

export function listFieldOccurrences(
  $: cheerio.CheerioAPI,
  config: ScraperFieldConfig,
  baseUrl: string,
): FieldOccurrenceResult[] {
  const selectors = Array.isArray(config.selectors)
    ? config.selectors.map((selector) => selector.trim()).filter(Boolean)
    : []

  if (config.active === false || selectors.length === 0) return []

  const results: FieldOccurrenceResult[] = []

  for (const selector of selectors) {
    const matches = $(selector)
    if (!matches.length) continue

    matches.each((index, element) => {
      try {
        const current = $(element)
        const attribute = config.attribute || 'text'
        const raw =
          attribute === 'text'
            ? current.text()
            : attribute === 'html'
              ? current.html()
              : current.attr(attribute)

        const rawValue = String(raw ?? '').trim()
        const matchedValue = applyRegex(rawValue, config.regex)
        const normalizedValue = matchedValue
          ? applyTransform(matchedValue, config.transform, baseUrl)
          : null

        results.push({
          occurrence: index + 1,
          selectorUsed: selector,
          rawValue: rawValue || null,
          normalizedValue,
          error: rawValue ? null : 'Valor vazio',
        })
      } catch (error) {
        results.push({
          occurrence: index + 1,
          selectorUsed: selector,
          rawValue: null,
          normalizedValue: null,
          error: String(error),
        })
      }
    })

    if (results.length > 0) break
  }

  return results
}

export function validateScraperConfig(config: ScraperSiteConfig): string[] {
  const errors: string[] = []

  if (!config.site || !['mypcards', 'ligayugioh'].includes(config.site)) {
    errors.push('Site invalido.')
  }

  if (!config.fields || typeof config.fields !== 'object') {
    errors.push('Campos da configuracao invalidos.')
    return errors
  }

  Object.entries(config.fields).forEach(([field, fieldConfig]) => {
    if (!Array.isArray(fieldConfig.selectors) || fieldConfig.selectors.length === 0) {
      errors.push(`Campo ${field}: informe ao menos um seletor.`)
    }

    fieldConfig.selectors.forEach((selector) => {
      if (!String(selector || '').trim()) {
        errors.push(`Campo ${field}: seletor vazio.`)
      }
    })

    if (!fieldConfig.attribute) {
      errors.push(`Campo ${field}: atributo obrigatorio.`)
    }

    if (fieldConfig.index !== undefined && fieldConfig.index !== null) {
      const index = Number(fieldConfig.index)
      if (!Number.isFinite(index) || index < 1) {
        errors.push(`Campo ${field}: indice deve ser maior ou igual a 1.`)
      }
    }

    if (fieldConfig.transform && !VALID_TRANSFORMS.has(fieldConfig.transform)) {
      errors.push(`Campo ${field}: transformacao invalida.`)
    }

    if (fieldConfig.regex) {
      if (fieldConfig.regex.length > 250) {
        errors.push(`Campo ${field}: regex muito longa.`)
      }

      try {
        new RegExp(fieldConfig.regex)
      } catch {
        errors.push(`Campo ${field}: regex invalida.`)
      }
    }
  })

  return errors
}
