import type { Campaign, Recommendation, Statistic } from "@/types";

const API_BASE = process.env.BACKEND_URL || "http://localhost:8000";

async function request<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}/api/v1${path}`, {
    cache: "no-store",
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) {
    throw new Error(`API error ${res.status}: ${await res.text()}`);
  }
  return res.json() as Promise<T>;
}

export async function fetchCampaigns(): Promise<Campaign[]> {
  return request<Campaign[]>("/campaigns");
}

export async function fetchStatistics(): Promise<Statistic[]> {
  return request<Statistic[]>("/statistics");
}

export async function fetchRecommendations(): Promise<Recommendation[]> {
  return request<Recommendation[]>("/recommendations");
}