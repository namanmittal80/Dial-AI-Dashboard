import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import SmallTile from '../components/tiles/SmallTile';
import MediumTile from '../components/tiles/MediumTile';
import LargeTile from '../components/tiles/LargeTile';
import ConversationAnalytics from '../components/ConversationAnalytics';
import ThemeToggle from '../components/ThemeToggle';
import { ThemeContext } from '../context/ThemeContext';
import { ConversationContext } from '../context/ConversationContext';
import apiService from '../api/apiService';
import '../styles/Dashboard.css';
import DailyVolumeChartComponent from '../components/charts/DailyVolumeChartComponent';
import { dailyCallVolumeByMonth } from '../api/mockData';
import ConversationTile from '../components/ConversationTile';

// Modern SVG Icons
const CallIcon = () => {
  const themeContext = useContext(ThemeContext);
  const darkMode = themeContext?.darkMode;
  
  return (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-indigo-600 dark:text-blue-400" viewBox="0 0 20 20" fill="currentColor" stroke="currentColor" strokeWidth={darkMode ? "0" : "0.8"}>
      <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z" fillOpacity={darkMode ? "1" : "0.5"} />
    </svg>
  );
};

const DropIcon = () => {
  const themeContext = useContext(ThemeContext);
  const darkMode = themeContext?.darkMode;
  
  return (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-red-600 dark:text-red-400" viewBox="0 0 20 20" fill="currentColor" stroke="currentColor" strokeWidth={darkMode ? "0" : "0.8"}>
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" fillOpacity={darkMode ? "1" : "0.5"} />
    </svg>
  );
};

const ConnectIcon = () => {
  const themeContext = useContext(ThemeContext);
  const darkMode = themeContext?.darkMode;
  
  return (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-emerald-600 dark:text-green-400" viewBox="0 0 20 20" fill="currentColor" stroke="currentColor" strokeWidth={darkMode ? "0" : "0.8"}>
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" fillOpacity={darkMode ? "1" : "0.5"} />
    </svg>
  );
};

// New SuccessRateIcon (percentage/stats based)
const SuccessRateIcon = () => {
  const themeContext = useContext(ThemeContext);
  const darkMode = themeContext?.darkMode;
  
  return (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-amber-600 dark:text-amber-400" viewBox="0 0 20 20" fill="currentColor" stroke="currentColor" strokeWidth={darkMode ? "0" : "0.8"}>
      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" fillOpacity={darkMode ? "1" : "0.5"} />
    </svg>
  );
};

