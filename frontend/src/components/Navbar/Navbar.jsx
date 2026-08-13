import { FaLeaf } from "react-icons/fa";

function Navbar() {
  return (
    <nav className="w-full bg-slate-900 border-b border-slate-800 shadow-md">
      <div className="max-w-7xl mx-auto px-8 py-5 flex justify-between items-center">

        {/* Logo */}

        <div className="flex items-center gap-3">

          <FaLeaf className="text-emerald-400 text-3xl" />

          <h1 className="text-2xl font-bold text-white">
            NutritionAI
          </h1>

        </div>

        {/* Menu */}

        <div className="hidden md:flex gap-10 text-slate-300">

          <a
            href="#"
            className="hover:text-emerald-400 transition"
          >
            Home
          </a>

          <a
            href="#"
            className="hover:text-emerald-400 transition"
          >
            Prediction
          </a>

          <a
            href="#"
            className="hover:text-emerald-400 transition"
          >
            About
          </a>

          <a
            href="#"
            className="hover:text-emerald-400 transition"
          >
            Contact
          </a>

        </div>

      </div>
    </nav>
  );
}

export default Navbar;