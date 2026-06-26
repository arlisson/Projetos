import { useEffect, useState } from 'react'

type HelpContent = {
  title: string
  intro?: string
  steps?: string[]
  notes?: string[]
}

type HelpConfig = Record<string, HelpContent>

type PageHelpButtonProps = {
  configKey: string
  fallbackTitle: string
}

let cachedHelpConfig: HelpConfig | null = null
let helpConfigPromise: Promise<HelpConfig> | null = null

async function loadHelpConfig(): Promise<HelpConfig> {
  if (cachedHelpConfig) return cachedHelpConfig

  if (!helpConfigPromise) {
    helpConfigPromise = fetch('/help-texts.json', { cache: 'no-store' })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Arquivo de ajuda nao encontrado.')
        }

        return response.json() as Promise<HelpConfig>
      })
      .then((config) => {
        cachedHelpConfig = config
        return config
      })
  }

  return helpConfigPromise
}

export function PageHelpButton({
  configKey,
  fallbackTitle,
}: PageHelpButtonProps) {
  const [content, setContent] = useState<HelpContent | null>(null)
  const [isOpen, setIsOpen] = useState(false)

  useEffect(() => {
    let active = true

    void loadHelpConfig()
      .then((config) => {
        if (!active) return
        setContent(config[configKey] ?? null)
      })
      .catch(() => {
        if (!active) return
        setContent(null)
      })

    return () => {
      active = false
    }
  }, [configKey])

  function closeHelp() {
    setIsOpen(false)
  }

  const title = content?.title || fallbackTitle

  return (
    <>
      <button
        type="button"
        className="page-help-button"
        aria-label={`Ajuda: ${title}`}
        title={`Ajuda: ${title}`}
        onClick={() => setIsOpen(true)}
      >
        ?
      </button>

      {isOpen && (
        <div
          className="help-modal-backdrop"
          role="presentation"
          onMouseDown={closeHelp}
        >
          <div
            className="help-modal-card"
            role="dialog"
            aria-modal="true"
            aria-labelledby={`help-title-${configKey}`}
            onMouseDown={(event) => event.stopPropagation()}
          >
            <div className="help-modal-header">
              <h3 className="help-modal-title" id={`help-title-${configKey}`}>
                {title}
              </h3>
              <button
                type="button"
                className="help-modal-close"
                aria-label="Fechar ajuda"
                onClick={closeHelp}
              >
                x
              </button>
            </div>

            {content ? (
              <div className="help-modal-body">
                {content.intro && <p>{content.intro}</p>}

                {content.steps && content.steps.length > 0 && (
                  <ol>
                    {content.steps.map((step) => (
                      <li key={step}>{step}</li>
                    ))}
                  </ol>
                )}

                {content.notes && content.notes.length > 0 && (
                  <ul>
                    {content.notes.map((note) => (
                      <li key={note}>{note}</li>
                    ))}
                  </ul>
                )}
              </div>
            ) : (
              <p className="help-modal-empty">
                Nenhum texto de ajuda configurado para esta tela.
              </p>
            )}
          </div>
        </div>
      )}
    </>
  )
}
