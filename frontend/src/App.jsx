import Navbar from "./components/Navbar/Navbar";
import Hero from "./components/Hero/Hero";
import Upload from "./components/Upload/Upload";
import About from "./components/About/About";

function App() {
  return (
    <div className="bg-[#0F172A] min-h-screen">

      <Navbar />

      <Hero />

      <Upload />

      <About />

    </div>
  );
}

export default App;