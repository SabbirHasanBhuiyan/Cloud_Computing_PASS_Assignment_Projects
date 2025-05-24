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
    <title>Even Numbers Generator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            max-width: 500px;
            width: 100%;
            text-align: center;
        }

        h1 {
            color: #333;
            margin-bottom: 30px;
            font-size: 2.5rem;
        }

        .input-group {
            margin-bottom: 30px;
        }

        label {
            display: block;
            margin-bottom: 10px;
            color: #555;
            font-size: 1.1rem;
        }

        input {
            width: 200px;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 1.1rem;
            text-align: center;
            transition: all 0.3s ease;
        }

        input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 1.1rem;
            cursor: pointer;
            transition: transform 0.3s ease;
        }

        button:hover {
            transform: translateY(-2px);
        }

        .result {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            display: none;
        }

        .numbers {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            margin-top: 20px;
        }

        .number {
            background: #667eea;
            color: white;
            padding: 8px 12px;
            border-radius: 20px;
            font-weight: bold;
            animation: fadeIn 0.5s ease;
        }

        .count {
            color: #667eea;
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 15px;
        }

        .error {
            color: #e74c3c;
            margin-top: 10px;
            display: none;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .loading {
            color: #667eea;
            margin-top: 20px;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Even Numbers</h1>

        <form id="evenForm">
            <div class="input-group">
                <label for="n">How many even numbers?</label>
                <input type="number" id="n" min="1" max="100" placeholder="Enter number" required>
            </div>
            <button type="submit">Generate</button>
        </form>

        <div class="loading" id="loading">Generating numbers...</div>
        <div class="error" id="error"></div>

        <div class="result" id="result">
            <div class="count" id="count"></div>
            <div class="numbers" id="numbers"></div>
        </div>
    </div>

    <script>
        document.getElementById('evenForm').addEventListener('submit', function(e) {
            e.preventDefault();

            const n = document.getElementById('n').value;
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const error = document.getElementById('error');

            // Hide previous results
            result.style.display = 'none';
            error.style.display = 'none';
            loading.style.display = 'block';

            // Validate input
            if (!n || n < 1 || n > 100) {
                loading.style.display = 'none';
                error.textContent = 'Please enter a number between 1 and 100';
                error.style.display = 'block';
                return;
            }

            // Send request
            fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({n: parseInt(n)})
            })
            .then(response => response.json())
            .then(data => {
                loading.style.display = 'none';

                if (data.error) {
                    error.textContent = data.error;
                    error.style.display = 'block';
                } else {
                    // Show results
                    document.getElementById('count').textContent = `Generated ${data.count} even numbers:`;

                    const numbersDiv = document.getElementById('numbers');
                    numbersDiv.innerHTML = '';

                    data.numbers.forEach((num, index) => {
                        setTimeout(() => {
                            const span = document.createElement('span');
                            span.className = 'number';
                            span.textContent = num;
                            numbersDiv.appendChild(span);
                        }, index * 50);
                    });

                    result.style.display = 'block';
                }
            })
            .catch(err => {
                loading.style.display = 'none';
                error.textContent = 'Something went wrong. Please try again.';
                error.style.display = 'block';
            });
        });
    </script>
</body>
</html>
    ''')

@app.route('/generate', methods=['POST'])
def generate_even():
    try:
        data = request.get_json()
        n = data.get('n', 0)

        if not isinstance(n, int) or n <= 0 or n > 100:
            return jsonify({'error': 'Please enter a number between 1 and 100'})

        # Generate even numbers
        even_numbers = [i * 2 for i in range(1, n + 1)]

        return jsonify({
            'numbers': even_numbers,
            'count': n
        })

    except Exception as e:
        return jsonify({'error': 'Invalid input'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
