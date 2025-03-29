import React from 'react';
import { SignIn } from '@clerk/clerk-react';
import '../styles/Auth.css';

const Login = () => {
  return (
    <div className="auth-container">
      <SignIn 
        waitlistUrl="/signup"
        appearance={{
          elements: {
            rootBox: {
              width: '100%',
              maxWidth: '500px'
            }
          }
        }}
      />
    </div>
  );
};

export default Login;