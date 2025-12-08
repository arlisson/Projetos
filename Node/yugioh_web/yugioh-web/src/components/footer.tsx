// src/components/layout/Footer.tsx

interface FooterProps {
  appName?: string
}

export function Footer({ appName = 'YU-GI-OH! Manager' }: FooterProps) {
  const year = new Date().getFullYear()

  return (
    <footer className="app-footer">
      <span className="app-footer-main">
        © {year} {appName}
      </span>

      <span className="app-footer-secondary">
        Dados financeiros e de preços são estimativos e dependem de scraping e cadastro correto.
      </span>
    </footer>
  )
}
