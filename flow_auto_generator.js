// Google Flow Batch Image Generator
// This script generates images via Google Flow's UI

const PROMPTS = [
    // News 1-3 examples
    {
        title: "PolyAI's ex-machine learning chief raises $20m for new robotics startup",
        prompts: [
            "Cinematic editorial photograph of PolyAI's ex-machine learning chief raises $20m for new robotics startup, professional studio lighting, futuristic tech entrepreneur, high-end office background, ultra-detailed, 16:9",
            "Futuristic documentary wide shot showing PolyAI's ex-machine learning chief raises $20m for new robotics startup, sleek robotics lab, holographic displays, cinematic lighting, photorealistic, 16:9"
        ]
    },
    // Add more prompts as needed...
];

async function waitForElement(selector, timeout = 10000) {
    const start = Date.now();
    while (Date.now() - start < timeout) {
        const el = document.querySelector(selector);
        if (el) return el;
        await new Promise(r => setTimeout(r, 500));
    }
    throw new Error(`Element ${selector} not found within ${timeout}ms`);
}

async function generateImage(prompt, index) {
    console.log(`Generating image ${index} for: ${prompt.substring(0, 50)}...`);
    
    try {
        // Click new project or use existing
        let newProjectBtn = document.querySelector('[data-testid="new-project-button"]') || 
                           document.querySelector('button[aria-label="New project"]');
        if (newProjectBtn) {
            newProjectBtn.click();
            await new Promise(r => setTimeout(r, 2000));
        }
        
        // Find the prompt/text input area
        let promptInput = document.querySelector('textarea[placeholder*="Describe"]') ||
                         document.querySelector('[aria-label="Prompt"] textarea') ||
                         document.querySelector('input[type="text"]');
        
        if (!promptInput) {
            console.log('Prompt input not found, trying alternative selectors');
        }
        
        // Try to type the prompt
        if (promptInput) {
            promptInput.focus();
            promptInput.value = prompt;
            promptInput.dispatchEvent(new Event('input', { bubbles: true }));
            promptInput.dispatchEvent(new Event('change', { bubbles: true }));
        }
        
        // Find generate button
        let generateBtn = document.querySelector('[data-testid="generate-button"]') ||
                         document.querySelector('button[aria-label="Generate"]') ||
                         document.querySelector('button[aria-label*="Generate"]');
        
        if (generateBtn) {
            generateBtn.click();
            console.log('Clicked generate button, waiting for results...');
            await new Promise(r => setTimeout(r, 15000));
        } else {
            console.log('Generate button not found, trying Enter key');
            document.querySelector('body').dispatchEvent(new KeyboardEvent('keydown', {'key': 'Enter'}));
            document.querySelector('body').dispatchEvent(new KeyboardEvent('keyup', {'key': 'Enter'}));
        }
        
        return { success: true, index };
    } catch (error) {
        console.error(`Error generating image ${index}:`, error);
        return { success: false, index, error: error.message };
    }
}

async function downloadImage(index) {
    // Try to find download button for the generated image
    try {
        // Find image download options
        let downloadBtn = document.querySelector('[aria-label*="Download"]') ||
                         document.querySelector('[data-testid="download-button"]') ||
                         document.querySelector('button[title*="Download"]');
        
        if (downloadBtn) {
            downloadBtn.click();
            console.log(`Downloaded image ${index}`);
            return true;
        }
    } catch (error) {
        console.error(`Download error for image ${index}:`, error);
    }
    return false;
}

// Export for use in browser console
window.FlowBatchGenerator = {
    generateImage,
    downloadImage,
    waitForElement
};

console.log("Flow Batch Generator loaded. Use FlowBatchGenerator.generateImage(prompt, index)");