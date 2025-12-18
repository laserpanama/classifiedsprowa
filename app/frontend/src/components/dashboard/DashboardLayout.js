import React from 'react';
import { Button } from '@/components/ui/button';

const DashboardLayout = ({ children }) => {
  return (
    <div className="flex h-screen bg-gray-100 dark:bg-gray-900">
      <aside className="w-64 bg-white dark:bg-gray-800 p-4 shadow-md">
        <h1 className="text-2xl font-bold mb-4 text-center">Classifieds Pro</h1>
        <nav>
          <ul>
            <li className="mb-2">
              <Button variant="ghost" className="w-full justify-start">
                {/* Icon can be added here later */}
                Dashboard
              </Button>
            </li>
            <li className="mb-2">
              <Button variant="ghost" className="w-full justify-start">
                Accounts
              </Button>
            </li>
            <li className="mb-2">
              <Button variant="ghost" className="w-full justify-start">
                Ads
              </Button>
            </li>
            <li className="mb-2">
              <Button variant="ghost" className="w-full justify-start">
                Schedules
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

export default DashboardLayout;
