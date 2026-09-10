import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8">
      <h1 className="text-4xl font-bold">
        Агент контекстной рекламы
      </h1>
      <p className="mt-4 text-lg text-gray-600">
        Автоматизация Яндекс.Директ (eLama) и VK Ads
      </p>
      <div className="mt-8 flex gap-4">
        <Link
          href="/dashboard"
          className="rounded-lg bg-blue-600 px-6 py-3 font-medium text-white hover:bg-blue-700"
        >
          Дашборд
        </Link>
        <Link
          href="/campaigns"
          className="rounded-lg border border-gray-300 px-6 py-3 font-medium hover:bg-gray-100"
        >
          Кампании
        </Link>
      </div>
    </main>
  );
}