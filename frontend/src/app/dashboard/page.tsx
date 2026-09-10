import { Suspense } from "react";
import { fetchCampaigns } from "@/lib/api";
import { MetricsCards } from "@/components/ui/metrics-cards";

export const dynamic = "force-dynamic";

export default async function DashboardPage() {
  const campaigns = await fetchCampaigns();

  return (
    <div className="p-8">
      <h1 className="text-2xl font-semibold">Дашборд</h1>
      <p className="mt-1 text-sm text-gray-500">
        Общая сводка по всем кампаниям
      </p>
      <Suspense fallback={<p className="mt-4">Загрузка...</p>}>
        <MetricsCards campaigns={campaigns} />
      </Suspense>
    </div>
  );
}