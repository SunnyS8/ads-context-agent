import "@/app/globals.css";
import type { Metadata } from "next";
import { Sidebar } from "@/components/layout/sidebar";

export const metadata: Metadata = {
  title: "Агент контекстной рекламы",
  description: "Автоматизация Яндекс.Директ (eLama) и VK Ads",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ru">
      <body className="min-h-screen bg-gray-50 text-gray-900 antialiased">
        <div className="flex min-h-screen">
          <Sidebar />
          <main className="flex-1 overflow-y-auto">{children}</main>
        </div>
      </body>
    </html>
  );
}
