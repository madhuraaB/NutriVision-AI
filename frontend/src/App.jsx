import Navbar from "./components/Navbar/Navbar";
import Hero from "./components/Hero/Hero";
import Upload from "./components/Upload/Upload";

function App() {
  return (
    <div className="bg-[#0F172A] min-h-screen">
      <Navbar />
      <Hero />
      <Upload />
    </div>
  );
}

export default App;