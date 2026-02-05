import React, { useState } from "react";
import HostLogin from "../components/Login";
import HostSignup from "../components/SignUp";
import Footer from "../components/Footer";
import Navbar from "../components/Navbar";
const HostAuthPage: React.FC = () => {
  const [isLogin, setIsLogin] = useState(true);

  const toggleToSignup = () => setIsLogin(false);
  const toggleToLogin = () => setIsLogin(true);

  return (
    <div className="min-h-screen bg-white text-gray-900">
      {/* HEADER */}
      <Navbar/>

      {/* MAIN CONTENT */}
      <main className="max-w-4xl mx-auto px-6 py-12">
        {/* Toggle Buttons */}
        <div className="flex justify-center mb-10">
          <div className="flex bg-gray-100 rounded-xl p-1 w-fit">
            <button
              onClick={toggleToLogin}
              className={`w-28 py-2 rounded-lg font-semibold transition-all
                ${isLogin 
                  ? 'bg-white text-blue-600 shadow' 
                  : 'text-gray-600'}`}
            >
              Login
            </button>
          
            <button
              onClick={toggleToSignup}
              className={`w-28 py-2 rounded-lg font-semibold transition-all
                ${!isLogin 
                  ? 'bg-white text-blue-600 shadow' 
                  : 'text-gray-600'}`}
            >
              Sign Up
            </button>
          </div>
        </div>

        {/* Form Container */}
        <div className="max-w-md mx-auto w-[700px]">
          {isLogin ? (
            <HostLogin toggleToSignup={toggleToSignup} />
          ) : (
            <HostSignup toggleToLogin={toggleToLogin} />
          )}
        </div>

       
      </main>

      {/* FOOTER */}
      <Footer/>
    </div>
  );
};

export default HostAuthPage;
