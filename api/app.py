from flask import Flask, request, render_template, send_file
import pandas as pd
pd.set_option('display.float_format', '{:.0f}'.format)
import matplotlib
matplotlib.use('Agg')  # Force non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
#import os
import io
import base64
import sys
import traceback

app = Flask(__name__)

def create_df(age,retirement_age,final_age,age_lst,expenses_lst,income,init,returns):
        income_lst = [income] * (retirement_age-age-1)
        zeroincome = [0] * (final_age-retirement_age)
        income_lst.insert(0,0)
        income_lst.extend(zeroincome)

        df = pd.DataFrame(columns=['age','income','expenses','cumulative'])
        df['age']=age_lst
        df['expenses']=expenses_lst
        df['income']=income_lst
        cum_calc = []
        for i in range(len(df)):
            if i == 0:
                cum_calc.append(init)
            else:
                cum_calc.append((cum_calc[i-1]*returns) + df.loc[i,'income'] - df.loc[i, 'expenses'])

        df['cumulative'] = cum_calc
        return df

@app.route('/', methods=['GET'])
def index():
    error = None
    image_data = None
    if request.method == 'GET':
        try:
            age = int(request.form['age'])
            retage = int(request.form['retage'])
            returns = float(request.form['returns'])
            returns = (returns/100)+1
            income = float(request.form['income'])
            expenses = float(request.form['expenses'])
            init = float(request.form['init'])

            final_age = 121
            retirement_age_list = list(range(age+1,retage+1,1))
            #retirement_age_list = [retage]
            age_lst = [i for i in  range(age,final_age)]
            expenses_lst = [expenses] * (final_age-age-1)
            expenses_lst.insert(0,0)

            for retirement_age in retirement_age_list:
                df = create_df(age,retirement_age,final_age,age_lst,expenses_lst,income,init,returns)
                plt.plot(df['age'],df['cumulative'],label=retirement_age)

            plt.grid(True, which='both', linestyle='--', linewidth=0.5)

            plt.axhline(y=0, color='red', linestyle='--', linewidth=1)
            plt.xlabel('Age')
            plt.xticks(rotation=45)
            plt.ylabel('Cumulative $ (\'000)')
            #plt.title(f'Sustainability at different retirement ages at {round((returns-1),2)*100}% return')
            plt.tight_layout()
            plt.legend(bbox_to_anchor=(0, 1), loc='upper left')
            plt.ylim(bottom=-200,top=2000)
            ax = plt.gca() # get current axis
            ax.xaxis.set_major_locator(ticker.MultipleLocator(5))  
            ax.yaxis.set_major_locator(ticker.MultipleLocator(200))
            #plt.savefig(f'Sustainability {init_cumulative}k inc {yearly_income}k exp {yearly_expense}k at {round((returnedcapital-1),2)*100} percent.png', dpi=300)
            #plt.show()

            # Output plot directly to BytesIO
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight')
            buf.seek(0)
            image_data = base64.b64encode(buf.getvalue()).decode('utf-8')
            plt.close()

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            trace = [i for i in traceback.format_tb(exc_traceback)]
            error = f"{str(e)} | {exc_type.__name__} | {exc_value} | {trace}"

    return render_template("index.html", error=error, image_data=image_data)

if __name__ == '__main__':
    app.run(debug=True)