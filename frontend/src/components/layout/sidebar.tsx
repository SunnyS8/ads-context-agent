"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BarChart3, LayoutDashboard, Megaphone, Sparkles } from "lucide-react";

const NAV = [
  { href: "/dashboard", label: "Дашборд", icon: LayoutDashboard },
  { href: "/campaigns", label: "Кампании", icon: Megaphone },
  { href: "/analytics", label: "Аналитика", icon: BarChart3 },
  { href: "/creatives", label: "Креативы", icon: Sparkles },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="flex w-60 shrink-0 flex-col border-r border-gray-200 bg-white">
      <div className="px-5 py-6">
        <p className="text-lg font-bold text-gray-900">Ad Agent</p>
        <p className="mt-0.5 text-xs text-gray-500">
          Яндекс.Директ · VK Ads
        </p>
      </div>
      <nav className="flex-1 space-y-1 px-3">
        {NAV.map(({ href, label, icon: Icon }) => {
          const active = pathname.startsWith(href);
          return (
            <Link
              key={href}
              href={href}
              className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                active
                  ? "bg-blue-50 text-blue-700"
                  : "text-gray-600 hover:bg-gray-100 hover:text-gray-900"
              }`}
            >
              <Icon className="h-4 w-4" />
              {label}
            </Link>
          );
        })}
      </nav>
      <div className="border-t border-gray-100 px-5 py-4 text-xs text-gray-400">
        Тестовый режим · демо-данные
      </div>
    </aside>
  );
}
