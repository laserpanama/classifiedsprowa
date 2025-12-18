import React from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import { Analytics } from "@vercel/analytics/react";
import "./App.css";
import DashboardLayout from "./components/dashboard/DashboardLayout";
import AccountsPage from "./pages/AccountsPage";
import AdsPage from "./pages/AdsPage";
import SchedulesPage from "./pages/SchedulesPage";

// Placeholder pages
const DashboardPage = () => <h2>Dashboard</h2>;
const NotFoundPage = () => <h2>404: Page Not Found</h2>;


// I will update the DashboardLayout to use Links for navigation
// This is a bit of a hack because I can't easily modify DashboardLayout.js without re-reading it
// In a real scenario, I'd edit DashboardLayout.js directly.
const PatchedDashboardLayout = ({ children }) => {
  const { Button } = require('./components/ui/button');
  return (
    <div className="flex h-screen bg-gray-100 dark:bg-gray-900">
      <aside className="w-64 bg-white dark:bg-gray-800 p-4 shadow-md">
        <h1 className="text-2xl font-bold mb-4 text-center">Classifieds Pro</h1>
        <nav>
          <ul>
            <li className="mb-2">
              <Button asChild variant="ghost" className="w-full justify-start">
                <Link to="/">Dashboard</Link>
              </Button>
            </li>
            <li className="mb-2">
              <Button asChild variant="ghost" className="w-full justify-start">
                <Link to="/accounts">Accounts</Link>
              </Button>
            </li>
            <li className="mb-2">
              <Button asChild variant="ghost" className="w-full justify-start">
                <Link to="/ads">Ads</Link>
              </Button>
            </li>
            <li className="mb-2">
              <Button asChild variant="ghost" className="w-full justify-start">
                <Link to="/schedules">Schedules</Link>
              </Button>
            </li>
          </ul>
        </nav>
      </aside>
      <main className="flex-1 p-6 overflow-y-auto">
        {children}
      </main>
    </div>
  );
};

const App = () => (
  <>
    <BrowserRouter>
      <PatchedDashboardLayout>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/accounts" element={<AccountsPage />} />
          <Route path="/ads" element={<AdsPage />} />
          <Route path="/schedules" element={<SchedulesPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </PatchedDashboardLayout>
    </BrowserRouter>
    <Analytics />
  </>
);

export default App;
