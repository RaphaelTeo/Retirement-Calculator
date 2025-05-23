from flask import Flask, request, send_file, render_template

app = Flask(__name__)

def simple_function(a,b,c):
    return a+b+c

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('age')
        retage = request.form.get('retage')
        returns = request.form.get('returns')
        income = request.form.get('income')
        expenses = request.form.get('expenses')
        init = request.form.get('init')

        if name and age and retage and returns and income and expenses and init:
            try:
                age = int(age)
                out = simple_function(age, retage, returns)
                return send_file(out, mimetype='text/plain', as_attachment=False, download_name='info.txt')
            except ValueError:
                return render_template('index.html', error="Age must be a number")
        return render_template('index.html', error="Please provide name and age")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)

            # Extract parameters (with defaults if not provided)
            
            try:
                age = float(query_params.get('age', ['30'])[0])
                retage = float(query_params.get('retage', ['60'])[0])
                returns = float(query_params.get('returns', ['1.02'])[0])
                income = float(query_params.get('income', ['90'])[0])
                expenses = float(query_params.get('expenses', ['36'])[0])
                init = float(query_params.get('init', ['100'])[0])
            except ValueError:
                age, retage, returns, income, expenses, init = 30, 60,1.02,90,36,100  # Fallback defaults for invalid inputs
            '''
            query = request.get("query", {})
            name = query.get("age", "retage", "returns", "income", "expenses", "init")
            '''
            init_age=age
            final_age = 121
            retirement_age_list = list(range(45,70,5))

            returnedcapital=returns
            yearly_income = income
            yearly_expense = expenses
            init_cumulative = init
            age = [i for i in  range(init_age,final_age)]
            expenses = [yearly_expense] * (final_age-init_age-1)
            expenses.insert(0,0)

            out = simple_function(yearly_income,yearly_expense,init_cumulative)

            # Send response
            
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "image/png"
                },
                "body": out,
                "isBase64Encoded": True
    }
            '''
            self.send_response(200)
            self.send_header('Content-Type', 'image/png')
            self.end_headers()
            self.wfile.write(base64.b64decode(image_base64))
            '''

        except Exception as e:
            # Log error and return 500
            return {
                "statusCode": 500,
                "headers": {
                    "Content-Type": "text/plain"
                },
                "body": f"Internal Server Error: {str(e)}".encode('utf-8'),
                "isBase64Encoded": False
    }       
            '''
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Internal Server Error: {str(e)}".encode('utf-8'))
            '''
        
        #return