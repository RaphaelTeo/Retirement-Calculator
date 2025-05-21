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

def handler(request):
    query = request.get("query", {})
    name = query.get("age", "retage", "returns", "income", "expenses", "init")

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

    return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "image/png"
            },
            "body": "plt",
            "isBase64Encoded": True
        }