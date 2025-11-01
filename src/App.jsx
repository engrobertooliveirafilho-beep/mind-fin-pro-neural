import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useStore } from "./state/useStore";
import { api } from "./lib/http";
import { motion } from "framer-motion";

const qc = new QueryClient();

export default function App() {
  const { user } = useStore();

  return (
    <QueryClientProvider client={qc}>
      <main className="min-h-screen bg-gray-950 text-white p-6">
        <motion.h1 initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-2xl font-bold">
          Mind Fin Pro Neural
        </motion.h1>
        <p>Usuário: {user?.name ?? "não logado"}</p>
      </main>
    </QueryClientProvider>
  );
}
