import { useEffect, useMemo, useState } from 'react'
import { Topbar } from '../../components/topBar'
import { Footer } from '../../components/footer'
import { Button } from '../../components/botao'
import { Loading } from '../../components/Loading'
import { PageHelpButton } from '../../components/PageHelpButton'
import {
  getEffectiveScraperConfig,
  getScraperSites,
  listScraperConfigHistory,
  restoreDefaultScraperConfig,
  restoreScraperConfigVersion,
  saveScraperConfig,
  testScraperFieldOccurrences,
  testScraperConfig,
  type ScraperConfigHistoryItem,
  type ScraperFieldOccurrencesResult,
  type ScraperSelectorTestResult,
} from '../../services/scraperConfigStorage'
import type {
  ScraperFieldConfig,
  ScraperSite,
  ScraperSiteConfig,
  ScraperTransform,
} from '../../../scraping/configurableExtractor'

const TRANSFORMS: ScraperTransform[] = [
  'text',
  'number',
  'currency-brl',
  'absolute-url',
]

const SITE_LABELS: Record<ScraperSite, string> = {
  mypcards: 'MYPCards',
  ligayugioh: 'LigaYugioh',
}

function cloneConfig(config: ScraperSiteConfig): ScraperSiteConfig {
  return JSON.parse(JSON.stringify(config)) as ScraperSiteConfig
}

function formatDate(value: string) {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleString('pt-BR')
}

function FieldInput({
  label,
  value,
  onChange,
}: {
  label: string
  value: string
  onChange: (value: string) => void
}) {
  return (
    <label className="scraper-config-label">
      <span>{label}</span>
      <input
        className="form-field-input"
        value={value}
        onChange={(event) => onChange(event.target.value)}
      />
    </label>
  )
}

