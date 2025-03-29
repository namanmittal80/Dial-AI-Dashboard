import React, { useState, useEffect } from 'react';
import { useUser, useClerk } from '@clerk/clerk-react';
import Sidebar from './Sidebar';

const Layout = ({ children }) => {
  console.log('Layout component rendering');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const { isSignedIn, user } = useUser();
  const { isLoaded } = useClerk();

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  console.log('Layout rendering content, user:', user?.id);
  
  return (
    <div className="flex h-screen">
      <Sidebar isOpen={sidebarOpen} toggleSidebar={toggleSidebar} />
      <div 
        className={`flex-1 transition-all duration-150 ease-in-out overflow-auto ${sidebarOpen ? 'ml-64' : 'ml-16'}`}
      >
        {children}
      </div>
    </div>
  );
};

export default Layout; 