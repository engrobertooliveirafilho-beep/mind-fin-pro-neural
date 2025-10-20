import React, { useEffect, useMemo, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

/** Fonte de dados: .env (VITE_AUDIT_JSON) ou fallback em /public */
const DATA_URL = import.meta.env.VITE_AUDIT_JSON ?? "/MIND_AUDIT_ENRICHED.json";

/* ----------------------- animações ----------------------- */
const listVariants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.06 }
  }
};

const cardVariants = {
  hidden: { y: 8, opacity: 0 },
  show: {
    y: 0,
    opacity: 1,
    transition: { duration: 0.2, ease: "easeOut" }
  }
};

/* ----------------------- helpers ----------------------- */
const colorByStatus = (s) => {
  const k = String(s || "").toLowerCase();
  if (["ok", "success", "good", "aprovado"].includes(k))
    return "border-emerald-500/40 text-emerald-300 bg-emerald-500/10";
  if (["warn", "warning", "atenção", "atencao"].includes(k))
    return "border-amber-500/40 text-amber-300 bg-amber-500/10";
  if (["error", "fail", "crítico", "critico"].includes(k))
    return "border-rose-500/40 text-rose-300 bg-rose-500/10";
  return "border-sky-500/40 text-sky-300 bg-sky-500/10";
};

const TAGS = ["ok", "warn", "info", "error"];

export default function App() {
  const [meta, setMeta] = useState(null);
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState("");

  // filtros
  const [q, setQ] = useState("");
  const [status, setStatus] = useState("all");
  const [limit, setLimit] = useState(20);

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        setLoading(true);
        setErr("");
        const res = await fetch(DATA_URL, { cache: "no-store" });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const json = await res.json();

        if (!alive) return;
        setMeta({
          version: json.version ?? "v0.x",
          generatedAt: json.generated ?? "",
          root: json.root ?? ""
        });
        setItems(Array.isArray(json.entries) ? json.entries : []);
      } catch (e) {
        setErr(`Falha ao carregar: ${String(e.message || e)}`);
        setItems([]);
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => {
      alive = false;
    };
  }, []);

  const filtered = useMemo(() => {
    let list = items;
    if (status !== "all") {
      list = list.filter(
        (it) => String(it.status || "").toLowerCase() === status
      );
    }
    if (q.trim()) {
      const key = q.toLowerCase();
      list = list.filter((it) => {
        const hay =
          `${it.title} ${it.file} ${it.origin} ${it.status} ${it.message}`.toLowerCase();
        return hay.includes(key);
      });
    }
    // mais recentes primeiro se tiver timestamp 'YYYY-MM-DD HH:mm'
    return list.slice(0, limit);
  }, [items, status, q, limit]);

  /* -------------- skeletons enquanto carrega -------------- */
  const skeletons = Array.from({ length: 6 }).map((_, i) => (
    <div
      key={`sk-${i}`}
      className="rounded-xl border border-white/10 bg-white/5 p-4 animate-pulse h-28"
    />
  ));

  return (
    <div className="min-h-screen bg-[#0B0E14] text-[#E6EDF7]">
      {/* Header */}
      <header className="sticky top-0 z-10 backdrop-blur bg-black/30 border-b border-white/10">
        <div className="mx-auto max-w-7xl px-4 py-3 flex items-center gap-3">
          <div className="size-6 rounded-sm bg-white/10" />
          <div className="flex-1">
            <h1 className="text-sm sm:text-base font-semibold">
              MIND FIN PRO – Audit Feed
            </h1>
            <p className="text-xs text-white/50">
              {meta
                ? `build: ${meta.version} • gerado: ${meta.generatedAt}`
                : "carregando…"}
            </p>
          </div>

          {/* “JSON v0.1” como badge */}
          <span className="text-[11px] px-2 py-1 rounded-full bg-white/5 border border-white/10">
            JSON v0.1
          </span>
        </div>
        {/* Filtros */}
        <div className="mx-auto max-w-7xl px-4 pb-3">
          <div className="flex flex-wrap items-center gap-2">
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Buscar (título, arquivo, status...)"
              className="flex-1 min-w-[260px] rounded-lg bg-white/5 border border-white/10 px-3 py-2 text-sm outline-none focus:border-white/20"
            />
            <select
              value={status}
              onChange={(e) => setStatus(e.target.value)}
              className="rounded-lg bg-white/5 border border-white/10 px-2 py-2 text-sm"
            >
              <option value="all">Status: Todos</option>
              {TAGS.map((t) => (
                <option key={t} value={t}>
                  {t.toUpperCase()}
                </option>
              ))}
            </select>
            <select
              value={limit}
              onChange={(e) => setLimit(Number(e.target.value))}
              className="rounded-lg bg-white/5 border border-white/10 px-2 py-2 text-sm"
            >
              {[10, 20, 50, 100].map((n) => (
                <option key={n} value={n}>
                  {n} itens
                </option>
              ))}
            </select>
            <button
              onClick={() => {
                setQ("");
                setStatus("all");
              }}
              className="text-xs px-2 py-2 rounded-lg border border-white/10 bg-white/5"
            >
              Reset
            </button>
          </div>
        </div>
      </header>

      {/* Erro de carregamento */}
      {err && (
        <div className="mx-auto max-w-7xl px-4 pt-3">
          <div className="rounded-lg border border-rose-500/30 bg-rose-500/10 text-rose-200 px-3 py-2 text-sm">
            {err}
          </div>
        </div>
      )}

      {/* Grid de cards */}
      <main className="mx-auto max-w-7xl px-4 py-5">
        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
            {skeletons}
          </div>
        ) : filtered.length === 0 ? (
          <div className="text-white/60 text-sm">Nada encontrado.</div>
        ) : (
          <motion.div
            variants={listVariants}
            initial="hidden"
            animate="show"
            className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4"
          >
            <AnimatePresence>
              {filtered.map((it, idx) => (
                <motion.div
                  key={`${it.timestamp}-${it.title}-${idx}`}
                  variants={cardVariants}
                  whileHover={{ y: -2, scale: 1.01 }}
                  transition={{ type: "spring", stiffness: 320, damping: 22 }}
                  className="rounded-xl border border-white/10 bg-white/5 p-4"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <h3 className="font-medium leading-5">
                        {it.title ?? "—"}
                      </h3>
                      <p className="text-xs text-white/50">
                        {it.file ?? "—"} • {it.origin ?? "—"}
                      </p>
                    </div>
                    {/* badge status */}
                    <span
                      className={
                        "text-[11px] px-2 py-1 rounded-full border " +
                        colorByStatus(it.status)
                      }
                    >
                      {String(it.status || "").toUpperCase() || "INFO"}
                    </span>
                  </div>

                  {it.message && (
                    <p className="mt-3 text-sm leading-relaxed text-white/80">
                      {it.message}
                    </p>
                  )}

                  <div className="mt-3 text-[11px] text-white/40">
                    {it.timestamp ?? ""}
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          </motion.div>
        )}
      </main>
    </div>
  );
}
