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
    <div className="min-h-screen bg-slate-50 text-gray-900 dark:bg-slate-950 dark:text-slate-100">
      {/* HEADER */}
      <Navbar/>

      {/* MAIN CONTENT */}
      <main className="max-w-4xl mx-auto px-6 py-12">
        {/* Toggle Buttons */}
        <div className="flex justify-center mb-10">
          <div className="flex items-center rounded-xl border border-slate-200 bg-slate-100/90 p-1 shadow-sm dark:border-slate-700 dark:bg-slate-900/90">
  <button
    onClick={toggleToLogin}
    className={`w-28 py-2 rounded-lg font-semibold transition-all duration-200
      ${isLogin 
        ? 'bg-white text-blue-700 shadow-sm dark:bg-slate-800 dark:text-sky-300' 
        : 'text-slate-600 hover:text-slate-800 dark:text-slate-300 dark:hover:text-slate-100'}`}
  >
    Login
  </button>

  <button
    onClick={toggleToSignup}
    className={`w-28 py-2 rounded-lg font-semibold transition-all duration-200
      ${!isLogin 
        ? 'bg-white text-blue-700 shadow-sm dark:bg-slate-800 dark:text-sky-300' 
        : 'text-slate-600 hover:text-slate-800 dark:text-slate-300 dark:hover:text-slate-100'}`}
  >
    Sign Up
  </button>
</div>

        </div>

        {/* Form Container */}
        <div className="w-full max-w-md mx-auto">
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
