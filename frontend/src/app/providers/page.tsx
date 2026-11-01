"use client";

import { useEffect, useState } from "react";
import { api, Page, Provider } from "@/lib/api";

const CATEGORIES = [
  { value: "", label: "All services" },
  { value: "grooming", label: "✂️ Grooming" },
  { value: "vet_visit", label: "🏠 Vet home visit" },
  { value: "vet_clinic", label: "🏥 Vet clinic" },
  { value: "training", label: "🎓 Training" },
  { value: "walking", label: "🦮 Walking" },
  { value: "boarding", label: "🏡 Boarding & daycare" },
];

export default function ProvidersPage() {
  const [city, setCity] = useState("");
  const [category, setCategory] = useState("");
  const [homeOnly, setHomeOnly] = useState(false);
  const [providers, setProviders] = useState<Provider[] | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const params = new URLSearchParams();
    if (city.trim()) params.set("city", city.trim());
    if (category) params.set("category", category);
    if (homeOnly) params.set("home", "true");
    const t = setTimeout(() => {
      api<Page<Provider>>(`/providers/?${params}`)
        .then((d) => {
          setProviders(d.results);
          setError("");
        })
        .catch(() => setError("Could not load providers. Is the backend running?"));
    }, 300);
    return () => clearTimeout(t);
  }, [city, category, homeOnly]);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Find pet services</h1>

      <div className="card grid gap-3 sm:grid-cols-[1fr_1fr_auto] sm:items-center">
        <input className="input" placeholder="City (e.g. Delhi)" value={city} onChange={(e) => setCity(e.target.value)} />
        <select className="input" value={category} onChange={(e) => setCategory(e.target.value)}>
          {CATEGORIES.map((c) => (
            <option key={c.value} value={c.value}>
              {c.label}
            </option>
          ))}
        </select>
        <label className="flex items-center gap-2 text-sm">
          <input type="checkbox" checked={homeOnly} onChange={(e) => setHomeOnly(e.target.checked)} />
          Home service
        </label>
      </div>

      {error && <p className="text-red-600">{error}</p>}

      {providers === null ? (
        !error && <p className="text-stone-500">Loading…</p>
      ) : providers.length === 0 ? (
        <div className="card text-center text-stone-600">No verified providers match yet. Try another city or service.</div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          {providers.map((p) => (
            <div key={p.id} className="card space-y-3">
              <div className="flex items-start justify-between gap-2">
                <div>
                  <h2 className="text-lg font-semibold">{p.business_name}</h2>
                  <p className="text-sm text-stone-500">
                    📍 {p.city} · {p.years_experience} yrs experience
                  </p>
                </div>
                {p.offers_home_service && (
                  <span className="rounded-full bg-green-50 px-2 py-0.5 text-xs font-medium text-green-700">Home visits</span>
                )}
              </div>
              {p.bio && <p className="text-sm text-stone-600">{p.bio}</p>}
              <ul className="divide-y divide-stone-100 text-sm">
                {p.services.map((s) => (
                  <li key={s.id} className="flex justify-between py-1.5">
                    <span>
                      {s.name} <span className="text-stone-400">· {s.duration_minutes} min</span>
                    </span>
                    <span className="font-medium">₹{Number(s.price_inr).toLocaleString("en-IN")}</span>
                  </li>
                ))}
              </ul>
              <button className="btn w-full" disabled title="Booking comes in Phase 1">
                Book (coming soon)
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
