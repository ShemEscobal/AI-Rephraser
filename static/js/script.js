
document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const originalTextArea = document.getElementById('original-text');
    const paraphrasedTextArea = document.getElementById('paraphrased-text');
    const academicLevelSelect = document.getElementById('academic-level');
    const paraphraseBtn = document.getElementById('paraphrase-btn');
    const clearBtn = document.getElementById('clear-btn');
    const copyBtn = document.getElementById('copy-btn');
    const wordCountSpan = document.getElementById('word-count');
    const loadingDiv = document.getElementById('loading');
    const resultContainer = document.getElementById('result-container');
    const testApiBtn = document.getElementById('test-api-btn');
    const apiTestResult = document.getElementById('api-test-result');
    
    // Update word count
    function updateWordCount() {
        const text = originalTextArea.value.trim();
        const wordCount = text ? text.split(/\s+/).length : 0;
        wordCountSpan.textContent = `${wordCount} word${wordCount !== 1 ? 's' : ''}`;
    }
    
    // Clear text
    clearBtn.addEventListener('click', function() {
        originalTextArea.value = '';
        updateWordCount();
        paraphrasedTextArea.value = '';
        copyBtn.disabled = true;
    });
    
    // Copy paraphrased text
    copyBtn.addEventListener('click', function() {
        paraphrasedTextArea.select();
        document.execCommand('copy');
        
        // Visual feedback
        paraphrasedTextArea.classList.add('highlight-copy');
        setTimeout(() => {
            paraphrasedTextArea.classList.remove('highlight-copy');
        }, 1000);
        
        // Change button text temporarily
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        setTimeout(() => {
            copyBtn.innerHTML = originalText;
        }, 2000);
    });
    
    // Test API connection
    testApiBtn.addEventListener('click', function() {
        // Disable button and show loading state
        testApiBtn.disabled = true;
        testApiBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Testing...';
        apiTestResult.innerHTML = '';
        
        // Call the test API endpoint
        fetch('/test-api')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    apiTestResult.innerHTML = `
                        <div class="alert alert-success">
                            <i class="fas fa-check-circle"></i> ${data.message}
                        </div>
                    `;
                } else {
                    apiTestResult.innerHTML = `
                        <div class="alert alert-danger">
                            <i class="fas fa-exclamation-triangle"></i> ${data.message}
                        </div>
                    `;
                }
            })
            .catch(error => {
                apiTestResult.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-triangle"></i> Error testing API: ${error.message}
                    </div>
                `;
            })
            .finally(() => {
                // Reset button state
                testApiBtn.disabled = false;
                testApiBtn.innerHTML = '<i class="fas fa-check-circle"></i> Test API Connection';
            });
    });
    
    // Word count update on input
    originalTextArea.addEventListener('input', updateWordCount);
    
    // Format error message for display
    function formatErrorMessage(error) {
        // Check if it's an API error with more details
        if (error.message.includes('API request error') || 
            error.message.includes('Failed to get proper response from API') ||
            error.message.includes('Authentication error')) {
            return `
                <div class="alert alert-danger">
                    <h5><i class="fas fa-exclamation-triangle"></i> API Error</h5>
                    <p>${error.message}</p>
                    <hr>
                    <p class="mb-0">Please check your API key or try again later.</p>
                </div>
            `;
        }
        
        return `
            <div class="alert alert-danger">
                <h5><i class="fas fa-exclamation-triangle"></i> Error</h5>
                <p>${error.message}</p>
            </div>
        `;
    }
    
    // Paraphrase text
    paraphraseBtn.addEventListener('click', function() {
        const originalText = originalTextArea.value.trim();
        const academicLevel = academicLevelSelect.value;
        
        if (!originalText) {
            alert('Please enter some text to paraphrase.');
            return;
        }
        
        // Show loading, hide result
        loadingDiv.classList.remove('d-none');
        resultContainer.style.display = 'none';
        paraphraseBtn.disabled = true;
        
        // Call API
        fetch('/paraphrase', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: originalText,
                academic_level: academicLevel
            }),
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'An error occurred while paraphrasing.');
                });
            }
            return response.json();
        })
        .then(data => {
            // Hide loading, show result
            loadingDiv.classList.add('d-none');
            resultContainer.style.display = 'block';
            
            // Update textarea with paraphrased text
            paraphrasedTextArea.value = data.paraphrased_text;
            
            // Enable copy button
            copyBtn.disabled = false;
        })
        .catch(error => {
            // Hide loading, show result with error
            loadingDiv.classList.add('d-none');
            resultContainer.style.display = 'block';
            
            // Show formatted error message
            if (error.message.includes('API') || error.message.includes('Failed') || error.message.includes('Authentication')) {
                // For API errors, display a formatted error message
                paraphrasedTextArea.value = '';
                resultContainer.innerHTML = formatErrorMessage(error);
            } else {
                // For other errors, just show in the textarea
                paraphrasedTextArea.value = `Error: ${error.message}`;
            }
            
            console.error('Error:', error);
        })
        .finally(() => {
            // Re-enable paraphrase button
            paraphraseBtn.disabled = false;
        });
    });
    
    // Initialize word count
    updateWordCount();
}); 
