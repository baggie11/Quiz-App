import React, { useState } from "react";
import { LogIn, Lock, User, Eye, EyeOff } from "lucide-react";
import { speak } from "../services/speech/tts";

const HostLogin: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const handleLogin = () => {
    if (!username || !password) {
      alert("Please fill all fields");
      return;
    }
    alert(`Logging in as ${username}`);
  };

  return (
    <div className="min-h-screen bg-white text-gray-900">

      {/* HEADER */}
      <header className="sticky top-0 z-50 border-b border-gray-200 bg-white/95 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">

            {/* Logo + Title */}
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-blue-500 rounded-xl flex items-center justify-center shadow-sm">
                <span className="text-white font-bold text-lg">QV</span>
              </div>

              <h1 className="text-2xl font-bold bg-gradient-to-r from-gray-900 to-blue-600 bg-clip-text text-transparent">
                QuizVision
              </h1>

              <div className="h-8 w-px bg-gray-300 mx-4" />

              {/* Logos */}
              <div className="flex items-center space-x-6">

                <div className="w-12 h-12 bg-white rounded-lg flex items-center justify-center overflow-hidden">
                  <img
                    src="/images/ssn-logo.png"
                    alt="SSN Logo"
                    className="w-full h-full object-contain p-1"
                  />
                </div>

                <div className="w-16 h-16 bg-white rounded-lg flex items-center justify-center overflow-hidden">
                  <img
                    src="/images/meity.png"
                    alt="MeitY Logo"
                    className="w-full h-full object-contain p-1"
                  />
                </div>
              </div>
            </div>

            {/* Host Login button */}
            <button
              className="px-5 py-2.5 bg-gradient-to-r from-blue-600 to-blue-500 text-white rounded-lg shadow hover:from-blue-700 hover:to-blue-600 transition flex items-center space-x-2"
            >
              <LogIn size={18} />
              <span>Host Login</span>
            </button>
          </div>
        </div>
      </header>

      {/* MAIN CONTENT */}
      <main className="max-w-3xl mx-auto px-6 py-12">
        <div className="bg-white border border-gray-200 rounded-2xl shadow-sm p-10">

          <div className="text-center mb-10">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-2xl mb-4">
              <LogIn className="text-blue-600" size={32} />
            </div>

            <h2 className="text-3xl font-bold">Host Login</h2>
            <p className="text-gray-600 mt-2">
              Login to create and host quizzes securely.
            </p>
          </div>

          {/* Username */}
          <div className="mb-6">
            <label className="text-sm font-medium text-gray-800 mb-2 block">
              Username / Email
            </label>

            <div className="relative">
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                onFocus={() => speak("Enter username or email")}
                placeholder="Enter your username"
                className="w-full px-6 py-4 bg-gray-50 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none"
              />
              <User className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500" />
            </div>
          </div>

          {/* Password */}
          <div className="mb-8">
            <label className="text-sm font-medium text-gray-800 mb-2 block">
              Password
            </label>

            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                onFocus={() => speak("Enter password")}
                placeholder="Enter your password"
                className="w-full px-6 py-4 bg-gray-50 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none"
              />

              <button
                type="button"
                className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-600"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>

              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
            </div>

            <button
              className="text-sm text-blue-600 mt-2 hover:text-blue-700"
              onClick={() => alert("Forgot Password clicked")}
            >
              Forgot Password?
            </button>
          </div>

          {/* Login Button */}
          <button
            onClick={handleLogin}
            className="w-full py-4 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600 text-white font-semibold rounded-xl shadow hover:shadow-md transition"
          >
            Login
          </button>
        </div>
      </main>

      {/* FOOTER */}
      <footer className="border-t border-gray-200 bg-white mt-20">
        <div className="max-w-7xl mx-auto px-6 py-8 flex flex-col md:flex-row justify-between items-center">

          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-blue-500 rounded-xl flex items-center justify-center">
              <span className="text-white font-bold">QV</span>
            </div>

            <div>
              <p className="text-sm font-medium text-gray-900">QuizVision • NLT Mission</p>
              <p className="text-xs text-gray-600">
                An initiative by the Government of India
              </p>
            </div>
          </div>

          <p className="text-sm text-gray-600 mt-4 md:mt-0">
            © {new Date().getFullYear()} QuizVision – All Rights Reserved
          </p>

        </div>
      </footer>

    </div>
  );
};

export default HostLogin;
