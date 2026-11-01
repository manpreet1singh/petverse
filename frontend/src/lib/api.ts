// Small fetch wrapper for the PetVerse API. Stores JWTs in localStorage and
// refreshes the access token once on a 401.

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api";

export type User = { id: number; phone: string; name: string; email: string; city: string; role: string };

export type Vaccination = { id: number; vaccine_name: string; date_given: string; next_due: string | null };

export type Pet = {
  id: number;
  name: string;
  species: string;
  breed: string;
  gender: string;
  date_of_birth: string | null;
  age_months: number | null;
  weight_kg: string | null;
  vaccinations: Vaccination[];
};

export type Service = { id: number; category: string; name: string; price_inr: string; duration_minutes: number };

export type Provider = {
  id: number;
  business_name: string;
  bio: string;
  city: string;
  offers_home_service: boolean;
  years_experience: number;
  services: Service[];
};

export type Page<T> = { count: number; results: T[] };

const tokens = {
  get access() {
    return typeof window === "undefined" ? null : localStorage.getItem("access");
  },
  get refresh() {
    return typeof window === "undefined" ? null : localStorage.getItem("refresh");
  },
  set(access: string, refresh?: string) {
    localStorage.setItem("access", access);
    if (refresh) localStorage.setItem("refresh", refresh);
  },
  clear() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
  },
};

export class ApiError extends Error {
  constructor(public status: number, public data: unknown) {
    super(typeof data === "object" && data && "detail" in data ? String((data as { detail: unknown }).detail) : `Request failed (${status})`);
  }
}

async function refreshAccess(): Promise<boolean> {
  if (!tokens.refresh) return false;
  const r = await fetch(`${API_URL}/auth/token/refresh/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh: tokens.refresh }),
  });
  if (!r.ok) {
    tokens.clear();
    return false;
  }
  const data = await r.json();
  tokens.set(data.access, data.refresh);
  return true;
}

export async function api<T>(path: string, options: RequestInit = {}, retry = true): Promise<T> {
  const headers = new Headers(options.headers);
  if (options.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  if (tokens.access) headers.set("Authorization", `Bearer ${tokens.access}`);

  const r = await fetch(`${API_URL}${path}`, { ...options, headers });
  if (r.status === 401 && retry && (await refreshAccess())) return api<T>(path, options, false);
  if (r.status === 204) return undefined as T;
  const data = await r.json().catch(() => null);
  if (!r.ok) throw new ApiError(r.status, data);
  return data as T;
}

export const auth = {
  requestOtp: (phone: string) =>
    api<{ detail: string }>("/auth/otp/request/", { method: "POST", body: JSON.stringify({ phone }) }),
  async verifyOtp(phone: string, code: string) {
    const data = await api<{ access: string; refresh: string; user: User; is_new_user: boolean }>(
      "/auth/otp/verify/",
      { method: "POST", body: JSON.stringify({ phone, code }) },
    );
    tokens.set(data.access, data.refresh);
    return data;
  },
  me: () => api<User>("/auth/me/"),
  isLoggedIn: () => !!tokens.access,
  logout: () => tokens.clear(),
};
