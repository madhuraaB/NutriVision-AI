import { FaCloudUploadAlt } from "react-icons/fa";

const Hero = () => {
    return (
        <section className="text-center px-6 py-20">
            <div className="max-w-4xl mx-auto">

                <h1 className="text-6xl font-extrabold text-white mb-6">
                    Nutrition Analysis
                    <span className="text-green-400"> using AI</span>
                </h1>

                <p className="text-gray-400 text-xl mb-10">
                    Upload an image of your Indian meal and instantly get
                    nutrition facts, calories, health score and AI-powered
                    recommendations.
                </p>

                <a
                    href="#upload"
                    className="bg-green-500 hover:bg-green-600 transition px-8 py-4 rounded-xl text-white font-semibold text-lg flex items-center gap-3 mx-auto shadow-lg w-fit"
                >
                    <FaCloudUploadAlt size={24} />
                    Upload Food Image
                </a>

            </div>
        </section>
    );
};

export default Hero;