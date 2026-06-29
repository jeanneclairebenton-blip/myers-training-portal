
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
