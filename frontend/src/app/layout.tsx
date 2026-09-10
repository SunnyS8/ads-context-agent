import "@/app/globals.css";
import type { Metadata } from "next";

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
        {children}
      </body>
    </html>
  );
}