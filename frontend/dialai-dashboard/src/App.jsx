import React, { Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import { ConversationProvider } from './context/ConversationContext';
import { SignedIn, SignedOut, RedirectToSignIn, useUser } from "@clerk/clerk-react";
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import ConversationInsights from './pages/ConversationInsights';
import Layout from './components/Layout';
import './App.css';

// Simple error boundary component
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Error caught by boundary:", error, errorInfo);
    this.setState({
      error: error,
      errorInfo: errorInfo
    });
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '20px', margin: '20px', border: '1px solid red', borderRadius: '5px' }}>
          <h2>Something went wrong.</h2>
          <details style={{ whiteSpace: 'pre-wrap' }}>
            {this.state.error && this.state.error.toString()}
            <br />
            {this.state.errorInfo && this.state.errorInfo.componentStack}
          </details>
          <button 
            onClick={() => window.location.reload()}
            style={{ 
              marginTop: '10px', 
              padding: '8px 16px', 
              background: '#f44336', 
              color: 'white', 
              border: 'none', 
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Reload Page
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

// Loading fallback component
const LoadingFallback = () => (
  <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
    <p>Loading...</p>
  </div>
);

// Create reusable protected route components
const ProtectedRoute = ({ children }) => {  
  return (
    <>
      <SignedIn>
        <Layout>{children}</Layout>
      </SignedIn>
      <SignedOut>
        <Navigate to="/login" replace />
      </SignedOut>
    </>
  );
};

// Create component for authentication pages that redirect when signed in
const AuthRoute = ({ children }) => {
  return (
    <>
      <SignedIn>
        <Navigate to="/dashboard" replace />
      </SignedIn>
      <SignedOut>
        {children}
      </SignedOut>
    </>
  );
};

function App() {
  console.log('App component rendering');
  
  return (
    <ErrorBoundary>
      <Suspense fallback={<LoadingFallback />}>
        <ThemeProvider>
          <ConversationProvider>
            <Router>
              <Routes>
                <Route path="/login" element={
                  <AuthRoute>
                    <Login />
                  </AuthRoute>
                } />
                
                <Route path="/signup" element={
                  <AuthRoute>
                    <Signup />
                  </AuthRoute>
                } />
                
                <Route path="/dashboard" element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                } />
                
                <Route path="/conversation-insights" element={
                  <ProtectedRoute>
                    <ConversationInsights />
                  </ProtectedRoute>
                } />
                
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
                <Route path="*" element={<Navigate to="/dashboard" replace />} />
              </Routes>
            </Router>
          </ConversationProvider>
        </ThemeProvider>
      </Suspense>
    </ErrorBoundary>
  );
}

export default App; 