import React from 'react';
import { SignUp, Waitlist } from '@clerk/clerk-react';
import '../styles/Auth.css';

const Signup = () => {
  return (
    <div className="auth-container">
        <Waitlist signInUrl="/login" afterJoinWaitlistUrl="/login" />
    </div>
  );
};

export default Signup; 