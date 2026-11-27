#!/usr/bin/env python3
"""
Google Flow Batch Image Generator using browser automation
This script uses browser_mcp tools to navigate and generate images in Google Flow
"""

import json
import time
from datetime import datetime

# Project paths
PROJECT_DIR = "/data/user/0/ai.antigem/files/home/projects/AINews-KrishnaVibez"
PROMPTS_FILE = f"{PROJECT_DIR}/flow_prompts_to_generate.json"
STATE_FILE = f"{PROJECT_DIR}/.ainews_image_state.json"
UPLOAD_LOG = f"{PROJECT_DIR}/world_ai_images_uploaded.json"

def load_prompts():
    with open(PROMPTS_FILE, 'r') as f:
        return json.load(f)

def update_state(progress, total):
    state = {
        "last_run_timestamp": time.time(),
        "last_run_date": datetime.now().isoformat(),
        "total_news": 50,
        "total_images_to_generate": 100,
        "status": f"generating_{progress}_{total}",
        "progress": f"{progress}/{total}",
        "generated_count": progress
    }
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def save_upload_results(results):
    log = {
        "timestamp": datetime.now().isoformat(),
        "total_uploaded": len(results),
        "items": results
    }
    with open(UPLOAD_LOG, 'w') as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

# JavaScript code to run in browser
FLOW_JS = """
// Google Flow Automation Script
(async function() {
    const prompts = PROMPTS_TO_PROCESS;
    const results = [];
    
    console.log('Starting Google Flow batch generation...');
    console.log('Total prompts to process:', prompts.length);
    
    for (let i = 0; i < prompts.length; i++) {
        const item = prompts[i];
        console.log(\`Processing \${item.news_index}.\${item.image_num}: \${item.title}\`);
        
        try {
            // Try to find the text input for prompt
            // Google Flow typically has a textarea or input for the prompt
            const promptInputs = document.querySelectorAll('textarea, input[type="text"]');
            let promptInput = null;
            
            for (const input of promptInputs) {
                const placeholder = input.getAttribute('placeholder') || '';
                const ariaLabel = input.getAttribute('aria-label') || '';
                if (placeholder.toLowerCase().includes('describe') || 
                    ariaLabel.toLowerCase().includes('prompt') ||
                    input.value === '') {
                    promptInput = input;
                    break;
                }
            }
            
            // Alternative: look for specific Flow selectors
            if (!promptInput) {
                promptInput = document.querySelector('[data-testid="prompt-input"]') ||
                               document.querySelector('.prompt-input-area textarea') ||
                               document.querySelector('contenteditable[role="textbox"]') ||
                               promptInputs[0];
            }
            
            if (promptInput) {
                // Clear and set the prompt
                promptInput.focus();
                promptInput.value = '';
                promptInput.value = item.prompt;
                
                // Trigger input events
                promptInput.dispatchEvent(new Event('input', {bubbles: true}));
                promptInput.dispatchEvent(new Event('change', {bubbles: true}));
                
                // Wait for prompt to be set
                await new Promise(r => setTimeout(r, 500));
                
                // Find and click generate
                const generateBtn = document.querySelector('[data-testid="generate-button"]') ||
                                   document.querySelector('button[aria-label*="Generate"]') ||
                                   document.querySelector('.generate-button') ||
                                   document.querySelector('button[role="switch"]');
                
                if (generateBtn) {
                    generateBtn.click();
                    console.log(\`Clicked generate for image \${i+1}\`);
                    
                    // Wait for generation (Flow typically takes 10-30 seconds)
                    await new Promise(r => setTimeout(r, 25000));
                    
                    // Try to download
                    const downloadBtn = document.querySelector('[aria-label*="Download"]') ||
                                       document.querySelector('[data-testid="download-button"]') ||
                                       document.querySelector('.download-button');
                    
                    if (downloadBtn) {
                        downloadBtn.click();
                        console.log(\`Downloaded image \${i+1}\`);
                    }
                } else {
                    console.log(\`Generate button not found for image \${i+1}, trying Enter key\`);
                    document.querySelector('body').dispatchEvent(new KeyboardEvent('keydown', {'key': 'Enter'}));
                }
            } else {
                console.log(\`Prompt input not found for image \${i+1}\`);
            }
            
            results.push({
                news_index: item.news_index,
                image_num: item.image_num,
                title: item.title,
                category: item.category,
                status: 'processed',
                timestamp: new Date().toISOString()
            });
            
            // Update state
            window.updateFlowProgress(i + 1, prompts.length);
            
        } catch (error) {
            console.error(\`Error processing prompt \${i+1}:\`, error);
            results.push({
                news_index: item.news_index,
                image_num: item.image_num,
                title: item.title,
                category: item.category,
                status: 'error',
                error: error.message,
                timestamp: new Date().toISOString()
            });
        }
        
        // Small delay between images
        await new Promise(r => setTimeout(r, 2000));
    }
    
    console.log('Batch generation complete!');
    console.log('Results:', results.length);
    
    // Return results to Python
    return results;
})();
"""

if __name__ == "__main__":
    prompts = load_prompts()
    print(f"Loaded {len(prompts)} prompts to process")
    print(f"Categories: {set(p['category'] for p in prompts)}")