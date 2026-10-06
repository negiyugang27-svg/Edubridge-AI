import http.server
import socketserver
import threading
import webbrowser
import time

# Define the port number
PORT = 8080

# Professional, multi-tiered Hackathon HTML/CSS/JS dashboard
HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FocusFlow | Digital Wellbeing & Screen Optimization Hub</title>
    <style>
        :root {
            --primary: #2563eb;
            --primary-hover: #1d4ed8;
            --success: #10b981;
            --background: #f8fafc;
            --surface: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: var(--background);
            color: var(--text-main);
            line-height: 1.5;
            padding: 40px 20px;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 40px;
        }

        header h1 {
            font-size: 2.5rem;
            font-weight: 800;
            letter-spacing: -0.025em;
            color: var(--text-main);
            margin-bottom: 8px;
        }

        header p {
            color: var(--text-muted);
            font-size: 1.125rem;
            max-width: 600px;
            margin: 0 auto;
        }

        /* Interactive Hackathon Tool Quick-Mockup */
        .calculator-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 32px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }

        .calc-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 16px;
        }

        .input-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .input-group label {
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--text-main);
        }

        .input-group input {
            padding: 10px 14px;
            border: 1px solid var(--border);
            border-radius: 8px;
            font-size: 1rem;
        }

        .result-box {
            background: #f1f5f9;
            padding: 16px;
            border-radius: 8px;
            margin-top: 20px;
            text-align: center;
            font-weight: 600;
        }

        /* Professional Resource Matrix Grid */
        .matrix-title {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 24px;
        }

        .card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }

        .badge {
            align-self: flex-start;
            background: #eff6ff;
            color: var(--primary);
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 12px;
        }

        .card h3 {
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 8px;
        }

        .card p {
            color: var(--text-muted);
            font-size: 0.95rem;
            margin-bottom: 20px;
            flex-grow: 1;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background-color: var(--primary);
            color: white;
            padding: 10px 16px;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.925rem;
            transition: background 0.2s;
            gap: 6px;
        }

        .btn:hover {
            background-color: var(--primary-hover);
        }

        footer {
            margin-top: 48px;
            text-align: center;
            border-top: 1px solid var(--border);
            padding-top: 24px;
            font-size: 0.875rem;
            color: var(--text-muted);
        }
    </style>
</head>
<body>

    <div class="container">
        <header>
            <div class="badge" style="align-self: center; margin: 0 auto 12px auto;">Hackathon Prototype V1.0</div>
            <h1>FocusFlow Dashboard</h1>
            <p>An enterprise-grade approach to mitigating digital fatigue, managing screen dependencies, and restoring clinical behavioral metrics.</p>
        </header>

        <!-- Hackathon Interactive Feature Matrix -->
        <section class="calculator-card">
            <h3>Interactive Assessment Tool</h3>
            <p style="font-size: 0.9rem; margin-bottom: 12px;">Simulate annual productivity reclamation values live for your pitch presentation:</p>
            <div class="calc-grid">
                <div class="input-group">
                    <label for="hours">Current Daily Phone Hours</label>
                    <input type="number" id="hours" value="6" min="0" max="24" oninput="calculateSavings()">
                </div>
                <div class="input-group">
                    <label for="target">Target Daily Hours</label>
                    <input type="number" id="target" value="2" min="0" max="24" oninput="calculateSavings()">
                </div>
            </div>
            <div class="result-box" id="result">
                Reclaimed time: 1,460 hours/year to reallocate to real-world deployment.
            </div>
        </section>

        <h2 class="matrix-title">Strategic Intervention Matrix 🎯</h2>
        
        <!-- Grid of real working industry standard solutions -->
        <div class="grid">
            <!-- Card 1: Clinical Guidance -->
            <div class="card">
                <div>
                    <span class="badge">Clinical Framework</span>
                    <h3>Mayo Clinic Guidelines</h3>
                    <p>Evidence-based screen paradigms focused on early childhood neural development, behavioral shifts, and implementing physical environment limitations.</p>
                </div>
                <a href="https://mayoclinichealthsystem.org" target="_blank" class="btn">Analyze Research ↗</a>
            </div>

            <!-- Card 2: Professional Open Source Tools -->
            <div class="card">
                <div>
                    <span class="badge">Technical Solution</span>
                    <h3>Google Family Link API</h3>
                    <p>Integrate directly into production networks to execute remote device locks, enforce granular app restrictions, and fetch live system telemetry logs.</p>
                </div>
                <a href="https://families.google" target="_blank" class="btn">Explore Integration ↗</a>
            </div>

            <!-- Card 3: Enterprise Strategy -->
            <div class="card">
                <div>
                    <span class="badge">Behavioral Architecture</span>
                    <h3>Center for Humane Tech</h3>
                    <p>Leverage the official design ledgers compiled by Silicon Valley veterans to construct apps engineered to respect user attention spans instead of capturing them.</p>
                </div>
                <a href="https://humanetech.com" target="_blank" class="btn">Review Ledger ↗</a>
            </div>
        </div>

        <footer>
            Local Python Server Infrastructure: <span style="color: var(--success); font-weight: 700;">Active [HTTP 200 OK]</span> • Logging real-time browser telemetry to terminal.
        </footer>
    </div>

    <script>
        function calculateSavings() {
            const hours = parseFloat(document.getElementById('hours').value) || 0;
            const target = parseFloat(document.getElementById('target').value) || 0;
            const savingsPerDay = Math.max(0, hours - target);
            const savingsPerYear = Math.round(savingsPerDay * 365);
            
            document.getElementById('result').innerText = 
                `Reclaimed time: ${savingsPerYear.toLocaleString()} hours/year to reallocate to real-world deployment.`;
        }
    </script>
</body>
</html>
"""

class HackathonHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP engine serving structured UI payloads while outputting terminal status logs."""
    def do_GET(self):
        # Explicit HTTP Response handshake
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        # Stream UI string into local client interface
        self.wfile.write(bytes(HTML_CONTENT, "utf-8"))

def launch_chrome_instance():
    """Bypasses standard OS handlers to initialize an automated Chrome tab request."""
    time.sleep(1)
    target_addr = f"http://localhost:{PORT}"