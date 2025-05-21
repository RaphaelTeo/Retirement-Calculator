from http.server import BaseHTTPRequestHandler
import pandas as pd
pd.set_option('display.float_format', '{:.0f}'.format)
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
plt.use('Agg')  # Force non-interactive backend
import io
import base64
from urllib.parse import parse_qs, urlparse

def create_df(retirement_age):
        income = [yearly_income] * (retirement_age-init_age-1)
        zeroincome = [0] * (final_age-retirement_age)
        income.insert(0,0)
        income.extend(zeroincome)

        df = pd.DataFrame(columns=['age','income','expenses','cumulative'])
        df['age']=age
        df['expenses']=expenses
        df['income']=income
        cum_calc = []
        for i in range(len(df)):
            if i == 0:
                cum_calc.append(init_cumulative)
            else:
                cum_calc.append((cum_calc[i-1]*returnedcapital) + df.loc[i,'income'] - df.loc[i, 'expenses'])

        df['cumulative'] = cum_calc
        return df

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)

            # Extract parameters (with defaults if not provided)
            name = query_params.get('name', ['Unknown'])[0]
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

            for retirement_age in retirement_age_list:
                df = create_df(retirement_age)
                plt.plot(df['age'],df['cumulative'],label=retirement_age)

            plt.grid(True, which='both', linestyle='--', linewidth=0.5)

            plt.axhline(y=0, color='red', linestyle='--', linewidth=2, label='run out of $')
            plt.xlabel('Age')
            plt.xticks(rotation=45)
            plt.ylabel('Cumulative $ (\'000) (log scale)')
            plt.title('Sustainability at different retirement ages')
            plt.legend()
            plt.ylim(bottom=-1000,top=3000) # hides anything below y=0
            ax = plt.gca() # get current axis
            ax.xaxis.set_major_locator(ticker.MultipleLocator(5))  
            ax.yaxis.set_major_locator(ticker.MultipleLocator(1000))
            #plt.savefig('Retirement funds.png', dpi=300)

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plt.close()

             # Encode image as base64
            image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
            buf.close()

            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'image/png')
            self.end_headers()
            self.wfile.write(base64.b64decode(image_base64))

        except Exception as e:
            # Log error and return 500
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Internal Server Error: {str(e)}".encode('utf-8'))
        
        return