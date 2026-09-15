export function ErrorState({ title, hint }: { title: string; hint?: string }) {
  return (
    <div className="rounded-xl border border-amber-200 bg-amber-50 p-6">
      <p className="font-medium text-amber-800">{title}</p>
      {hint ? <p className="mt-1 text-sm text-amber-700">{hint}</p> : null}
      <p className="mt-2 text-xs text-amber-600">
        Бесплатный сервер «засыпает» между запросами: первое открытие может
        занять до минуты. Подожди 30–60 секунд и обнови страницу — данные
        появятся.
      </p>
    </div>
  );
}
