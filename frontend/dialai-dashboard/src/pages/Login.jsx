import React from 'react';
import { SignIn } from '@clerk/clerk-react';
import '../styles/Auth.css';

const Login = () => {
  return (
    <div className="auth-container">
      <SignIn 
        signUpUrl="/signup"
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