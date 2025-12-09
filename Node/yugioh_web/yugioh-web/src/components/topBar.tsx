// src/components/layout/Topbar.tsx
import { useNavigate } from 'react-router-dom'

type MenuItem = {
  label: string
  path: string
}

type MenuGroup = {
  label: string
  items: MenuItem[]
}

interface TopbarProps {
  pageTitle?: string
}

export function Topbar({ pageTitle = 'YU-GI-OH! Manager' }: TopbarProps) {
  const navigate = useNavigate()

  const menuGroups: MenuGroup[] = [
    {
      label: 'Cartas',
      items: [
        { label: 'Cadastrar Cartas', path:'/cartas/cadastrar' },
        { label: 'Listar Cartas', path: '/cartas/listar' },
        {
          label: 'Cadastrar Cartas de Coleção',
          path: 'cartas/colecao/cadastrar',
        },
      ],
    },
    {
      label: 'Produtos',
      items: [
        { label: 'Cadastrar Produtos', path: '/produtos/cadastrar' },
        { label: 'Listar Produtos', path: '/produtos/listar' },
      ],
    },
    {
      label: 'Gestão',
      items: [
        { label: 'Configurações', path: '/configuracoes' },
        { label: 'Banco de dados', path: '/banco-dados' },
        { label: 'Logs / diagnósticos', path: '/logs' },
      ],
    },
  ]

  return (
    <header className="topbar">
      <div className="topbar-left">
        
        <span className="app-title">{pageTitle}</span>
        <span className="app-title">
          <button
            className="dropdown-item"
            key={'home'}
            onClick={() => navigate('/')}
          >
            Home
          </button>
        </span>
      </div>

      <nav className="topbar-nav">
        {menuGroups.map((group) => (
          <div className="topbar-nav-item" key={group.label}>
            <button className="topbar-nav-button">
              {group.label} <span>▾</span>
            </button>

            <div className="dropdown-menu">
              {group.items.map((item) => (
                <button
                  className="dropdown-item"
                  key={item.path}
                  onClick={() => navigate(item.path)}
                >
                  {item.label}
                </button>
              ))}
            </div>
          </div>
        ))}
      </nav>
    </header>
  )
}
