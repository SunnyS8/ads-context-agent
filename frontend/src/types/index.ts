export type CampaignStatus = "active" | "paused" | "archived";

export interface Campaign {
  id: number;
  platform: string;
  external_id: string;
  name: string;
  status: CampaignStatus;
  daily_budget: number | null;
  target_cpl: number | null;
  created_at: string;
  updated_at: string;
}

export interface Statistic {
  id: number;
  campaign_id: number;
  date: string;
  impressions: number;
  clicks: number;
  spend: number;
  conversions: number;
  revenue: number;
}

export interface Recommendation {
  id: number;
  campaign_id: number;
  action: string;
  old_value: number | null;
  new_value: number | null;
  reason: string;
  status: "pending" | "approved" | "rejected" | "applied" | "expired";
  created_at: string;
}