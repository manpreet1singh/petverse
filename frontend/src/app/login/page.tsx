"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { auth } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [step, setStep] = useState<"phone" | "code">("phone");
  const [phone, setPhone] = useState("");
  const [code, setCode] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Accept "9876543210" and turn it into "+919876543210".
  const normalized = () => {
    const digits = phone.replace(/[^\d+]/g, "");
    return digits.startsWith("+") ? digits : `+91${digits}`;
  };

  async function submit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      if (step === "phone") {
        await auth.requestOtp(normalized());
        setStep("code");
      } else {
        await auth.verifyOtp(normalized(), code);
        router.push("/pets");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-sm">
      <form onSubmit={submit} className="card space-y-4">
        <h1 className="text-2xl font-bold">Log in to PetVerse</h1>

        {step === "phone" ? (
          <label className="block space-y-1">
            <span className="text-sm font-medium">Mobile number</span>
            <input
              className="input"
              type="tel"
              placeholder="98765 43210"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              required
              autoFocus
            />
          </label>
        ) : (
          <label className="block space-y-1">
            <span className="text-sm font-medium">Enter the 6-digit code sent to {normalized()}</span>
            <input
              className="input tracking-[0.5em]"
              inputMode="numeric"
              maxLength={6}
              value={code}
              onChange={(e) => setCode(e.target.value.replace(/\D/g, ""))}
              required
              autoFocus
            />
          </label>
        )}

        {error && <p className="text-sm text-red-600">{error}</p>}

        <button className="btn w-full" disabled={loading}>
          {loading ? "Please wait…" : step === "phone" ? "Send code" : "Verify & log in"}
        </button>

        {step === "code" && (
          <button type="button" className="w-full text-sm text-stone-500 hover:underline" onClick={() => setStep("phone")}>
            Change number
          </button>
        )}
      </form>
    </div>
  );
}
