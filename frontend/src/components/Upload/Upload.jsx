import { useState } from "react";

import {
    FaCloudUploadAlt,
    FaFire,
    FaDrumstickBite,
    FaBreadSlice,
    FaTint,
    FaRobot,
    FaRedo
} from "react-icons/fa";

const Upload = () => {

    const [selectedFile, setSelectedFile] = useState(null);
    const [selectedImage, setSelectedImage] = useState(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleImageChange = (e) => {

        const file = e.target.files[0];

        if (file) {

            setSelectedFile(file);
            setSelectedImage(URL.createObjectURL(file));

            setResult(null);
            setError(null);
        }
    };

    const handleAnalyze = async () => {

        if (!selectedFile) return;

        setLoading(true);
        setError(null);
        setResult(null);

        try {

            const formData = new FormData();

            formData.append("file", selectedFile);

            const response = await fetch(
                "http://127.0.0.1:8000/predict",
                {
                    method: "POST",
                    body: formData
                }
            );

            if (!response.ok) {
                throw new Error("Prediction failed");
            }

            const data = await response.json();

            console.log("Prediction result:", data);

            if (data.error) {
                throw new Error(data.error);
            }

            setResult(data);

        } catch (err) {

            console.error(err);

            setError(
                "Failed to analyze image. Please try again."
            );

        } finally {

            setLoading(false);
        }
    };

    const handleRemove = () => {

        setSelectedFile(null);
        setSelectedImage(null);
        setResult(null);
        setError(null);
    };

    const formatFoodName = (name) => {

        return name
            ? name.replaceAll("_", " ")
            : "";
    };

    return (

        <section
            id="upload"
            className="flex justify-center px-6 py-12"
        >

            <div className="w-full max-w-5xl">

                {/* =========================
                    UPLOAD BOX
                ========================= */}

                {!selectedImage && (

                    <label
                        htmlFor="image-upload"
                        className="
                            border-2 border-dashed
                            border-green-500
                            rounded-2xl
                            bg-[#1E293B]
                            hover:bg-[#243447]
                            transition
                            cursor-pointer
                            flex flex-col
                            items-center
                            justify-center
                            py-16
                        "
                    >

                        <FaCloudUploadAlt
                            size={65}
                            className="text-green-400 mb-5"
                        />

                        <h2 className="text-2xl font-bold text-white">
                            Upload Food Image
                        </h2>

                        <p className="text-gray-400 mt-2">
                            JPG • JPEG • PNG
                        </p>

                        <span
                            className="
                                mt-6
                                bg-green-500
                                hover:bg-green-600
                                px-7 py-3
                                rounded-lg
                                text-white
                                font-semibold
                            "
                        >
                            Choose Image
                        </span>

                    </label>
                )}

                <input
                    id="image-upload"
                    type="file"
                    accept="image/jpeg,image/jpg,image/png"
                    className="hidden"
                    onChange={handleImageChange}
                />

                {/* =========================
                    IMAGE PREVIEW
                ========================= */}

                {selectedImage && !result && (

                    <div className="bg-[#1E293B] rounded-2xl p-6">

                        <h2 className="text-white text-xl font-bold mb-5">
                            Image Preview
                        </h2>

                        <img
                            src={selectedImage}
                            alt="Selected food"
                            className="
                                rounded-xl
                                w-full
                                max-h-[400px]
                                object-contain
                                border border-gray-700
                            "
                        />

                        <div className="flex justify-center gap-4 mt-8">

                            <button
                                onClick={handleAnalyze}
                                disabled={loading}
                                className="
                                    bg-green-500
                                    hover:bg-green-600
                                    disabled:bg-gray-600
                                    px-10 py-4
                                    rounded-xl
                                    text-lg
                                    font-semibold
                                    text-white
                                    transition
                                "
                            >

                                {loading
                                    ? "Analyzing..."
                                    : "🔍 Analyze Food"}

                            </button>

                            <button
                                onClick={handleRemove}
                                disabled={loading}
                                className="
                                    bg-gray-600
                                    hover:bg-gray-700
                                    px-8 py-4
                                    rounded-xl
                                    text-lg
                                    font-semibold
                                    text-white
                                "
                            >
                                Remove
                            </button>

                        </div>

                        {error && (

                            <p className="text-red-400 text-center mt-5">
                                {error}
                            </p>

                        )}

                    </div>
                )}

                {/* =========================
                    RESULT
                ========================= */}

                {result && result.food && (

                    <div className="mt-6">

                        {/* HEADING */}

                        <div className="mb-6">

                            <h2 className="text-3xl font-bold text-white">
                                Nutrition Analysis
                            </h2>

                            <p className="text-gray-400 mt-1">
                                AI-powered analysis of your food
                            </p>

                        </div>


                        {/* =========================
                            FOOD DETECTED
                        ========================= */}

                        <div className="
                            bg-[#1E293B]
                            rounded-2xl
                            p-6
                            shadow-lg
                        ">

                            <div className="
                                flex
                                flex-col
                                md:flex-row
                                gap-8
                                items-center
                            ">

                                {/* SMALLER IMAGE */}

                                <img
                                    src={selectedImage}
                                    alt={result.food}
                                    className="
                                        w-full
                                        md:w-56
                                        h-48
                                        object-cover
                                        rounded-xl
                                    "
                                />

                                <div className="flex-1 w-full">

                                    <p className="
                                        text-green-400
                                        font-semibold
                                        tracking-wide
                                    ">
                                        FOOD DETECTED
                                    </p>

                                    <h2 className="
                                        text-4xl
                                        font-bold
                                        text-white
                                        mt-2
                                    ">
                                        {formatFoodName(result.food)}
                                    </h2>

                                    {/* CONFIDENCE */}

                                    <div className="mt-4">

                                        <div className="
                                            flex
                                            justify-between
                                            text-sm
                                            mb-2
                                        ">

                                            <span className="text-gray-400">
                                                AI Confidence
                                            </span>

                                            <span className="
                                                text-green-400
                                                font-semibold
                                            ">
                                                {(result.confidence * 100).toFixed(2)}%
                                            </span>

                                        </div>

                                        <div className="
                                            w-full
                                            h-2
                                            bg-gray-700
                                            rounded-full
                                            overflow-hidden
                                        ">

                                            <div
                                                className="
                                                    h-full
                                                    bg-green-400
                                                    rounded-full
                                                "
                                                style={{
                                                    width: `${Math.min(
                                                        result.confidence * 100,
                                                        100
                                                    )}%`
                                                }}
                                            />

                                        </div>

                                    </div>

                                </div>

                            </div>

                        </div>


                        {/* =========================
                            NUTRITION CARDS
                        ========================= */}

                        {result.nutrition && (

                            <div className="
                                grid
                                grid-cols-2
                                md:grid-cols-4
                                gap-4
                                mt-6
                            ">

                                {/* CALORIES */}

                                <div className="
                                    bg-[#1E293B]
                                    rounded-xl
                                    p-5
                                    text-center
                                ">

                                    <FaFire
                                        className="
                                            text-orange-400
                                            text-2xl
                                            mx-auto
                                        "
                                    />

                                    <p className="text-gray-400 mt-2">
                                        Calories
                                    </p>

                                    <p className="
                                        text-2xl
                                        font-bold
                                        text-orange-400
                                        mt-2
                                    ">
                                        {result.nutrition.calories}
                                    </p>

                                    <p className="text-gray-500 text-sm">
                                        kcal
                                    </p>

                                </div>


                                {/* PROTEIN */}

                                <div className="
                                    bg-[#1E293B]
                                    rounded-xl
                                    p-5
                                    text-center
                                ">

                                    <FaDrumstickBite
                                        className="
                                            text-blue-400
                                            text-2xl
                                            mx-auto
                                        "
                                    />

                                    <p className="text-gray-400 mt-2">
                                        Protein
                                    </p>

                                    <p className="
                                        text-2xl
                                        font-bold
                                        text-blue-400
                                        mt-2
                                    ">
                                        {result.nutrition.protein}
                                    </p>

                                    <p className="text-gray-500 text-sm">
                                        grams
                                    </p>

                                </div>


                                {/* CARBS */}

                                <div className="
                                    bg-[#1E293B]
                                    rounded-xl
                                    p-5
                                    text-center
                                ">

                                    <FaBreadSlice
                                        className="
                                            text-yellow-400
                                            text-2xl
                                            mx-auto
                                        "
                                    />

                                    <p className="text-gray-400 mt-2">
                                        Carbs
                                    </p>

                                    <p className="
                                        text-2xl
                                        font-bold
                                        text-yellow-400
                                        mt-2
                                    ">
                                        {result.nutrition.carbs}
                                    </p>

                                    <p className="text-gray-500 text-sm">
                                        grams
                                    </p>

                                </div>


                                {/* FAT */}

                                <div className="
                                    bg-[#1E293B]
                                    rounded-xl
                                    p-5
                                    text-center
                                ">

                                    <FaTint
                                        className="
                                            text-red-400
                                            text-2xl
                                            mx-auto
                                        "
                                    />

                                    <p className="text-gray-400 mt-2">
                                        Fat
                                    </p>

                                    <p className="
                                        text-2xl
                                        font-bold
                                        text-red-400
                                        mt-2
                                    ">
                                        {result.nutrition.fat}
                                    </p>

                                    <p className="text-gray-500 text-sm">
                                        grams
                                    </p>

                                </div>

                            </div>
                        )}


                        {/* =========================
                            HEALTH SCORE
                        ========================= */}

                        {result.health_score !== undefined && (

                            <div className="
                                bg-[#1E293B]
                                rounded-2xl
                                p-8
                                mt-6
                                text-center
                            ">

                                <p className="text-gray-400 text-lg">
                                    Health Score
                                </p>

                                <div className="
                                    flex
                                    justify-center
                                    mt-5
                                ">

                                    <div
                                        className="
                                            w-36
                                            h-36
                                            rounded-full
                                            flex
                                            items-center
                                            justify-center
                                        "
                                        style={{
                                            background: `conic-gradient(
                                                #22c55e ${result.health_score * 3.6}deg,
                                                #334155 ${result.health_score * 3.6}deg
                                            )`
                                        }}
                                    >

                                        <div className="
                                            w-28
                                            h-28
                                            rounded-full
                                            bg-[#1E293B]
                                            flex
                                            flex-col
                                            items-center
                                            justify-center
                                        ">

                                            <span className="
                                                text-4xl
                                                font-bold
                                                text-green-400
                                            ">
                                                {result.health_score}
                                            </span>

                                            <span className="
                                                text-gray-500
                                                text-sm
                                            ">
                                                / 100
                                            </span>

                                        </div>

                                    </div>

                                </div>

                            </div>
                        )}


                        {/* =========================
                            AI RECOMMENDATION
                        ========================= */}

                        {result.recommendation && (

                            <div className="
                                bg-[#1E293B]
                                border
                                border-green-500/20
                                rounded-2xl
                                p-7
                                mt-6
                                shadow-lg
                            ">

                                <div className="
                                    flex
                                    items-center
                                    gap-3
                                ">

                                    <div className="
                                        w-11
                                        h-11
                                        rounded-full
                                        bg-green-500/10
                                        flex
                                        items-center
                                        justify-center
                                    ">

                                        <FaRobot className="
                                            text-green-400
                                            text-xl
                                        "/>

                                    </div>

                                    <div>

                                        <h3 className="
                                            text-xl
                                            font-bold
                                            text-green-400
                                        ">
                                            AI Nutrition Insight
                                        </h3>

                                        <p className="
                                            text-gray-500
                                            text-sm
                                        ">
                                            Personalized recommendation
                                        </p>

                                    </div>

                                </div>

                                <p className="
                                    text-gray-300
                                    mt-5
                                    leading-relaxed
                                    text-lg
                                ">
                                    {result.recommendation}
                                </p>

                            </div>
                        )}


                        {/* =========================
                            ANALYZE ANOTHER
                        ========================= */}

                        <div className="
                            flex
                            justify-center
                            mt-8
                            mb-6
                        ">

                            <button
                                onClick={handleRemove}
                                className="
                                    bg-green-500
                                    hover:bg-green-600
                                    px-8
                                    py-3
                                    rounded-xl
                                    text-white
                                    font-semibold
                                    flex
                                    items-center
                                    gap-2
                                    transition
                                "
                            >

                                <FaRedo />

                                Analyze Another Image

                            </button>

                        </div>

                    </div>
                )}


                {/* =========================
                    UNSUPPORTED FOOD
                ========================= */}

                {result && !result.food && (

                    <div className="
                        bg-[#1E293B]
                        rounded-2xl
                        p-8
                        mt-6
                        text-center
                    ">

                        <p className="
                            text-yellow-400
                            text-xl
                            font-semibold
                        ">
                            ⚠️ {result.message || "Food not supported"}
                        </p>

                        <button
                            onClick={handleRemove}
                            className="
                                mt-6
                                bg-green-500
                                hover:bg-green-600
                                px-8
                                py-3
                                rounded-xl
                                text-white
                                font-semibold
                            "
                        >
                            Try Another Image
                        </button>

                    </div>
                )}

            </div>

        </section>
    );
};

export default Upload;