import { fetchStatistics } from "@/lib/api";
import { ErrorState } from "@/components/ui/error-state";
import SpendChart from "@/components/charts/spend-chart";
import { KpiCards, type KpiItem } from "@/components/ui/kpi-cards";
import { formatMoney, formatNumber } from "@/lib/format";
import type { Statistic } from "@/types";

export const dynamic = "force-dynamic";

export default async function AnalyticsPage() {
  let statistics;
  try {
    statistics = await fetchStatistics();
  } catch {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-semibold">Аналитика</h1>
        <div className="mt-6">
          <ErrorState title="Сервер недоступен" />
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
      revenue: acc.revenue + s.revenue,
    }),
    { impressions: 0, clicks: 0, spend: 0, conversions: 0, revenue: 0 }
  );

  const ctr = totals.impressions ? (totals.clicks / totals.impressions) * 100 : 0;
  const cpc = totals.clicks ? totals.spend / totals.clicks : 0;
  const cpa = totals.conversions ? totals.spend / totals.conversions : 0;
  const roas = totals.spend ? totals.revenue / totals.spend : 0;

  const kpi: KpiItem[] = [
    { label: "Показы", value: formatNumber(totals.impressions) },
    { label: "Клики", value: formatNumber(totals.clicks), hint: `CTR: ${ctr.toFixed(2)}%` },
    { label: "CPC", value: formatMoney(cpc) },
    { label: "ROAS", value: roas ? `${roas.toFixed(2)}×` : "—" },
  ];

  return (
    <div className="p-8">
      <h1 className="text-2xl font-semibold">Аналитика</h1>
      <p className="mt-1 text-sm text-gray-500">
        Динамика и ключевые показатели
      </p>

      <div className="mt-6 space-y-6">
        <KpiCards items={kpi} />

        <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
          <h2 className="text-sm font-semibold text-gray-900">Расход по дням</h2>
          <div className="mt-4">
            <SpendChart statistics={statistics} />
          </div>
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
            <p className="text-sm text-gray-500">Расход за период</p>
            <p className="mt-2 text-2xl font-semibold">
              {formatMoney(totals.spend)}
            </p>
          </div>
          <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
            <p className="text-sm text-gray-500">Конверсии / CPA</p>
            <p className="mt-2 text-2xl font-semibold">
              {formatNumber(totals.conversions)}
              <span className="ml-2 text-sm text-gray-400">
                CPA: {formatMoney(cpa)}
              </span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
