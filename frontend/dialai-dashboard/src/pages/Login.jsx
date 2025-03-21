import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Auth.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  
  console.log('Login component rendered');

  // Remove the automatic navigation that might be causing issues
  // useEffect(() => {
  //   navigate("/dashboard");
  // }, [navigate]);
  
  // Add a check for existing authentication
  useEffect(() => {
    console.log('Login useEffect running');
    const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
    console.log('Is authenticated:', isAuthenticated);
    
    if (isAuthenticated) {
      console.log('User is already authenticated, redirecting to dashboard');
      navigate('/dashboard');
    }
  }, [navigate]);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Login form submitted with:', email, password);
    
    try {
      // Mock successful login
      localStorage.setItem('isAuthenticated', 'true');
      console.log('Authentication set in localStorage');
      
      // Navigate to dashboard
      console.log('Navigating to dashboard');
      navigate('/dashboard');
    } catch (error) {
      console.error('Error during login process:', error);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-form-container">
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="focus:border-purple-500"
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="focus:border-purple-500"
            />
          </div>
          <button type="submit" className="auth-button">Login</button>
        </form>
        <p className='p-2 text-center text-black'>
          Don't have an account? <a href="/signup">Sign up</a>
        </p>
      </div>
    </div>
  );
};

export default Login;