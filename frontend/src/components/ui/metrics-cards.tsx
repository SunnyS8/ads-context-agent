import type { Campaign } from "@/types";

function formatMoney(value: number | null | undefined): string {
  if (value === null || value === undefined) return "—";
  return new Intl.NumberFormat("ru-RU", {
    style: "currency",
    currency: "RUB",
    maximumFractionDigits: 0,
  }).format(value);
}

export default function MetricsCards({
  campaigns,
}: {
  campaigns: Campaign[];
}) {
  const active = campaigns.filter((c) => c.status === "active");
  const totalBudget = campaigns.reduce(
    (sum, c) => sum + (c.daily_budget ?? 0),
    0
  );

  return (
    <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-3">
      <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
        <p className="text-sm text-gray-500">Кампаний всего</p>
        <p className="mt-2 text-3xl font-semibold">{campaigns.length}</p>
      </div>
      <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
        <p className="text-sm text-gray-500">Активных</p>
        <p className="mt-2 text-3xl font-semibold">{active.length}</p>
      </div>
      <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
        <p className="text-sm text-gray-500">Дневной бюджет</p>
        <p className="mt-2 text-3xl font-semibold">
          {formatMoney(totalBudget)}
        </p>
      </div>
    </div>
  );
}