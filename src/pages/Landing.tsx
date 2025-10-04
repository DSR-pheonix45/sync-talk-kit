import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { ArrowRight, Bot, FileText, TrendingUp } from 'lucide-react';

export default function Landing() {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleGetStarted = () => {
    if (isAuthenticated) {
      navigate('/dashboard');
    } else {
      navigate('/login');
    }
  };

  return (
    <div className="min-h-screen bg-[#070B14] text-white">
      {/* Navigation */}
      <nav className="border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-[#00FFD1] rounded-lg flex items-center justify-center">
                <span className="text-xl font-bold text-black">D</span>
              </div>
              <span className="text-xl font-semibold">Datalis</span>
            </div>
            
            <div className="flex items-center space-x-4">
              {isAuthenticated ? (
                <Link
                  to="/dashboard"
                  className="px-4 py-2 rounded-md bg-[#00FFD1] text-black font-semibold hover:bg-[#00FFD1]/90"
                >
                  Dashboard
                </Link>
              ) : (
                <>
                  <Link
                    to="/login"
                    className="px-4 py-2 text-gray-300 hover:text-white"
                  >
                    Login
                  </Link>
                  <Link
                    to="/signup"
                    className="px-4 py-2 rounded-md bg-[#00FFD1] text-black font-semibold hover:bg-[#00FFD1]/90"
                  >
                    Sign Up
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-5xl md:text-7xl font-bold mb-6">
              Turn Data into
              <br />
              Actionable <span className="text-[#00FFD1]">Insights</span>
              <br />
              with AI
            </h1>
            <p className="text-xl text-gray-400 mb-10 max-w-2xl mx-auto">
              Let AI transform your business data into the insights you need
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button
                onClick={handleGetStarted}
                className="px-8 py-3 rounded-md bg-[#00FFD1] text-black font-semibold hover:bg-[#00FFD1]/90 flex items-center justify-center gap-2"
              >
                Try Datalis
                <ArrowRight className="h-5 w-5" />
              </button>
              <button className="px-8 py-3 rounded-md border border-gray-700 text-white hover:bg-gray-800">
                View Walkthrough
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <h2 className="text-3xl font-bold text-center mb-12">
          Transforming Financial Challenges
        </h2>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="p-6 rounded-lg bg-[#0B1221] border border-gray-800">
            <div className="w-12 h-12 rounded-lg bg-[#00FFD1]/10 flex items-center justify-center mb-4">
              <Bot className="h-6 w-6 text-[#00FFD1]" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Consultant Agent</h3>
            <p className="text-gray-400">
              From Questions to Strategy — Faster than Ever. Get AI-powered insights for budgeting, planning, and forecasting.
            </p>
          </div>
          
          <div className="p-6 rounded-lg bg-[#0B1221] border border-gray-800">
            <div className="w-12 h-12 rounded-lg bg-[#00FFD1]/10 flex items-center justify-center mb-4">
              <FileText className="h-6 w-6 text-[#00FFD1]" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Auditor Agent</h3>
            <p className="text-gray-400">
              From Data to Deductions — Audits Made Effortless. Compliant audit generation with smart checklists.
            </p>
          </div>
          
          <div className="p-6 rounded-lg bg-[#0B1221] border border-gray-800">
            <div className="w-12 h-12 rounded-lg bg-[#00FFD1]/10 flex items-center justify-center mb-4">
              <TrendingUp className="h-6 w-6 text-[#00FFD1]" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Taxation Agent</h3>
            <p className="text-gray-400">
              Simplify Tax. Maximize Compliance. Automate tax prep, filings, and reconciliation.
            </p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div className="bg-gradient-to-r from-[#00FFD1]/10 to-transparent rounded-2xl p-12 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to get started?</h2>
          <p className="text-gray-400 mb-8">
            Join thousands of businesses transforming their data into insights
          </p>
          <button
            onClick={handleGetStarted}
            className="px-8 py-3 rounded-md bg-[#00FFD1] text-black font-semibold hover:bg-[#00FFD1]/90"
          >
            Get Started for Free
          </button>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-400">
            <p>&copy; 2025 Datalis. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
