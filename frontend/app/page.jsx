'use client'

import { useState } from 'react';
import axios from 'axios';

export default function Home() {
    const [prompt, setPrompt] = useState("");
    const [generatedCode, setGeneratedCode] = useState("");
    const [executionResult, setExecutionResult] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5001/process-natural-language', {
                prompt,
            });
            setGeneratedCode(response.data.code);
            setExecutionResult(response.data.execution_result);
        } catch (error) {
            console.error(error);
            setExecutionResult("Error executing commands. Please try again.");
        }
    };

    return (
        <div className="p-8">
            <h1 className="text-2xl font-bold mb-4">Finch Robot Command Center</h1>
            <form onSubmit={handleSubmit} className="mb-6">
                <textarea
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="Describe what you want the Finch robot to do..."
                    className="border p-2 w-full h-32 mb-4 text-black"
                />
                <button
                    type="submit"
                    className="bg-blue-500 text-white p-2 rounded"
                >
                    Execute Commands
                </button>
            </form>
            <div>
                <h2 className="text-lg font-semibold">Generated Python Code:</h2>
                <pre className="bg-black p-4 border rounded">{generatedCode}</pre>
                <h2 className="text-lg font-semibold mt-4">Execution Result:</h2>
                <pre className="bg-black p-4 border rounded">{executionResult}</pre>
            </div>
        </div>
    );
}
