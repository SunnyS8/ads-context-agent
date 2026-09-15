import type { CampaignStatus } from "@/types";

const STYLES: Record<CampaignStatus, { label: string; className: string }> = {
  active: {
    label: "Активна",
    className: "bg-emerald-50 text-emerald-700 ring-emerald-600/20",
  },
  paused: {
    label: "На паузе",
    className: "bg-amber-50 text-amber-700 ring-amber-600/20",
  },
  archived: {
    label: "Архив",
    className: "bg-gray-100 text-gray-600 ring-gray-500/20",
  },
};

export function StatusBadge({ status }: { status: CampaignStatus }) {
  const style = STYLES[status] ?? STYLES.archived;
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ring-1 ring-inset ${style.className}`}
    >
      {style.label}
    </span>
  );
}
