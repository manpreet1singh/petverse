"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { auth } from "@/lib/api";

export default function Navbar() {
  const pathname = usePathname();
  const router = useRouter();
  const [loggedIn, setLoggedIn] = useState(false);

  useEffect(() => setLoggedIn(auth.isLoggedIn()), [pathname]);

  const link = (href: string, label: string) => (
    <Link
      href={href}
      className={`rounded-md px-3 py-1.5 text-sm font-medium ${
        pathname.startsWith(href) ? "bg-brand-50 text-brand-700" : "text-stone-600 hover:text-stone-900"
      }`}
    >
      {label}
    </Link>
  );

  return (
    <header className="sticky top-0 z-10 border-b border-stone-200 bg-white/90 backdrop-blur">
      <nav className="mx-auto flex max-w-5xl items-center gap-2 px-4 py-3">
        <Link href="/" className="mr-auto text-lg font-bold text-brand-600">
          🐾 PetVerse
        </Link>
        {link("/providers", "Find services")}
        {loggedIn && link("/pets", "My pets")}
        {loggedIn ? (
          <button
            className="btn-outline text-sm"
            onClick={() => {
              auth.logout();
              setLoggedIn(false);
              router.push("/");
            }}
          >
            Log out
          </button>
        ) : (
          <Link href="/login" className="btn text-sm">
            Log in
          </Link>
        )}
      </nav>
    </header>
  );
}
