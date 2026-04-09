import { useMemo } from "react";
import type { FinancialRow } from "../api/types";
import { formatInt, formatUsd, formatUsdPerShare } from "../utils/format";

type Props = { rows: FinancialRow[] };

export function PublicCompanyFinancials({ rows }: Props) {
  const displayRows = useMemo(
    () =>
      [...rows]
        .sort((a, b) => String(b.date ?? "").localeCompare(String(a.date ?? "")))
        .slice(0, 12),
    [rows],
  );

  return (
    <div className="card">
      <h2 className="section-title">Financials</h2>
      <div className="table-wrap">
        <table className="data">
          <thead>
            <tr>
              <th>Date</th>
              <th>Close</th>
              <th>Volume</th>
              <th>Shares out.</th>
              <th>Free cash flow</th>
            </tr>
          </thead>
          <tbody>
            {displayRows.map((r, i) => (
              <tr key={`${r.date}-${i}`}>
                <td>{r.date ?? "—"}</td>
                <td>{formatUsdPerShare(r.close ?? null)}</td>
                <td>{formatInt(r.volume ?? null)}</td>
                <td>{formatInt(r.sharesOutstanding ?? null)}</td>
                <td>{formatUsd(r.freeCashFlow ?? null)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
