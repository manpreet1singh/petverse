import Link from "next/link";

const features = [
  { icon: "🩺", title: "Health records", text: "Vaccinations, allergies and vet notes for every pet, always with you." },
  { icon: "✂️", title: "Grooming", text: "Book verified groomers at home or in-salon." },
  { icon: "🏥", title: "Vet visits", text: "Find vets near you, including home visits." },
  { icon: "🎓", title: "Training & walking", text: "Trusted trainers and walkers in your city." },
];

export default function Home() {
  return (
    <div className="space-y-12">
      <section className="rounded-3xl bg-gradient-to-br from-brand-50 to-amber-50 px-6 py-14 text-center sm:px-12">
        <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl">Everything your pet needs, in one place</h1>
        <p className="mx-auto mt-4 max-w-xl text-lg text-stone-600">
          Keep your pet&apos;s health records, and book verified groomers, vets and trainers near you.
        </p>
        <div className="mt-8 flex flex-wrap justify-center gap-3">
          <Link href="/login" className="btn px-6 py-3">
            Get started
          </Link>
          <Link href="/providers" className="btn-outline px-6 py-3">
            Browse services
          </Link>
        </div>
      </section>

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {features.map((f) => (
          <div key={f.title} className="card">
            <div className="text-3xl">{f.icon}</div>
            <h3 className="mt-3 font-semibold">{f.title}</h3>
            <p className="mt-1 text-sm text-stone-600">{f.text}</p>
          </div>
        ))}
      </section>
    </div>
  );
}
