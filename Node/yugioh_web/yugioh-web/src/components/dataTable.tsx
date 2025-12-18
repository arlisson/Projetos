// src/components/ui/DataTable.tsx
import React, { useMemo, useState } from 'react'




export type Column<T> = {
  key: keyof T | string
  label: string
  width?: string
  render?: (value: any, row: T, rowIndex: number) => React.ReactNode
  sum?: boolean
  formatSum?: (sum: number) => React.ReactNode
  sortable?: boolean
  valueGetter?: (row: T) => any
}

export interface DataTableProps<T> {
  columns: Column<T>[]
  data: T[]
  rowKey?: keyof T | ((row: T, index: number) => string | number)
  emptyMessage?: string
  className?: string
  /** Callback ao clicar em uma linha */
  onRowClick?: (row: T, index: number) => void
}

type SortDirection = 'asc' | 'desc' | null

interface SortState {
  key: string | null
  direction: SortDirection
}

export function DataTable<T>({
  columns,
  data,
  rowKey,
  emptyMessage = 'Nenhum registro encontrado.',
  className,
  onRowClick,
}: DataTableProps<T>) {
  const [sortState, setSortState] = useState<SortState>({
    key: null,
    direction: null,
  })

  const getRowKey = (row: T, index: number) => {
    if (typeof rowKey === 'function') {
      return rowKey(row, index)
    }
    if (typeof rowKey === 'string') {
      const value = (row as any)[rowKey]
      if (value !== undefined && value !== null) {
        return value
      }
    }
    return index
  }

  const getCellRaw = (row: T, col: Column<T>) => {
    if (col.valueGetter) return col.valueGetter(row)
    if (typeof col.key === 'string') return (row as any)[col.key]
    return (row as any)[col.key as keyof T]
  }

  const sums: Record<string, number> = {}
  const hasAnySum = columns.some((c) => c.sum)

  if (hasAnySum && data.length > 0) {
    for (const col of columns) {
      if (!col.sum) continue
      const key = String(col.key)
      let total = 0

      for (const row of data) {
        const raw = getCellRaw(row, col)
        const num =
          typeof raw === 'number'
            ? raw
            : raw != null && raw !== ''
            ? Number(
                String(raw)
                  .replace('.', '')
                  .replace(',', '.'),
              )
            : 0

        if (!Number.isNaN(num)) total += num
      }

      sums[key] = total
    }
  }

  const sortedData = useMemo(() => {
    const { key, direction } = sortState
    if (!key || !direction) return data

    const dirFactor = direction === 'asc' ? 1 : -1
    const col = columns.find((c) => String(c.key) === key)
    if (!col) return data

    return [...data].sort((a, b) => {
      const va = getCellRaw(a, col)
      const vb = getCellRaw(b, col)

      if (va == null && vb == null) return 0
      if (va == null) return 1 * dirFactor
      if (vb == null) return -1 * dirFactor

      const na =
        typeof va === 'number'
          ? va
          : Number(
              String(va)
                .replace('.', '')
                .replace(',', '.'),
            )
      const nb =
        typeof vb === 'number'
          ? vb
          : Number(
              String(vb)
                .replace('.', '')
                .replace(',', '.'),
            )

      if (!Number.isNaN(na) && !Number.isNaN(nb)) {
        if (na < nb) return -1 * dirFactor
        if (na > nb) return 1 * dirFactor
        return 0
      }

      const sa = String(va).toUpperCase()
      const sb = String(vb).toUpperCase()
      if (sa < sb) return -1 * dirFactor
      if (sa > sb) return 1 * dirFactor
      return 0
    })
  }, [data, sortState, columns])

  const handleHeaderClick = (col: Column<T>) => {
    const colKey = String(col.key)
    const sortable = col.sortable !== false
    if (!sortable) return

    setSortState((prev) => {
      if (prev.key !== colKey) {
        return { key: colKey, direction: 'asc' }
      }
      if (prev.direction === 'asc') {
        return { key: colKey, direction: 'desc' }
      }
      if (prev.direction === 'desc') {
        return { key: null, direction: null }
      }
      return { key: colKey, direction: 'asc' }
    })
  }

  const getSortIndicator = (col: Column<T>): string | null => {
    const colKey = String(col.key)
    if (sortState.key !== colKey) return null
    if (sortState.direction === 'asc') return '▲'
    if (sortState.direction === 'desc') return '▼'
    return null
  }

  return (
    <div className={`table-wrapper ${className ?? ''}`}>
      <table className="table">
        <thead>
          {hasAnySum && (
            <tr className="table-summary-row">
              {columns.map((col) => {
                const key = String(col.key)
                const sumValue = sums[key] ?? 0

                return (
                  <th
                    key={key}
                    style={col.width ? { width: col.width } : undefined}
                  >
                    {col.sum
                      ? col.formatSum
                        ? col.formatSum(sumValue)
                        : sumValue.toFixed(2)
                      : ''}
                  </th>
                )
              })}
            </tr>
          )}

          <tr>
            {columns.map((col) => {
              const sortable = col.sortable !== false
              const indicator = getSortIndicator(col)

              return (
                <th
                  key={String(col.key)}
                  style={col.width ? { width: col.width } : undefined}
                  className={sortable ? 'table-header-sortable' : undefined}
                  onClick={() => handleHeaderClick(col)}
                >
                  <span className="table-header-label">
                    {col.label}
                    {indicator && (
                      <span className="table-header-indicator">
                        {indicator}
                      </span>
                    )}
                  </span>
                </th>
              )
            })}
          </tr>
        </thead>

        <tbody>
          {sortedData.length === 0 && (
            <tr>
              <td colSpan={columns.length} className="table-empty">
                {emptyMessage}
              </td>
            </tr>
          )}

          {sortedData.map((row, rowIndex) => (
            <tr
              key={getRowKey(row, rowIndex)}
              className={onRowClick ? 'table-row-clickable' : undefined}
              onClick={onRowClick ? () => onRowClick(row, rowIndex) : undefined}
            >
              {columns.map((col) => {
                const rawValue = getCellRaw(row, col)

                return (
                  <td key={String(col.key)}>
                    {col.render
                      ? col.render(rawValue, row, rowIndex)
                      : String(
                          rawValue === undefined || rawValue === null
                            ? ''
                            : rawValue,
                        )}
                  </td>
                )
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
