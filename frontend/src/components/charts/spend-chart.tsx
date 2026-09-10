"use client";

import {
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { Statistic } from "@/types";

type Point = {
  date: string;
  spend: number;
};

export default function SpendChart({
  statistics,
}: {
  statistics: Statistic[];
}) {
  const days = statistics.reduce<Record<string, Point>>((acc, s) => {
    acc[s.date] = {
      date: s.date,
      spend: (acc[s.date]?.spend ?? 0) + s.spend,
    };
    return acc;
  }, {});

  const data = Object.values(days).sort((a, b) =>
    a.date.localeCompare(b.date)
  );

  return (
    <div className="h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="spend"
            stroke="#2563eb"
            strokeWidth={2}
            name="Расход"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}