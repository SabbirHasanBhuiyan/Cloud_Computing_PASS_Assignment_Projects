from flask import Flask, render_template_string

app = Flask(__name__)

# Your HTML content
HTML_CONTENT = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nth Largest Number Finder</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            padding: 40px;
        }

        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 2.5rem;
        }

        .info {
            background: #e8f8f5;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
            color: #11998e;
            font-size: 1.1rem;
        }

        .input-section {
            margin-bottom: 30px;
        }

        .section-title {
            color: #11998e;
            font-size: 1.4rem;
            font-weight: bold;
            margin-bottom: 15px;
            text-align: center;
        }

        .numbers-input {
            display: flex;
            flex-direction: column;
            gap: 15px;
            margin-bottom: 20px;
        }

        .input-row {
            display: flex;
            gap: 15px;
            align-items: center;
            justify-content: center;
            flex-wrap: wrap;
        }

        label {
            color: #11998e;
            font-weight: bold;
            font-size: 1.1rem;
            min-width: 120px;
        }

        #numbersList {
            flex: 1;
            min-width: 300px;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 1.1rem;
            transition: all 0.3s ease;
        }

        #numbersList:focus {
            outline: none;
            border-color: #11998e;
            box-shadow: 0 0 0 3px rgba(17, 153, 142, 0.1);
        }

        #nValue {
            width: 80px;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 10px;
            text-align: center;
            font-size: 1.1rem;
            transition: all 0.3s ease;
        }

        #nValue:focus {
            outline: none;
            border-color: #11998e;
            box-shadow: 0 0 0 3px rgba(17, 153, 142, 0.1);
        }

        .numbers-display {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            margin: 20px 0;
            min-height: 50px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
        }

        .number-chip {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: bold;
            animation: fadeIn 0.3s ease;
        }

        .number-chip.highlighted {
            background: linear-gradient(135deg, #e74c3c 0%, #f39c12 100%);
            transform: scale(1.1);
            box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);
        }

        .controls {
            text-align: center;
            margin: 30px 0;
        }

        button {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 1.1rem;
            cursor: pointer;
            margin: 0 10px 10px 0;
            transition: transform 0.3s ease;
        }

        button:hover {
            transform: translateY(-2px);
        }

        button:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }

        .result-section {
            margin-top: 30px;
            text-align: center;
            display: none;
        }

        .result-title {
            color: #11998e;
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 20px;
        }

        .result-value {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            font-size: 2.5rem;
            font-weight: bold;
            display: inline-block;
            min-width: 150px;
            animation: bounceIn 0.6s ease;
        }

        .result-details {
            margin-top: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            color: #666;
        }

        .sorted-numbers {
            margin-top: 15px;
            font-size: 1.1rem;
        }

        .error {
            color: #e74c3c;
            text-align: center;
            margin: 20px 0;
            display: none;
            padding: 15px;
            background: #fdf2f2;
            border-radius: 10px;
            font-size: 1.1rem;
        }

        .loading {
            text-align: center;
            color: #11998e;
            margin: 20px 0;
            display: none;
            font-size: 1.2rem;
        }

        .loading::after {
            content: '';
            animation: dots 1.5s steps(5, end) infinite;
        }

        @keyframes dots {
            0%, 20% { content: '.'; }
            40% { content: '..'; }
            60% { content: '...'; }
            80%, 100% { content: ''; }
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.8); }
            to { opacity: 1; transform: scale(1); }
        }

        @keyframes bounceIn {
            0% { opacity: 0; transform: scale(0.3); }
            50% { opacity: 1; transform: scale(1.1); }
            100% { opacity: 1; transform: scale(1); }
        }

        @media (max-width: 768px) {
            .container {
                padding: 20px;
            }

            h1 {
                font-size: 2rem;
            }

            .input-row {
                flex-direction: column;
                align-items: stretch;
            }

            label {
                min-width: auto;
                text-align: center;
            }

            #numbersList {
                min-width: auto;
            }

            .result-value {
                font-size: 2rem;
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Nth Largest Number Finder</h1>

        <div class="info">
            Enter a list of numbers (separated by commas) and specify which largest number you want to find.
        </div>

        <div class="input-section">
            <div class="section-title">Input Numbers</div>
            <div class="numbers-input">
                <div class="input-row">
                    <label for="numbersList">Numbers:</label>
                    <input type="text" id="numbersList" placeholder="e.g., 5, 12, 8, 3, 15, 9, 1, 7"
                           oninput="updateNumbersDisplay()">
                </div>
                <div class="input-row">
                    <label for="nValue">Find the:</label>
                    <input type="number" id="nValue" min="1" value="1" oninput="validateInput()">
                    <span style="color: #11998e; font-weight: bold; font-size: 1.1rem;">largest number</span>
                </div>
            </div>
        </div>

        <div class="section-title">Current Numbers</div>
        <div id="numbersDisplay" class="numbers-display">
            <span style="color: #999; font-style: italic;">Enter numbers above to see them here</span>
        </div>

        <div class="controls">
            <button onclick="findNthLargest()">Find Nth Largest</button>
            <button onclick="generateRandomNumbers()">Generate Random Numbers</button>
            <button onclick="clearAll()">Clear All</button>
        </div>

        <div class="loading" id="loading">Processing</div>
        <div class="error" id="error"></div>

        <div class="result-section" id="result">
            <div class="result-title" id="resultTitle">Result</div>
            <div class="result-value" id="resultValue">0</div>
            <div class="result-details" id="resultDetails"></div>
        </div>
    </div>

    <script>
        let currentNumbers = [];
        let sortedNumbers = [];

        // Update numbers display as user types
        function updateNumbersDisplay() {
            const input = document.getElementById('numbersList').value;
            const display = document.getElementById('numbersDisplay');

            if (!input.trim()) {
                display.innerHTML = '<span style="color: #999; font-style: italic;">Enter numbers above to see them here</span>';
                currentNumbers = [];
                return;
            }

            // Parse numbers from input
            const numbers = input.split(',')
                .map(s => s.trim())
                .filter(s => s !== '')
                .map(s => {
                    const num = parseFloat(s);
                    return isNaN(num) ? null : num;
                });

            // Filter out invalid numbers
            currentNumbers = numbers.filter(n => n !== null);

            // Display valid numbers
            if (currentNumbers.length === 0) {
                display.innerHTML = '<span style="color: #e74c3c;">No valid numbers found</span>';
            } else {
                display.innerHTML = currentNumbers
                    .map(num => `<span class="number-chip">${num}</span>`)
                    .join('');
            }

            validateInput();
            hideResult();
        }

        // Validate input and enable/disable button
        function validateInput() {
            const n = parseInt(document.getElementById('nValue').value);
            const findButton = document.querySelector('button[onclick="findNthLargest()"]');

            if (currentNumbers.length === 0 || n < 1 || n > currentNumbers.length) {
                findButton.disabled = true;
            } else {
                findButton.disabled = false;
            }

            hideError();
        }

        // Generate random numbers for testing
        function generateRandomNumbers() {
            const count = Math.floor(Math.random() * 8) + 5; // 5-12 numbers
            const numbers = [];

            for (let i = 0; i < count; i++) {
                numbers.push(Math.floor(Math.random() * 100) + 1); // 1-100
            }

            document.getElementById('numbersList').value = numbers.join(', ');
            updateNumbersDisplay();
        }

        // Clear all inputs
        function clearAll() {
            document.getElementById('numbersList').value = '';
            document.getElementById('nValue').value = '1';
            updateNumbersDisplay();
            hideResult();
        }

        // Find nth largest number
        function findNthLargest() {
            const n = parseInt(document.getElementById('nValue').value);

            if (currentNumbers.length === 0) {
                showError('Please enter some numbers first.');
                return;
            }

            if (n < 1 || n > currentNumbers.length) {
                showError(`N must be between 1 and ${currentNumbers.length} (total numbers available).`);
                return;
            }

            hideError();
            showLoading();

            // Simulate processing time for better UX
            setTimeout(() => {
                try {
                    // Sort numbers in descending order
                    sortedNumbers = [...currentNumbers].sort((a, b) => b - a);

                    // Remove duplicates for finding nth largest unique number
                    const uniqueSorted = [...new Set(sortedNumbers)];

                    if (n > uniqueSorted.length) {
                        hideLoading();
                        showError(`Only ${uniqueSorted.length} unique numbers available. Cannot find ${n}${getOrdinalSuffix(n)} largest.`);
                        return;
                    }

                    const nthLargest = uniqueSorted[n - 1];

                    hideLoading();
                    showResult(nthLargest, n, uniqueSorted);

                } catch (error) {
                    hideLoading();
                    showError('An error occurred while processing the numbers.');
                }
            }, 800);
        }

        // Display result
        function showResult(nthLargest, n, uniqueSorted) {
            const resultTitle = document.getElementById('resultTitle');
            const resultValue = document.getElementById('resultValue');
            const resultDetails = document.getElementById('resultDetails');

            resultTitle.textContent = `The ${n}${getOrdinalSuffix(n)} Largest Number`;
            resultValue.textContent = nthLargest;

            // Highlight the nth largest number in the display
            highlightNumber(nthLargest);

            // Show details
            const originalCount = currentNumbers.length;
            const uniqueCount = uniqueSorted.length;
            const position = sortedNumbers.indexOf(nthLargest) + 1;

            resultDetails.innerHTML = `
                <div><strong>Original numbers:</strong> ${originalCount} total</div>
                <div><strong>Unique numbers:</strong> ${uniqueCount} total</div>
                <div><strong>Position in sorted list:</strong> ${position}${getOrdinalSuffix(position)}</div>
                <div class="sorted-numbers">
                    <strong>All numbers sorted (descending):</strong><br>
                    ${sortedNumbers.slice(0, 10).join(', ')}${sortedNumbers.length > 10 ? '...' : ''}
                </div>
            `;

            document.getElementById('result').style.display = 'block';
        }

        // Highlight the nth largest number in the display
        function highlightNumber(targetNumber) {
            const chips = document.querySelectorAll('.number-chip');
            chips.forEach(chip => {
                chip.classList.remove('highlighted');
                if (parseFloat(chip.textContent) === targetNumber) {
                    chip.classList.add('highlighted');
                }
            });
        }

        // Get ordinal suffix (1st, 2nd, 3rd, etc.)
        function getOrdinalSuffix(n) {
            const lastDigit = n % 10;
            const lastTwoDigits = n % 100;

            if (lastTwoDigits >= 11 && lastTwoDigits <= 13) {
                return 'th';
            }

            switch (lastDigit) {
                case 1: return 'st';
                case 2: return 'nd';
                case 3: return 'rd';
                default: return 'th';
            }
        }

        // Utility functions
        function showError(message) {
            const error = document.getElementById('error');
            error.textContent = message;
            error.style.display = 'block';
        }

        function hideError() {
            document.getElementById('error').style.display = 'none';
        }

        function showLoading() {
            document.getElementById('loading').style.display = 'block';
        }

        function hideLoading() {
            document.getElementById('loading').style.display = 'none';
        }

        function hideResult() {
            document.getElementById('result').style.display = 'none';
            // Remove highlighting
            const chips = document.querySelectorAll('.number-chip');
            chips.forEach(chip => chip.classList.remove('highlighted'));
        }

        // Initialize with some sample data
        document.getElementById('numbersList').value = '15, 8, 23, 4, 16, 12, 9, 3, 21, 7';
        updateNumbersDisplay();
    </script>
</body>
</html>'''

@app.route('/')
def index():
    return render_template_string(HTML_CONTENT)

if __name__ == '__main__':
    app.run(debug=True)
