export interface KpiItem {
  label: string;
  value: string;
  hint?: string;
}

export function KpiCards({ items }: { items: KpiItem[] }) {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {items.map((item) => (
        <div
          key={item.label}
          className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm"
        >
          <p className="text-sm text-gray-500">{item.label}</p>
          <p className="mt-2 text-2xl font-semibold text-gray-900">
            {item.value}
          </p>
          {item.hint ? (
            <p className="mt-1 text-xs text-gray-400">{item.hint}</p>
          ) : null}
        </div>
      ))}
    </div>
  );
}
