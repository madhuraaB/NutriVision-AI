import {
    FaBrain,
    FaUtensils,
    FaChartPie,
    FaHeart
} from "react-icons/fa";

const About = () => {

    const foods = [
        "Aloo Matar",
        "Besan Cheela",
        "Biryani",
        "Chapathi",
        "Chole Bhature",
        "Dal",
        "Dhokla",
        "Dosa",
        "Gulab Jamun",
        "Idli",
        "Jalebi",
        "Kadai Paneer",
        "Naan",
        "Pani Puri",
        "Pakoda",
        "Pav Bhaji",
        "Poha",
        "Rolls",
        "Samosa",
        "Vada Pav"
    ];

    const features = [
        {
            icon: <FaBrain />,
            title: "AI Food Recognition",
            description:
                "Identifies Indian food from an uploaded image using an AI-based image classification model."
        },
        {
            icon: <FaChartPie />,
            title: "Nutrition Analysis",
            description:
                "Provides calories, protein, carbohydrates and fat information for the detected food."
        },
        {
            icon: <FaHeart />,
            title: "Health Insights",
            description:
                "Generates a nutrition score and simple recommendations based on the food's nutritional profile."
        }
    ];

    return (
        <section
            id="about"
            className="px-6 py-20 bg-[#0F172A]"
        >
            <div className="max-w-6xl mx-auto">

                {/* Heading */}
                <div className="text-center mb-12">

                    <p className="text-green-400 font-semibold tracking-wider uppercase text-sm">
                        About NutriVision AI
                    </p>

                    <h2 className="text-3xl md:text-4xl font-bold text-white mt-3">
                        Understand Your Food Better
                    </h2>

                    <p className="text-gray-400 max-w-2xl mx-auto mt-4 leading-relaxed">
                        NutriVision AI is an AI-powered Indian food recognition
                        and nutrition analysis platform. Upload a food image to
                        identify the dish, explore its nutritional information,
                        view a health score, and receive a simple nutrition insight.
                    </p>

                </div>


                {/* Feature Cards */}
                <div className="grid md:grid-cols-3 gap-6 mb-14">

                    {features.map((feature, index) => (
                        <div
                            key={index}
                            className="
                                bg-[#1E293B]
                                border border-gray-800
                                rounded-2xl
                                p-6
                                text-center
                                hover:border-green-500/40
                                hover:-translate-y-1
                                transition-all
                                duration-300
                            "
                        >

                            <div className="
                                w-14 h-14
                                mx-auto
                                rounded-full
                                bg-green-500/10
                                flex items-center justify-center
                                text-green-400
                                text-2xl
                            ">
                                {feature.icon}
                            </div>

                            <h3 className="text-white font-bold text-lg mt-5">
                                {feature.title}
                            </h3>

                            <p className="text-gray-400 text-sm leading-relaxed mt-3">
                                {feature.description}
                            </p>

                        </div>
                    ))}

                </div>


                {/* Supported Foods */}
                <div className="
                    bg-[#1E293B]
                    border border-gray-800
                    rounded-2xl
                    p-7 md:p-9
                ">

                    <div className="flex items-center gap-3 mb-5">

                        <div className="
                            w-11 h-11
                            rounded-full
                            bg-green-500/10
                            flex items-center justify-center
                        ">
                            <FaUtensils className="text-green-400" />
                        </div>

                        <div>
                            <h3 className="text-xl font-bold text-white">
                                Currently Supported Foods
                            </h3>

                            <p className="text-gray-500 text-sm">
                                20 Indian food categories
                            </p>
                        </div>

                    </div>


                    <div className="flex flex-wrap gap-3">

                        {foods.map((food, index) => (
                            <span
                                key={index}
                                className="
                                    px-4 py-2
                                    rounded-full
                                    bg-[#0F172A]
                                    border border-gray-700
                                    text-gray-300
                                    text-sm
                                    hover:border-green-500/50
                                    hover:text-green-400
                                    transition
                                "
                            >
                                {food}
                            </span>
                        ))}

                    </div>

                    <p className="text-gray-500 text-sm mt-6">
                        The current model is trained specifically on these
                        categories. Images outside these categories may produce
                        inaccurate or unsupported predictions.
                    </p>

                </div>

            </div>
        </section>
    );
};

export default About;