'use client'

import { useState } from 'react';

const CommandInput = ({ onSendCommand }) => {
    const [prompt, setPrompt] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await fetch('/api/generate-code', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt }),
        });
        const result = await response.json();
        onSendCommand(result.code);
        setPrompt("");
    };

    return (
        <form onSubmit={handleSubmit} className="p-4">
            <input
                type="text"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Enter command for Finch"
                className="border p-2 w-full"
            />
            <button type="submit" className="bg-blue-500 text-white p-2 mt-2">
                Generate Code
            </button>
        </form>
    );
};

export default CommandInput;
