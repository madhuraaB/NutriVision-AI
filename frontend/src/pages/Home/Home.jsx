import Navbar from "../../components/Navbar/Navbar";

function Home() {
  return (
    <div className="min-h-screen bg-slate-950 text-white">

      <Navbar />

      <div className="flex justify-center items-center h-[80vh]">

        <h1 className="text-6xl font-bold">
          NutritionAI
        </h1>

      </div>

    </div>
  );
}

export default Home;