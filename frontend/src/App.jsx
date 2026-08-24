import { Routes, Route } from "react-router-dom";

import PageShell from "./components/layout/PageShell";
import Dashboard from "./pages/Dashboard";
import NewRun from "./pages/NewRun";
import LiveRun from "./pages/LiveRun";
import Findings from "./pages/Findings";

export default function App() {
  return (
    <PageShell>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/new" element={<NewRun />} />
        <Route path="/runs/:sessionId" element={<LiveRun />} />
        <Route path="/runs/:sessionId/findings" element={<Findings />} />
      </Routes>
    </PageShell>
  );
}