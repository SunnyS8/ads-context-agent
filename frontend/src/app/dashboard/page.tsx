import { Suspense } from "react";
import { fetchCampaigns, fetchRecommendations, fetchStatistics } from "@/lib/api";
import { KpiCards, type KpiItem } from "@/components/ui/kpi-cards";
import { StatusBadge } from "@/components/ui/status-badge";
import { ErrorState } from "@/components/ui/error-state";
import SpendChart from "@/components/charts/spend-chart";
import { formatMoney, formatNumber } from "@/lib/format";
import type { Recommendation, Statistic } from "@/types";

export const dynamic = "force-dynamic";

const ACTION_LABELS: Record<string, string> = {
  decrease_bid: "Снизить ставку",
  increase_bid: "Поднять ставку",
  pause_for_review: "Пауза на проверку",
  monitor: "Наблюдение",
};

function RecommendationsList({ items }: { items: Recommendation[] }) {
  if (items.length === 0) {
    return (
      <p className="text-sm text-gray-500">
        Проблем не найдено — все кампании в порядке.
      </p>
    );
  }
  return (
    <ul className="space-y-3">
      {items.slice(0, 5).map((r) => (
        <li
          key={r.id}
          className="rounded-lg border border-gray-100 bg-gray-50 p-4"
        >
          <p className="text-sm font-medium text-gray-900">
            Кампания #{r.campaign_id} · {ACTION_LABELS[r.action] ?? r.action}
          </p>
          <p className="mt-1 text-sm text-gray-600">{r.reason}</p>
        </li>
      ))}
    </ul>
  );
}

export default async function DashboardPage() {
  let campaigns, statistics, recommendations;
  try {
    [campaigns, statistics, recommendations] = await Promise.all([
      fetchCampaigns(),
      fetchStatistics(),
      fetchRecommendations(),
    ]);
  } catch {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-semibold">Дашборд</h1>
        <div className="mt-6">
          <ErrorState
            title="Не удалось загрузить данные"
            hint="Сервер запущен? Окно start_local.bat должно быть открыто."
          />
        </div>
      </div>
    );
  }

  const totals = statistics.reduce(
    (acc, s: Statistic) => ({
      impressions: acc.impressions + s.impressions,
      clicks: acc.clicks + s.clicks,
      spend: acc.spend + s.spend,
      conversions: acc.conversions + s.conversions,
    }),
    { impressions: 0, clicks: 0, spend: 0, conversions: 0 }
  );

  const ctr = totals.impressions ? (totals.clicks / totals.impressions) * 100 : 0;
  const cpa = totals.conversions ? totals.spend / totals.conversions : 0;

  const kpi: KpiItem[] = [
    { label: "Расход за 7 дней", value: formatMoney(totals.spend) },
    {
      label: "Конверсии",
      value: formatNumber(totals.conversions),
      hint: `CPA: ${formatMoney(cpa)}`,
    },
    { label: "Клики", value: formatNumber(totals.clicks), hint: `CTR: ${ctr.toFixed(2)}%` },
    {
      label: "Кампании",
      value: `${campaigns.filter((c) => c.status === "active").length} / ${campaigns.length}`,
      hint: "активные / всего",
    },
  ];

  const activeCampaigns = campaigns.filter((c) => c.status !== "archived");

  return (
    <div className="p-8">
      <h1 className="text-2xl font-semibold">Дашборд</h1>
      <p className="mt-1 text-sm text-gray-500">
        Сводка за последние 7 дней по всем площадкам
      </p>

      <div className="mt-6 space-y-6">
        <KpiCards items={kpi} />

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
            <h2 className="text-sm font-semibold text-gray-900">
              Расход по дням
            </h2>
            <div className="mt-4">
              <SpendChart statistics={statistics} />
            </div>
          </div>

          <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
            <h2 className="text-sm font-semibold text-gray-900">
              Что требует внимания
            </h2>
            <div className="mt-4">
              <RecommendationsList items={recommendations} />
            </div>
          </div>
        </div>

        <div className="rounded-xl border border-gray-200 bg-white shadow-sm">
          <div className="border-b border-gray-100 px-5 py-4">
            <h2 className="text-sm font-semibold text-gray-900">Кампании</h2>
          </div>
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs uppercase text-gray-400">
                <th className="px-5 py-3 font-medium">Название</th>
                <th className="px-5 py-3 font-medium">Площадка</th>
                <th className="px-5 py-3 font-medium">Статус</th>
                <th className="px-5 py-3 text-right font-medium">
                  Дневной бюджет
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {activeCampaigns.map((c) => (
                <tr key={c.id} className="hover:bg-gray-50">
                  <td className="px-5 py-3 font-medium text-gray-900">
                    {c.name}
                  </td>
                  <td className="px-5 py-3 text-gray-600">
                    {c.platform === "elama" ? "Яндекс.Директ" : c.platform}
                  </td>
                  <td className="px-5 py-3">
                    <StatusBadge status={c.status} />
                  </td>
                  <td className="px-5 py-3 text-right text-gray-900">
                    {formatMoney(c.daily_budget)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
