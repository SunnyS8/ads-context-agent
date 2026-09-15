import { fetchCampaigns, fetchStatistics } from "@/lib/api";
import { StatusBadge } from "@/components/ui/status-badge";
import { ErrorState } from "@/components/ui/error-state";
import { formatMoney, formatNumber } from "@/lib/format";
import type { Statistic } from "@/types";

export const dynamic = "force-dynamic";

export default async function CampaignsPage() {
  let campaigns, statistics;
  try {
    [campaigns, statistics] = await Promise.all([
      fetchCampaigns(),
      fetchStatistics(),
    ]);
  } catch {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-semibold">Кампании</h1>
        <div className="mt-6">
          <ErrorState title="Сервер недоступен" />
        </div>
      </div>
    );
  }

  const statsByCampaign = statistics.reduce<Record<number, Statistic[]>>(
    (acc, s) => {
      (acc[s.campaign_id] ??= []).push(s);
      return acc;
    },
    {}
  );

  return (
    <div className="p-8">
      <h1 className="text-2xl font-semibold">Кампании</h1>
      <p className="mt-1 text-sm text-gray-500">
        Показатели за всю доступную историю статистики
      </p>

      <div className="mt-6 rounded-xl border border-gray-200 bg-white shadow-sm">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-xs uppercase text-gray-400">
              <th className="px-5 py-3 font-medium">Кампания</th>
              <th className="px-5 py-3 font-medium">Статус</th>
              <th className="px-5 py-3 text-right font-medium">Показы</th>
              <th className="px-5 py-3 text-right font-medium">Клики</th>
              <th className="px-5 py-3 text-right font-medium">CTR</th>
              <th className="px-5 py-3 text-right font-medium">Расход</th>
              <th className="px-5 py-3 text-right font-medium">Конверсии</th>
              <th className="px-5 py-3 text-right font-medium">CPA</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {campaigns.map((c) => {
              const stats = statsByCampaign[c.id] ?? [];
              const impressions = stats.reduce((s, x) => s + x.impressions, 0);
              const clicks = stats.reduce((s, x) => s + x.clicks, 0);
              const spend = stats.reduce((s, x) => s + x.spend, 0);
              const conversions = stats.reduce((s, x) => s + x.conversions, 0);
              const ctr = impressions ? (clicks / impressions) * 100 : 0;
              const cpa = conversions ? spend / conversions : 0;

              return (
                <tr key={c.id} className="hover:bg-gray-50">
                  <td className="px-5 py-3">
                    <p className="font-medium text-gray-900">{c.name}</p>
                    <p className="text-xs text-gray-400">
                      {c.platform === "elama" ? "Яндекс.Директ" : c.platform}
                    </p>
                  </td>
                  <td className="px-5 py-3">
                    <StatusBadge status={c.status} />
                  </td>
                  <td className="px-5 py-3 text-right text-gray-900">
                    {formatNumber(impressions)}
                  </td>
                  <td className="px-5 py-3 text-right text-gray-900">
                    {formatNumber(clicks)}
                  </td>
                  <td className="px-5 py-3 text-right text-gray-900">
                    {ctr.toFixed(2)}%
                  </td>
                  <td className="px-5 py-3 text-right text-gray-900">
                    {formatMoney(spend)}
                  </td>
                  <td className="px-5 py-3 text-right text-gray-900">
                    {formatNumber(conversions)}
                  </td>
                  <td className="px-5 py-3 text-right text-gray-900">
                    {formatMoney(cpa)}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
        {campaigns.length === 0 ? (
          <p className="px-5 py-8 text-center text-sm text-gray-500">
            Кампаний пока нет. Запустите start_local.bat — он добавит демо-данные.
          </p>
        ) : null}
      </div>
    </div>
  );
}
