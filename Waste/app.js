const form = document.getElementById('guide-form');
const resultSection = document.getElementById('result');
const resultTitle = document.getElementById('result-title');
const resultText = document.getElementById('result-text');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const item = document.getElementById('item').value.trim();
    const category = document.getElementById('category').value;
    const context = document.getElementById('context').value.trim();

    if (!item) return alert("Please enter an item name");

    // Show loading
    resultSection.style.display = 'block';
    resultTitle.textContent = 'Generating...';
    resultText.textContent = 'Please wait while we fetch the guide.';

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ item, category, context })
        });

        if (!response.ok) throw new Error('Server error');

        const data = await response.json();
        resultTitle.textContent = `Guide for: ${item}`;
        resultText.textContent = data.guide;
    } catch (err) {
        resultTitle.textContent = 'Error';
        resultText.textContent = 'Failed to generate guide. Try again later.';
        console.error(err);
    }
});