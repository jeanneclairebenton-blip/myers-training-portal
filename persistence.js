
// Auto-Save and Load functionality for Myers Agent Training Modules
document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('input, textarea');
    
    // Load saved data
    inputs.forEach(input => {
        if (!input.id) return;
        
        // Only target inputs related to user progress
        if (input.type === 'hidden' || input.id.startsWith('search')) return;
        
        const storageKey = 'myers_' + window.location.pathname.split('/').pop() + '_' + input.id;
        const savedValue = localStorage.getItem(storageKey);
        
        if (savedValue !== null) {
            if (input.type === 'checkbox' || input.type === 'radio') {
                input.checked = savedValue === 'true';
            } else {
                input.value = savedValue;
            }
            
            // Dispatch input event so UI updates (like char counters)
            input.dispatchEvent(new Event('input', { bubbles: true }));
        }
        
        // Add event listeners to save data
        const saveFunc = () => {
            if (input.type === 'checkbox' || input.type === 'radio') {
                localStorage.setItem(storageKey, input.checked);
            } else {
                localStorage.setItem(storageKey, input.value);
            }
            if (typeof checkProve === 'function') {
                checkProve();
            }
        };
        
        input.addEventListener('input', saveFunc);
        input.addEventListener('change', saveFunc);
    });
    
    // Trigger any validation functions like checkProve if they exist
    if (typeof checkProve === 'function') {
        checkProve();
    }
});

// --- ZOHO WEBHOOK INTEGRATION ---
// Sends agent progress to Zoho Flow / CRM when they submit a module
document.addEventListener('click', (e) => {
    if (e.target && e.target.id === 'submitBtn') {
        // Wait a tiny bit for the native submitModule() to run its validation
        setTimeout(() => {
            // Check if the button was successfully disabled (meaning validation passed)
            if (e.target.disabled) {
                sendDataToZoho();
            }
        }, 100);
    }
});

function sendDataToZoho() {
    // ⚠️ REPLACE THIS URL WITH YOUR ACTUAL ZOHO FLOW WEBHOOK URL
    const ZOHO_WEBHOOK_URL = "https://flow.zoho.com/webhook/incoming?example";
    
    // Gather all inputs
    const inputs = document.querySelectorAll('input:not([type="hidden"]), textarea');
    const moduleData = {};
    
    inputs.forEach(input => {
        let label = input.placeholder || input.name || input.id;
        
        // Try to find an associated label tag
        if (input.labels && input.labels.length > 0) {
            label = input.labels[0].innerText;
        } else if (input.previousElementSibling && input.previousElementSibling.tagName === 'LABEL') {
            label = input.previousElementSibling.innerText;
        }
        
        if (input.type === 'checkbox' || input.type === 'radio') {
            moduleData[label] = input.checked;
        } else {
            moduleData[label] = input.value;
        }
    });

    const payload = {
        agent_name: "Agent Name (can be passed via URL params in Zoho)",
        module_title: document.title,
        module_path: window.location.pathname.split('/').pop(),
        submission_time: new Date().toISOString(),
        answers: moduleData
    };

    console.log("Sending to Zoho:", payload);

    // Send the data
    fetch(ZOHO_WEBHOOK_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
    }).then(response => {
        console.log("Zoho Webhook Success:", response);
    }).catch(error => {
        console.error("Zoho Webhook Error:", error);
    });
}
