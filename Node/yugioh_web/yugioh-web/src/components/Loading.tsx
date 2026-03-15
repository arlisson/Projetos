interface LoadingProps {
  message?: string
  fullScreen?: boolean
}

export function Loading({
  message = 'Buscando cartas da coleção...',
  fullScreen = false,
}: LoadingProps) {
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: fullScreen ? '100vh' : '160px',
        width: '100%',
      }}
    >
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '0.9rem',
          padding: '1.25rem 1.5rem',
          borderRadius: '16px',
          border: '1px solid rgba(255,255,255,0.08)',
          background: 'rgba(255,255,255,0.03)',
          boxShadow: '0 10px 30px rgba(0,0,0,0.18)',
          minWidth: '240px',
        }}
      >
        <div
          style={{
            width: '42px',
            height: '42px',
            borderRadius: '999px',
            border: '4px solid rgba(255,255,255,0.15)',
            borderTopColor: 'rgba(87,197,234,1)',
            animation: 'spin 0.9s linear infinite',
          }}
        />

        <div
          style={{
            fontSize: '0.95rem',
            color: 'var(--text-secondary, #ade5f2)',
            textAlign: 'center',
          }}
        >
          {message}
        </div>

        <style>
          {`
            @keyframes spin {
              from { transform: rotate(0deg); }
              to { transform: rotate(360deg); }
            }
          `}
        </style>
      </div>
    </div>
  )
}