const Dashboard = () => {
  console.log('Dashboard component rendering');
  const navigate = useNavigate();
  
  // Wrap context usage in try/catch to debug potential context issues
  let darkMode, selectConversationById;
  try {
    const themeContext = useContext(ThemeContext);
    darkMode = themeContext?.darkMode;
    console.log('Theme context loaded, darkMode:', darkMode);
    
    const conversationContext = useContext(ConversationContext);
    selectConversationById = conversationContext?.selectConversationById;
    console.log('Conversation context loaded');
  } catch (error) {
    console.error('Error accessing context:', error);
  }
  
  const [dashboardData, setDashboardData] = useState(null);
  const [recentConversations, setRecentConversations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    console.log('Dashboard useEffect running');
    
    // Check authentication
    const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
    console.log('Is authenticated in Dashboard:', isAuthenticated);
    
    if (!isAuthenticated) {
      console.log('User is not authenticated, redirecting to login');
      navigate('/login');
      return;
    }

    // Fetch dashboard data
    const fetchDashboardData = async () => {
      try {
        console.log('Fetching dashboard data');
        setLoading(true);
        const data = await apiService.dashboard.getStats();
        console.log('Dashboard data received:', data);
        setDashboardData(data);
        
        // Fetch recent conversations separately
        try {
          console.log('Fetching recent conversations');
          const conversationsData = await apiService.conversations.getRecent();
          console.log('Recent conversations received:', conversationsData);
          
          // Add index to each conversation for reference
          const conversationsWithIndex = conversationsData.map((conversation, index) => ({
            ...conversation,
            index
          }));
          setRecentConversations(conversationsWithIndex);
        } catch (convErr) {
          console.error('Error fetching recent conversations:', convErr);
          // Don't fail the whole dashboard if just conversations fail
          setRecentConversations([]);
        }
        
        setLoading(false);
      } catch (err) {
        console.error('Error fetching dashboard data:', err);
        setError(err.message);
        setLoading(false);
      }
    };
    
    fetchDashboardData();
  }, [navigate]);

  const handleLogout = () => {
    console.log('Logout clicked');
    localStorage.removeItem('isAuthenticated');
    console.log('Authentication removed from localStorage');
    navigate('/login');
  };

  // Handle conversation tile click
  const handleConversationClick = (conversation) => {
    console.log("Dashboard: Conversation clicked, ID:", conversation.id);
    
    // Use window.location for direct navigation to ensure a fresh load
    window.location.href = `/conversation-insights?index=${conversation.index}`;
  };

  return (
    <div className="min-h-screen w-full" style={{ backgroundColor: 'var(--color-bg-primary)' }}>
      <header className="flex justify-between items-center p-4 border-b shadow-sm" 
        style={{ 
          backgroundColor: 'var(--color-bg-primary)', 
          borderColor: darkMode ? '#2d3748' : '#e2e8f0',
          color: 'var(--color-text-primary)'
        }}>
        <h1 className="text-2xl font-bold" style={{ color: 'var(--color-text-primary)' }}>Dashboard</h1>
        <div className="flex items-center space-x-4">
          <ThemeToggle />
          <button 
            onClick={handleLogout} 
            className="px-4 py-2 text-white rounded-md hover:opacity-90 transition-opacity"
            style={{ 
              background: `linear-gradient(to right, var(--color-gradient-primary), var(--color-gradient-secondary))` 
            }}
          >
            Logout
          </button>
        </div>
      </header>
      
      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-primary-500"></div>
        </div>
      ) : error ? (
        <div className="p-4">
          <div className="bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200 p-4 rounded-lg">
            Error loading dashboard data: {error}
          </div>
        </div>
      ) : (
        <>
          {/* Small tiles in a grid with exact widths */}
          <div className="p-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              <div>
                <SmallTile 
                  title="Total Calls" 
                  value={dashboardData?.total_calls || 0} 
                  icon={<CallIcon />} 
                  layout="modern"
                />
              </div>
              <div>
                <SmallTile 
                  title="Calls Connected" 
                  value={dashboardData?.calls_connected || 0} 
                  icon={<ConnectIcon />} 
                  layout="modern"
                />
              </div>
              <div>
                <SmallTile 
                  title="Calls Dropped" 
                  value={dashboardData?.calls_dropped || 0} 
                  icon={<DropIcon />} 
                  layout="modern"
                />
              </div>
              <div>
                <SmallTile 
                  title="Success Rate" 
                  value={`${dashboardData?.success_rate || 0}%`} 
                  icon={<SuccessRateIcon />} 
                  layout="modern"
                />
              </div>
            </div>
          </div>
          <div className="p-4">
            <ConversationAnalytics />
          </div>
          <div className="p-4 grid grid-cols-1 gap-4">
            <LargeTile title={<span className="text-gray-900 dark:text-white">Daily Call Volume</span>}>
              <div className="h-full w-full rounded-lg" 
                style={{ 
                  backgroundColor: 'var(--color-bg-primary)',
                  color: 'var(--color-text-primary)',
                  overflow: 'hidden'
                }}>
                <DailyVolumeChartComponent data={dailyCallVolumeByMonth} />
              </div>
            </LargeTile>
          </div>

       

          {/* Recent Conversations */}
          {/* {recentConversations.length > 0 && (
            <div className="p-4 mb-6">
              <h2 className="text-xl font-bold mb-4" style={{ color: 'var(--color-text-primary)' }}>Recent Conversations</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {recentConversations.map((conversation) => (
                  <div key={conversation.id}>
                    <ConversationTile 
                      conversation={conversation} 
                      index={conversation.index}
                      onClick={handleConversationClick}
                    />
                  </div>
                ))}
              </div>
            </div>
          )} */}
        </>
      )}
    </div>
  );
};

export default Dashboard; 