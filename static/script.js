let editor;

require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs' }});
require(['vs/editor/editor.main'], function() {
    editor = monaco.editor.create(document.getElementById('editor-container'), {
        value: [
            'function calculateSum(arr) {',
            '    let sum = 0;',
            '    for(let i=0; i <= arr.length; i++) { // Bug here',
            '        sum += arr[i];',
            '    }',
            '    return sum;',
            '}',
            '',
            'console.log(calculateSum([1, 2, 3]));'
        ].join('\n'),
        language: 'javascript',
        theme: 'vs-dark',
        automaticLayout: true,
        minimap: { enabled: false },
        fontSize: 14,
        fontFamily: "'JetBrains Mono', monospace"
    });

    document.getElementById('language-select').addEventListener('change', (e) => {
        monaco.editor.setModelLanguage(editor.getModel(), e.target.value);
    });
});

// Tab switching logic
const tabs = document.querySelectorAll('.tab-btn');
const contents = document.querySelectorAll('.tab-content');

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        contents.forEach(c => c.classList.remove('active'));
        
        tab.classList.add('active');
        document.getElementById(tab.dataset.target).classList.add('active');
    });
});

// Analyze Code
document.getElementById('analyze-btn').addEventListener('click', async () => {
    const code = editor.getValue();
    const language = document.getElementById('language-select').value;
    
    if(!code.trim()) return alert("Please enter some code to analyze.");

    // UI state
    document.getElementById('loading').classList.remove('hidden');
    contents.forEach(c => c.classList.add('hidden')); // hide text content
    document.getElementById('analyze-btn').disabled = true;

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code, language })
        });

        const data = await response.json();
        
        if(response.ok) {
            // Simple markdown formatter since we don't have a library
            const formatMD = (text) => text
                .replace(/^### (.*$)/gim, '<h3>$1</h3>')
                .replace(/^## (.*$)/gim, '<h2>$1</h2>')
                .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
                .replace(/```([\s\S]*?)```/gim, '<pre><code>$1</code></pre>')
                .replace(/`(.*?)`/gim, '<code>$1</code>')
                .replace(/\n/gim, '<br/>');

            document.getElementById('bugs').innerHTML = `<div class="markdown-body">${formatMD(data.bugs)}</div>`;
            document.getElementById('optimizations').innerHTML = `<div class="markdown-body">${formatMD(data.optimizations)}</div>`;
            document.getElementById('quality').innerHTML = `<div class="markdown-body">${formatMD(data.quality)}</div>`;
        } else {
            alert("Error: " + (data.error || "Failed to analyze code"));
        }

    } catch (err) {
        alert("Network error. Make sure the backend is running.");
        console.error(err);
    } finally {
        document.getElementById('loading').classList.add('hidden');
        contents.forEach(c => c.classList.remove('hidden'));
        document.getElementById('analyze-btn').disabled = false;
        
        // Reset tabs to bugs
        tabs[0].click();
    }
});
