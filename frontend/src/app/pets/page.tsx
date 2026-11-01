"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useCallback, useEffect, useState } from "react";
import { api, auth, Page, Pet } from "@/lib/api";

const SPECIES = ["dog", "cat", "bird", "rabbit", "fish", "other"];
const EMOJI: Record<string, string> = { dog: "🐶", cat: "🐱", bird: "🐦", rabbit: "🐰", fish: "🐟", other: "🐾" };

function formatAge(months: number | null) {
  if (months === null) return "Age unknown";
  if (months < 12) return `${months} mo`;
  const y = Math.floor(months / 12);
  return `${y} yr${y > 1 ? "s" : ""}${months % 12 ? ` ${months % 12} mo` : ""}`;
}

const emptyForm = { name: "", species: "dog", breed: "", gender: "unknown", date_of_birth: "", weight_kg: "" };

export default function PetsPage() {
  const router = useRouter();
  const [pets, setPets] = useState<Pet[] | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState(emptyForm);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    try {
      setPets((await api<Page<Pet>>("/pets/")).results);
    } catch {
      auth.logout();
      router.push("/login");
    }
  }, [router]);

  useEffect(() => {
    if (!auth.isLoggedIn()) router.push("/login");
    else load();
  }, [load, router]);

  async function addPet(e: FormEvent) {
    e.preventDefault();
    setError("");
    const body = { ...form, date_of_birth: form.date_of_birth || null, weight_kg: form.weight_kg || null };
    try {
      await api("/pets/", { method: "POST", body: JSON.stringify(body) });
      setForm(emptyForm);
      setShowForm(false);
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not save pet");
    }
  }

  async function removePet(pet: Pet) {
    if (!confirm(`Remove ${pet.name}?`)) return;
    await api(`/pets/${pet.id}/`, { method: "DELETE" });
    load();
  }

  const set = (k: keyof typeof form) => (e: { target: { value: string } }) => setForm({ ...form, [k]: e.target.value });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">My pets</h1>
        <button className="btn" onClick={() => setShowForm((s) => !s)}>
          {showForm ? "Cancel" : "+ Add pet"}
        </button>
      </div>

      {showForm && (
        <form onSubmit={addPet} className="card grid gap-4 sm:grid-cols-2">
          <input className="input" placeholder="Name" value={form.name} onChange={set("name")} required />
          <select className="input" value={form.species} onChange={set("species")}>
            {SPECIES.map((s) => (
              <option key={s} value={s}>
                {EMOJI[s]} {s[0].toUpperCase() + s.slice(1)}
              </option>
            ))}
          </select>
          <input className="input" placeholder="Breed (e.g. Labrador)" value={form.breed} onChange={set("breed")} />
          <select className="input" value={form.gender} onChange={set("gender")}>
            <option value="unknown">Gender</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
          <label className="space-y-1 text-sm">
            <span className="text-stone-600">Date of birth</span>
            <input className="input" type="date" value={form.date_of_birth} onChange={set("date_of_birth")} />
          </label>
          <label className="space-y-1 text-sm">
            <span className="text-stone-600">Weight (kg)</span>
            <input className="input" type="number" step="0.1" min="0" value={form.weight_kg} onChange={set("weight_kg")} />
          </label>
          {error && <p className="text-sm text-red-600 sm:col-span-2">{error}</p>}
          <button className="btn sm:col-span-2">Save pet</button>
        </form>
      )}

      {pets === null ? (
        <p className="text-stone-500">Loading…</p>
      ) : pets.length === 0 ? (
        <div className="card text-center text-stone-600">
          <div className="text-4xl">🐾</div>
          <p className="mt-2">No pets yet. Add your first pet to get started.</p>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          {pets.map((pet) => {
            const nextDue = pet.vaccinations.map((v) => v.next_due).filter(Boolean).sort()[0];
            return (
              <div key={pet.id} className="card flex gap-4">
                <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-full bg-brand-50 text-3xl">
                  {EMOJI[pet.species] ?? "🐾"}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-start justify-between gap-2">
                    <h2 className="text-lg font-semibold">{pet.name}</h2>
                    <button className="text-sm text-stone-400 hover:text-red-600" onClick={() => removePet(pet)}>
                      Remove
                    </button>
                  </div>
                  <p className="text-sm text-stone-600">
                    {pet.breed || pet.species} · {formatAge(pet.age_months)}
                    {pet.weight_kg && ` · ${pet.weight_kg} kg`}
                  </p>
                  <p className="mt-2 text-xs text-stone-500">
                    💉 {pet.vaccinations.length} vaccination{pet.vaccinations.length === 1 ? "" : "s"}
                    {nextDue && ` · next due ${nextDue}`}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