export function ScraperConfigs() {
  const sites = useMemo(() => getScraperSites(), [])
  const [site, setSite] = useState<ScraperSite>('mypcards')
  const [config, setConfig] = useState<ScraperSiteConfig | null>(null)
  const [history, setHistory] = useState<ScraperConfigHistoryItem[]>([])
  const [testUrl, setTestUrl] = useState('')
  const [testResult, setTestResult] = useState<ScraperSelectorTestResult | null>(
    null,
  )
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [testing, setTesting] = useState(false)
  const [testingField, setTestingField] = useState<string | null>(null)
  const [fieldOccurrences, setFieldOccurrences] = useState<
    Record<string, ScraperFieldOccurrencesResult>
  >({})
  const [expandedOccurrences, setExpandedOccurrences] = useState<
    Record<string, boolean>
  >({})

  async function loadSite(nextSite = site) {
    setLoading(true)
    setTestResult(null)

    try {
      const [effective, versions] = await Promise.all([
        getEffectiveScraperConfig(nextSite),
        listScraperConfigHistory(nextSite),
      ])
      setConfig(cloneConfig(effective))
      setHistory(versions)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void loadSite(site)
  }, [site])

  function updateField(
    fieldName: string,
    updater: (field: ScraperFieldConfig) => ScraperFieldConfig,
  ) {
    setConfig((current) => {
      if (!current) return current
      const next = cloneConfig(current)
      next.fields[fieldName] = updater(next.fields[fieldName])
      return next
    })
  }

  async function handleSave() {
    if (!config || saving) return

    setSaving(true)
    try {
      const result = await saveScraperConfig(config)
      if (!result.ok) {
        alert(result.errors.join('\n'))
        return
      }

      alert('Configuracao salva com sucesso.')
      await loadSite(config.site)
    } finally {
      setSaving(false)
    }
  }

  async function handleTest() {
    if (!config || testing) return
    if (!testUrl.trim()) {
      alert('Informe uma URL para testar.')
      return
    }

    setTesting(true)
    try {
      const result = await testScraperConfig(config, testUrl.trim())
      setTestResult(result)
    } finally {
      setTesting(false)
    }
  }

  async function handleTestField(fieldName: string) {
    if (!config || testingField) return
    if (!testUrl.trim()) {
      alert('Informe uma URL no teste de seletor antes de listar ocorrencias.')
      return
    }

    setTestingField(fieldName)
    try {
      const result = await testScraperFieldOccurrences(
        config,
        fieldName,
        testUrl.trim(),
      )
      setFieldOccurrences((current) => ({
        ...current,
        [fieldName]: result,
      }))
    } finally {
      setTestingField(null)
    }
  }

  async function handleRestoreDefault() {
    if (!config) return
    const confirmed = window.confirm(
      `Restaurar a configuracao padrao de ${SITE_LABELS[config.site]}?`,
    )
    if (!confirmed) return

    await restoreDefaultScraperConfig(config.site)
    await loadSite(config.site)
  }

  async function handleRestoreHistory(item: ScraperConfigHistoryItem) {
    const confirmed = window.confirm('Restaurar esta versao da configuracao?')
    if (!confirmed) return

    const result = await restoreScraperConfigVersion(item)
    if (!result.ok) {
      alert(result.errors.join('\n'))
      return
    }

    await loadSite(item.site)
  }

  return (
    <div className="app-shell">
      <Topbar pageTitle="Configuracao de scrapers" />

      <main className="form-page-content">
        <section className="form-page-left" style={{ maxWidth: '100%' }}>
          <div className="section-header">
            <div>
              <h2 className="section-title section-title-with-help">
                Seletores de scraping
                <PageHelpButton
                  configKey="gestao.scrapers"
                  fallbackTitle="Como configurar scrapers"
                />
              </h2>
              <p className="section-subtitle">
                Ajuste os seletores usados para extrair dados dos sites.
              </p>
            </div>

            <div className="scraper-config-site-select">
              <label className="scraper-config-label">
                <span>Site</span>
                <select
                  className="form-field-input"
                  value={site}
                  onChange={(event) => setSite(event.target.value as ScraperSite)}
                >
                  {sites.map((item) => (
                    <option key={item} value={item}>
                      {SITE_LABELS[item]}
                    </option>
                  ))}
                </select>
              </label>
            </div>
          </div>

          {loading || !config ? (
            <Loading message="Carregando configuracao..." />
          ) : (
            <>
              <div className="scraper-config-toolbar">
                <Button type="button" onClick={handleSave} disabled={saving}>
                  {saving ? 'Salvando...' : 'Salvar configuracao'}
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={handleRestoreDefault}
                  disabled={saving}
                >
                  Restaurar padrao
                </Button>
              </div>

              <div className="scraper-config-grid">
                {Object.entries(config.fields).map(([fieldName, field]) => (
                  <div
                    className={[
                      'scraper-config-card',
                      expandedOccurrences[fieldName]
                        ? 'scraper-config-card-expanded'
                        : '',
                    ]
                      .filter(Boolean)
                      .join(' ')}
                    key={fieldName}
                  >
                    <div className="scraper-config-card-header">
                      <strong>{fieldName}</strong>
                      <label className="scraper-config-toggle">
                        <input
                          type="checkbox"
                          checked={field.active !== false}
                          onChange={(event) =>
                            updateField(fieldName, (current) => ({
                              ...current,
                              active: event.target.checked,
                            }))
                          }
                        />
                        <span>Ativo</span>
                      </label>
                    </div>

                    <label className="scraper-config-label">
                      <span>Seletores CSS, um por linha</span>
                      <textarea
                        className="scraper-config-textarea"
                        value={(field.selectors || []).join('\n')}
                        onChange={(event) =>
                          updateField(fieldName, (current) => ({
                            ...current,
                            selectors: event.target.value
                              .split('\n')
                              .map((selector) => selector.trim())
                              .filter(Boolean),
                          }))
                        }
                      />
                    </label>

                    <div className="scraper-config-row">
                      <FieldInput
                        label="Atributo"
                        value={field.attribute || 'text'}
                        onChange={(value) =>
                          updateField(fieldName, (current) => ({
                            ...current,
                            attribute: value,
                          }))
                        }
                      />

                      <label className="scraper-config-label">
                        <span>Transformacao</span>
                        <select
                          className="form-field-input"
                          value={field.transform || 'text'}
                          onChange={(event) =>
                            updateField(fieldName, (current) => ({
                              ...current,
                              transform: event.target.value as ScraperTransform,
                            }))
                          }
                        >
                          {TRANSFORMS.map((transform) => (
                            <option key={transform} value={transform}>
                              {transform}
                            </option>
                          ))}
                        </select>
                      </label>
                    </div>

                    <div className="scraper-config-row scraper-config-row-single">
                      <FieldInput
                        label="Ocorrencia"
                        value={field.index === null || field.index === undefined ? '' : String(field.index)}
                        onChange={(value) =>
                          updateField(fieldName, (current) => ({
                            ...current,
                            index: value ? Number(value) : null,
                          }))
                        }
                      />
                    </div>

                    <div className="scraper-config-row">
                      <FieldInput
                        label="Regex opcional"
                        value={field.regex || ''}
                        onChange={(value) =>
                          updateField(fieldName, (current) => ({
                            ...current,
                            regex: value || null,
                          }))
                        }
                      />

                      <FieldInput
                        label="Fallback"
                        value={String(field.fallback ?? '')}
                        onChange={(value) =>
                          updateField(fieldName, (current) => ({
                            ...current,
                            fallback: value || null,
                          }))
                        }
                      />
                    </div>

                    <div className="scraper-config-card-actions">
                      <Button
                        type="button"
                        variant="outline"
                        size="sm"
                        onClick={() => handleTestField(fieldName)}
                        disabled={testingField !== null}
                      >
                        {testingField === fieldName
                          ? 'Listando...'
                          : 'Listar ocorrencias'}
                      </Button>
                    </div>

                    {fieldOccurrences[fieldName] && (
                      <div
                        className={[
                          'scraper-occurrences',
                          expandedOccurrences[fieldName]
                            ? 'scraper-occurrences-expanded'
                            : '',
                        ]
                          .filter(Boolean)
                          .join(' ')}
                      >
                        <div className="scraper-occurrences-header">
                          <strong>{fieldOccurrences[fieldName].message}</strong>

                          {fieldOccurrences[fieldName].occurrences.length > 0 && (
                            <Button
                              type="button"
                              variant="ghost"
                              size="sm"
                              onClick={() =>
                                setExpandedOccurrences((current) => ({
                                  ...current,
                                  [fieldName]: !current[fieldName],
                                }))
                              }
                            >
                              {expandedOccurrences[fieldName]
                                ? 'Recolher'
                                : 'Expandir visualizacao'}
                            </Button>
                          )}
                        </div>

                        {fieldOccurrences[fieldName].occurrences.length > 0 && (
                          <div className="scraper-occurrences-list">
                            {fieldOccurrences[fieldName].occurrences.map(
                              (item) => (
                                <div
                                  className="scraper-occurrence-row"
                                  key={`${item.selectorUsed}-${item.occurrence}`}
                                >
                                  <span className="scraper-occurrence-number">
                                    {item.occurrence}
                                  </span>
                                  <span title={item.rawValue || item.error || ''}>
                                    {item.rawValue || item.error || '-'}
                                  </span>
                                  <span
                                    title={String(item.normalizedValue ?? '')}
                                  >
                                    {String(item.normalizedValue ?? '-')}
                                  </span>
                                </div>
                              ),
                            )}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                ))}
              </div>

              <section className="section-block scraper-config-test">
                <h2 className="section-title">Teste de seletor</h2>

                <div className="scraper-config-test-row">
                  <input
                    className="form-field-input"
                    value={testUrl}
                    onChange={(event) => setTestUrl(event.target.value)}
                    placeholder="URL da carta ou produto"
                  />
                  <Button type="button" onClick={handleTest} disabled={testing}>
                    {testing ? 'Testando...' : 'Testar'}
                  </Button>
                </div>

                {testResult && (
                  <div className="scraper-config-result">
                    <strong>{testResult.message}</strong>
                    <div className="table-wrapper" style={{ marginTop: '1rem' }}>
                      <table className="table">
                        <thead>
                          <tr>
                            <th>Campo</th>
                            <th>Status</th>
                            <th>Seletor</th>
                            <th>Ocorrencia</th>
                            <th>Valor bruto</th>
                            <th>Normalizado</th>
                          </tr>
                        </thead>
                        <tbody>
                          {Object.values(testResult.diagnostics).map((item) => (
                            <tr key={item.field}>
                              <td>{item.field}</td>
                              <td>{item.found ? 'Encontrado' : item.error}</td>
                              <td>{item.selectorUsed || '-'}</td>
                              <td>
                                {item.indexUsed
                                  ? `${item.indexUsed}/${item.matchCount}`
                                  : '-'}
                              </td>
                              <td>{item.rawValue || '-'}</td>
                              <td>{String(item.normalizedValue ?? '-')}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}
              </section>

              <section className="section-block">
                <h2 className="section-title">Historico</h2>

                {history.length === 0 ? (
                  <p className="section-subtitle">
                    Nenhuma alteracao registrada para este site.
                  </p>
                ) : (
                  <div className="scraper-config-history">
                    {history.map((item) => (
                      <div className="scraper-config-history-row" key={item.id}>
                        <span>{formatDate(item.created_at)}</span>
                        <Button
                          type="button"
                          variant="outline"
                          size="sm"
                          onClick={() => handleRestoreHistory(item)}
                        >
                          Restaurar
                        </Button>
                      </div>
                    ))}
                  </div>
                )}
              </section>
            </>
          )}
        </section>
      </main>

      <Footer />
    </div>
  )
}
