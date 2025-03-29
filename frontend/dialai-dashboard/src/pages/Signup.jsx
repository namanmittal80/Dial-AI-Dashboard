import React from 'react';
import { SignUp } from '@clerk/clerk-react';
import '../styles/Auth.css';

const Signup = () => {
  return (
    <div className="auth-container">
        <SignUp signInUrl="/login" />
    </div>
  );
};

export default Signup; 