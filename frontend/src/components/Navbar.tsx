import React from "react";
import { LogIn } from "lucide-react";
import { Link } from "react-router-dom";
import { speak } from "../services/speech/tts";

const Navbar: React.FC = () => {
  return (
    <div>
      {/* Header with subtle accent */}
      <header className="sticky top-0 z-50 border-b border-gray-100 bg-white/95 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            
            {/* Logo and Brand */}
            <div className="flex items-center space-x-6">
              <div className="flex items-center space-x-3">
                <Link to = "/">
                <h1
                  className="text-3xl font-bold tracking-[0.06em] text-sky-700 dark:text-teal-300"
                  style={{ fontFamily: '"Sora", "Outfit", "Avenir Next", "Segoe UI", sans-serif' }}
                >
                  Shravya
                </h1>
                </Link>
              </div>

              {/* Divider */}
              <div className="h-8 w-px bg-gray-200"></div>

              {/* Organization Logos */}
              <div className="flex items-center gap-4 px-1 py-1">

                {/* SSN Logo */}
                <div className="h-12 w-14 flex items-center justify-center overflow-hidden">
                  <img
                    src="/images/ssn-logo.png"
                    alt="SSN Logo"
                    className="w-full h-full object-contain"
                  />
                </div>

                {/* MeitY Logo */}
                <div className="h-14 w-28 flex items-center justify-center overflow-hidden">
                  <img
                    src="/images/meity.png"
                    alt="MeitY Logo"
                    className="h-full w-full object-contain"
                  />
                </div>
              </div>
            </div>

           <Link
            to="/auth"
            tabIndex={0}
            onFocus={() => speak("Host Login")}
            className="px-5 py-2.5 bg-gradient-to-r from-[#2563eb] to-[#3b82f6] 
                        hover:from-[#1d4ed8] hover:to-[#2563eb] 
                        text-white font-medium rounded-lg shadow-sm 
                        flex items-center space-x-2 group"
            >
            <LogIn size={18} />
            <span className="text-sm">Host Login</span>
            </Link>

          </div>
        </div>
      </header>
    </div>
  );
};

export default Navbar;
