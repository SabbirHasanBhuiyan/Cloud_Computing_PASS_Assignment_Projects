# app.py
from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Matrix Multiplication</title>
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
            max-width: 900px;
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

        .matrix-section {
            display: flex;
            justify-content: space-between;
            gap: 20px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }

        .matrix-container {
            flex: 1;
            min-width: 250px;
        }

        .matrix-title {
            color: #11998e;
            font-size: 1.3rem;
            font-weight: bold;
            margin-bottom: 15px;
            text-align: center;
        }

        .size-inputs {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-bottom: 15px;
        }

        .size-inputs input {
            width: 60px;
            padding: 8px;
            border: 2px solid #ddd;
            border-radius: 8px;
            text-align: center;
            font-size: 1rem;
        }

        .size-inputs span {
            display: flex;
            align-items: center;
            font-weight: bold;
            color: #11998e;
        }

        .matrix {
            display: grid;
            gap: 5px;
            justify-content: center;
            margin-bottom: 15px;
        }

        .matrix input {
            width: 50px;
            height: 50px;
            border: 2px solid #ddd;
            border-radius: 8px;
            text-align: center;
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        .matrix input:focus {
            outline: none;
            border-color: #11998e;
            box-shadow: 0 0 0 3px rgba(17, 153, 142, 0.1);
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
            margin: 0 10px;
            transition: transform 0.3s ease;
        }

        button:hover {
            transform: translateY(-2px);
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

        .result-matrix {
            display: grid;
            gap: 5px;
            justify-content: center;
            margin: 20px 0;
        }

        .result-matrix .cell {
            width: 60px;
            height: 60px;
            background: #11998e;
            color: white;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.1rem;
            animation: fadeIn 0.5s ease;
        }

        .error {
            color: #e74c3c;
            text-align: center;
            margin: 20px 0;
            display: none;
            padding: 15px;
            background: #fdf2f2;
            border-radius: 10px;
        }

        .loading {
            text-align: center;
            color: #11998e;
            margin: 20px 0;
            display: none;
        }

        .info {
            background: #e8f8f5;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
            color: #11998e;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.8); }
            to { opacity: 1; transform: scale(1); }
        }

        @media (max-width: 768px) {
            .matrix-section {
                flex-direction: column;
            }

            .container {
                padding: 20px;
            }

            h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Matrix Multiplication</h1>

        <div class="info">
            Enter matrix dimensions and values. Matrix A columns must equal Matrix B rows for multiplication.
        </div>

        <div class="matrix-section">
            <div class="matrix-container">
                <div class="matrix-title">Matrix A</div>
                <div class="size-inputs">
                    <input type="number" id="rowsA" min="1" max="4" value="2" onchange="generateMatrices()">
                    <span>×</span>
                    <input type="number" id="colsA" min="1" max="4" value="3" onchange="generateMatrices()">
                </div>
                <div id="matrixA" class="matrix"></div>
            </div>

            <div class="matrix-container">
                <div class="matrix-title">Matrix B</div>
                <div class="size-inputs">
                    <input type="number" id="rowsB" min="1" max="4" value="3" onchange="generateMatrices()">
                    <span>×</span>
                    <input type="number" id="colsB" min="1" max="4" value="2" onchange="generateMatrices()">
                </div>
                <div id="matrixB" class="matrix"></div>
            </div>
        </div>

        <div class="controls">
            <button onclick="randomFill()">Random Fill</button>
            <button onclick="multiplyMatrices()">Multiply Matrices</button>
            <button onclick="clearMatrices()">Clear All</button>
        </div>

        <div class="loading" id="loading">Calculating...</div>
        <div class="error" id="error"></div>

        <div class="result-section" id="result">
            <div class="result-title">Result Matrix (A × B)</div>
            <div id="resultMatrix" class="result-matrix"></div>
        </div>
    </div>

    <script>
        // Generate matrix input fields
        function generateMatrices() {
            generateMatrix('matrixA', 'rowsA', 'colsA');
            generateMatrix('matrixB', 'rowsB', 'colsB');
            hideResult();
        }

        function generateMatrix(containerId, rowsId, colsId) {
            const container = document.getElementById(containerId);
            const rows = parseInt(document.getElementById(rowsId).value);
            const cols = parseInt(document.getElementById(colsId).value);

            container.innerHTML = '';
            container.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;

            for (let i = 0; i < rows * cols; i++) {
                const input = document.createElement('input');
                input.type = 'number';
                input.value = '0';
                input.step = 'any';
                container.appendChild(input);
            }
        }

        // Fill matrices with random values
        function randomFill() {
            const inputs = document.querySelectorAll('.matrix input');
            inputs.forEach(input => {
                input.value = Math.floor(Math.random() * 10) + 1;
            });
        }

        // Clear all matrices
        function clearMatrices() {
            const inputs = document.querySelectorAll('.matrix input');
            inputs.forEach(input => {
                input.value = '0';
            });
            hideResult();
        }

        // Get matrix values from inputs
        function getMatrixValues(containerId, rows, cols) {
            const container = document.getElementById(containerId);
            const inputs = container.querySelectorAll('input');
            const matrix = [];

            for (let i = 0; i < rows; i++) {
                const row = [];
                for (let j = 0; j < cols; j++) {
                    const value = parseFloat(inputs[i * cols + j].value) || 0;
                    row.push(value);
                }
                matrix.push(row);
            }

            return matrix;
        }

        // Multiply matrices
        function multiplyMatrices() {
            const rowsA = parseInt(document.getElementById('rowsA').value);
            const colsA = parseInt(document.getElementById('colsA').value);
            const rowsB = parseInt(document.getElementById('rowsB').value);
            const colsB = parseInt(document.getElementById('colsB').value);

            // Check if multiplication is possible
            if (colsA !== rowsB) {
                showError(`Cannot multiply matrices. Matrix A columns (${colsA}) must equal Matrix B rows (${rowsB})`);
                return;
            }

            const matrixA = getMatrixValues('matrixA', rowsA, colsA);
            const matrixB = getMatrixValues('matrixB', rowsB, colsB);

            hideError();
            showLoading();

            // Send to server for multiplication
            fetch('/multiply', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    matrixA: matrixA,
                    matrixB: matrixB
                })
            })
            .then(response => response.json())
            .then(data => {
                hideLoading();

                if (data.error) {
                    showError(data.error);
                } else {
                    showResult(data.result, rowsA, colsB);
                }
            })
            .catch(err => {
                hideLoading();
                showError('Something went wrong. Please try again.');
            });
        }

        // Display result matrix
        function showResult(result, rows, cols) {
            const container = document.getElementById('resultMatrix');
            container.innerHTML = '';
            container.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;

            for (let i = 0; i < rows; i++) {
                for (let j = 0; j < cols; j++) {
                    setTimeout(() => {
                        const cell = document.createElement('div');
                        cell.className = 'cell';
                        cell.textContent = result[i][j];
                        container.appendChild(cell);
                    }, (i * cols + j) * 100);
                }
            }

            document.getElementById('result').style.display = 'block';
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
        }

        // Initialize matrices on page load
        generateMatrices();
        randomFill();
    </script>
</body>
</html>
    ''')

@app.route('/multiply', methods=['POST'])
def multiply_matrices():
    try:
        data = request.get_json()
        matrix_a = data.get('matrixA', [])
        matrix_b = data.get('matrixB', [])

        # Validate matrices
        if not matrix_a or not matrix_b:
            return jsonify({'error': 'Invalid matrices provided'})

        rows_a = len(matrix_a)
        cols_a = len(matrix_a[0]) if matrix_a else 0
        rows_b = len(matrix_b)
        cols_b = len(matrix_b[0]) if matrix_b else 0

        # Check if multiplication is possible
        if cols_a != rows_b:
            return jsonify({'error': 'Matrix dimensions are incompatible for multiplication'})

        # Perform matrix multiplication
        result = []
        for i in range(rows_a):
            row = []
            for j in range(cols_b):
                sum_val = 0
                for k in range(cols_a):
                    sum_val += matrix_a[i][k] * matrix_b[k][j]
                row.append(round(sum_val, 2))
            result.append(row)

        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': 'Error in matrix multiplication'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
