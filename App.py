import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai
import os
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt

# ✅ Load API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("⚠️ Gemini API Key is missing! Please check your .env file.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

# ✅ Streamlit UI
st.set_page_config(page_title="AI Personal Finance Planner", page_icon="💰", layout="wide")

# Theme Mode Selection
with st.sidebar:
    theme_mode = option_menu("Theme Mode", ["System", "Light", "Dark"], icons=["laptop", "sun", "moon"], menu_icon="palette", default_index=0)

if theme_mode == "Dark":
    st.markdown(
        """
        <style>
        body {
            background-color: #0e1117;
            color: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
elif theme_mode == "Light":
    st.markdown(
        """
        <style>
        body {
            background-color: #ffffff;
            color: #000000;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


st.title("💰AI Personal Finance Agent🤖")
st.write("Manage your budget and get financial advice with AI.")

AI_path = "AI.png"  # Ensure this file is in the same directory as your script
try:
    st.sidebar.image(AI_path)
except FileNotFoundError:
    st.sidebar.warning("AI.png file not found. Please check the file path.")

image_path = "image.png"  # Ensure this file is in the same directory as your script
try:
    st.sidebar.image(image_path)
except FileNotFoundError:
    st.sidebar.warning("image.png file not found. Please check the file path.")


# Sidebar Navigation
with st.sidebar:
    st.header("⚙ App Features")

    tab_selection = st.radio("Select a Feature:", [
        "🏠 Dashboard Overview",
        "📊 Budget Planning",
        "💸 Expense Tracking",
        "💡 AI Smart Saving Tips",
        "📈 Investment Insights",
        "🔍 Credit Score Analysis",
        "🎯 Financial Goal Setting",
        "⏰ Bill Payment Reminders",
        "📑 Income & Expense Report",
        "🤖 AI Chat Assistant",
        "🚀 Personalized Financial Growth Roadmap",
        "💹 Crypto & Stock Market Portfolio Tracker",
        "📜 AI-Generated Monthly & Yearly Financial Reports",
        "📊 AI-Powered Tax Calculator",
        "💰 Savings Optimizer"
    ])
    
    st.markdown("👨👨‍💻Developer:- Abhishek💖Yadav")
    
    developer_path = "my.jpg"  # Ensure this file is in the same directory as your script
    try:
        st.sidebar.image(developer_path)
    except FileNotFoundError:
        st.sidebar.warning("my.jpg file not found. Please check the file path.")

# ✅ Speech Recognition Setup
recognizer = sr.Recognizer()
def listen_speech():
    try:
        with sr.Microphone() as source:
            st.write("🎤 Listening... Speak now.")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5)
            return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand."
    except sr.RequestError:
        return "Speech Recognition service unavailable."

def speak_text(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"Error in text-to-speech: {e}")

# Initialize session state
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = {}
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Create top tabs (Tab1 to Tab6)
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["AI Financial Advice", "Budget Planner", "Spending Alerts", "Financial Insights", "Financial Goals", "Expense Analysis"])

with tab1:
    st.header("💡 Get AI Financial Advice")
    st.write("Ask for personalized financial advice from our AI.")
    user_input = st.text_area("Enter your financial concern:", value=st.session_state['user_data'].get('financial_concern', ''))
    if st.button("🎤 Speak"):
        user_input = listen_speech()
        st.text(f"You said: {user_input}")

    if user_input:
        st.session_state['user_data']['financial_concern'] = user_input
        try:
            response = model.generate_content(f"Give me a personal finance advice for: {user_input}", generation_config={
                "temperature": 0.3,
                "top_k": 50,
                "top_p": 0.9,
                "max_output_tokens": 500
            })
            ai_reply = response.text
            st.write("💡 **AI Advice:**")
            st.info(ai_reply)
            
            if st.button("🔊 Speak Response"):
                speak_text(ai_reply)
        except Exception as e:
            st.error(f"⚠️ Error generating AI response: {e}")

with tab2:
    st.header("📊 Budget Planner")
    st.write("Plan your budget by entering your income and expenses.")
    income = st.number_input("Enter your monthly income ($)", min_value=0, value=st.session_state['user_data'].get('income', 0))
    expenses = st.number_input("Enter your total monthly expenses ($)", min_value=0, value=st.session_state['user_data'].get('expenses', 0))

    if st.button("💰 Calculate Savings"):
        st.session_state['user_data']['income'] = income
        st.session_state['user_data']['expenses'] = expenses
        savings = income - expenses
        if savings > 0:
            st.success(f"You are saving ${savings} per month! 🎉")
        else:
            st.error("Your expenses are exceeding your income. Consider cost-cutting! 🚨")

with tab3:
    st.header("🚨 Spending Alerts & Budget Warnings")
    st.write("Set your budget and get alerts if you exceed it.")
    budget = st.number_input("Set your monthly budget ($)", min_value=0, value=st.session_state['user_data'].get('budget', 0))

    if st.button("🚨 Check Budget"):
        st.session_state['user_data']['budget'] = budget
        if expenses > budget:
            st.error(f"Your budget is ${budget:.2f}, but you have already spent ${expenses:.2f}. Be careful! 😲")
        else:
            st.success(f"You are within your budget of ${budget:.2f}. Keep it up! 🎉")

with tab4:
    st.header("📊 Personalized Financial Insights")
    st.write("Get insights based on your income and expenses.")
    if income > 0 and expenses > 0:
        ideal_saving = income * 0.3  # Assuming 30% of income should be saved
        st.info(f"Your ideal saving should be ${ideal_saving:.2f} per month based on your income of ${income:.2f}.")

with tab5:
    st.header("🎯 Set Financial Goals")
    st.write("Set and track your financial goals.")
    goal = st.text_input("Enter your financial goal (e.g., Buy a car, Save for vacation)", value=st.session_state['user_data'].get('goal', ''))
    goal_amount = st.number_input("Goal Amount ($)", min_value=0, value=st.session_state['user_data'].get('goal_amount', 0))
    saving_per_month = st.number_input("How much can you save per month? ($)", min_value=0, value=st.session_state['user_data'].get('saving_per_month', 0))

    if st.button("📅 Calculate Goal Timeline"):
        st.session_state['user_data']['goal'] = goal
        st.session_state['user_data']['goal_amount'] = goal_amount
        st.session_state['user_data']['saving_per_month'] = saving_per_month
        if saving_per_month > 0:
            months_needed = goal_amount / saving_per_month
            st.success(f"You will achieve your goal in {round(months_needed, 1)} months! 🎯")
            st.info(f"If you save ${saving_per_month:.2f} per month, you will have ${goal_amount:.2f} in {round(months_needed, 1)} months.")
        else:
            st.error("You need to save something to reach your goal! 😅")

with tab6:
    st.header("📉 Expense Categorization & Analysis")
    st.write("Analyze your expenses by category.")
    expense_data = st.text_area("Enter your expenses (category:amount, e.g., Food:200, Rent:800)", value=st.session_state['user_data'].get('expense_data', ''))

    if st.button("📊 Analyze Spending"):
        st.session_state['user_data']['expense_data'] = expense_data
        if expense_data:
            expenses = [item.split(":") for item in expense_data.split(",")]
            df = pd.DataFrame(expenses, columns=["Category", "Amount"])
            df["Amount"] = df["Amount"].astype(float)
            fig, ax = plt.subplots()
            df.groupby("Category").sum().plot(kind="pie", y="Amount", ax=ax, autopct='%1.1f%%')
            st.pyplot(fig)
            st.write(df.groupby("Category").sum())

# Create bottom tabs (Tab7 to Tab13)
tab7, tab8, tab9, tab10, tab11, tab12, tab13 = st.tabs(["Loan & EMI Calculator", "Investment Suggestions", "Monthly Budget Planner", "Financial Health Score", "Expense Predictions", "Gamification & Rewards", "Financial Q&A"])

with tab7:
    st.header("💳 Loan & EMI Calculator")
    st.write("Calculate your loan EMI based on the loan amount, interest rate, and tenure.")
    loan_amount = st.number_input("Loan Amount ($)", min_value=0, value=st.session_state['user_data'].get('loan_amount', 0))
    interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, max_value=100.0, value=st.session_state['user_data'].get('interest_rate', 0.0))
    loan_tenure = st.number_input("Loan Tenure (years)", min_value=0, value=st.session_state['user_data'].get('loan_tenure', 0))

    if st.button("📈 Calculate EMI"):
        st.session_state['user_data']['loan_amount'] = loan_amount
        st.session_state['user_data']['interest_rate'] = interest_rate
        st.session_state['user_data']['loan_tenure'] = loan_tenure
        if loan_amount > 0 and interest_rate > 0 and loan_tenure > 0:
            monthly_interest_rate = interest_rate / (12 * 100)
            number_of_payments = loan_tenure * 12
            emi = loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** number_of_payments) / ((1 + monthly_interest_rate) ** number_of_payments - 1)
            st.success(f"Your EMI will be ${emi:.2f} per month for a loan of ${loan_amount:.2f} at {interest_rate}% interest over {loan_tenure} years.")
        else:
            st.error("Please enter valid loan details.")

with tab8:
    st.header("📈 Smart Investment Suggestions")
    st.write("Get smart investment suggestions based on the amount you want to invest.")
    investment_amount = st.number_input("Enter amount to invest ($)", min_value=0, value=st.session_state['user_data'].get('investment_amount', 0))

    if st.button("💡 Get Investment Advice"):
        st.session_state['user_data']['investment_amount'] = investment_amount
        if investment_amount > 0:
            try:
                response = model.generate_content(f"Suggest best investment options for ${investment_amount}", generation_config={
                    "temperature": 0.3,
                    "top_k": 50,
                    "top_p": 0.9,
                    "max_output_tokens": 500
                })
                investment_advice = response.text
                st.info(f"💡 **Investment Advice:** {investment_advice}")
            except Exception as e:
                st.error(f"⚠️ Error generating investment advice: {e}")
        else:
            st.error("Please enter a valid investment amount.")

with tab9:
    st.header("🎯 Monthly Budget Planner")
    st.write("Generate a monthly budget plan based on your past spending patterns.")
    if st.button("📅 Generate Budget Plan"):
        try:
            response = model.generate_content("Generate a monthly budget plan based on past spending patterns", generation_config={
                "temperature": 0.3,
                "top_k": 50,
                "top_p": 0.9,
                "max_output_tokens": 500
            })
            budget_plan = response.text
            st.info(f"📅 **Budget Plan:** {budget_plan}")
        except Exception as e:
            st.error(f"⚠️ Error generating budget plan: {e}")

with tab10:
    st.header("💳 Financial Health Score")
    st.write("Get your financial health score based on your income, expenses, savings, and debts.")
    if st.button("📊 Get Financial Health Score"):
        try:
            response = model.generate_content("Analyze financial health score based on income, expenses, savings, and debts", generation_config={
                "temperature": 0.3,
                "top_k": 50,
                "top_p": 0.9,
                "max_output_tokens": 500
            })
            health_score = response.text
            st.info(f"📊 **Financial Health Score:** {health_score}")
        except Exception as e:
            st.error(f"⚠️ Error generating financial health score: {e}")

with tab11:
    st.header("🤖 Smart Expense Predictions")
    st.write("Predict your future expenses based on past spending patterns.")
    if st.button("🔮 Predict Future Expenses"):
        try:
            response = model.generate_content("Predict future expenses based on past spending patterns", generation_config={
                "temperature": 0.3,
                "top_k": 50,
                "top_p": 0.9,
                "max_output_tokens": 500
            })
            expense_predictions = response.text
            st.info(f"🔮 **Expense Predictions:** {expense_predictions}")
        except Exception as e:
            st.error(f"⚠️ Error generating expense predictions: {e}")

with tab12:
    st.header("🎮 Gamification & Rewards")
    st.write("Earn rewards for completing finance-related tasks.")
    if st.button("🏆 Check Rewards"):
        try:
            response = model.generate_content("Provide rewards for completing finance-related tasks", generation_config={
                "temperature": 0.3,
                "top_k": 50,
                "top_p": 0.9,
                "max_output_tokens": 500
            })
            rewards_info = response.text
            st.info(f"🏆 **Rewards:** {rewards_info}")
        except Exception as e:
            st.error(f"⚠️ Error generating rewards information: {e}")

with tab13:
    st.header("💬 Financial Q&A Chatbot")
    st.write("Ask any financial question and get answers from our AI chatbot.")
    
    # Display chat history
    for chat in st.session_state['chat_history']:
        st.write(f"**You:** {chat['question']}")
        st.write(f"**AI:** {chat['answer']}")
    
    user_question = st.text_area("Ask a financial question:", value="")
    if st.button("💬 Get Answer"):
        if user_question:
            try:
                response = model.generate_content(f"Answer the following financial question: {user_question}", generation_config={
                    "temperature": 0.3,
                    "top_k": 50,
                    "top_p": 0.9,
                    "max_output_tokens": 500
                })
                chatbot_answer = response.text
                st.session_state['chat_history'].append({"question": user_question, "answer": chatbot_answer})
                st.write(f"**You:** {user_question}")
                st.write(f"**AI:** {chatbot_answer}")
            except Exception as e:
                st.error(f"⚠️ Error generating chatbot answer: {e}")
        else:
            st.error("Please enter a question.")

# Create bottom tabs (Tab14 to Tab18)
tab14, tab15, tab16, tab17, tab18 = st.tabs(["Personalized Financial Growth Roadmap", "Crypto & Stock Market Portfolio Tracker", "AI-Generated Monthly & Yearly Financial Reports", "AI-Powered Tax Calculator", "Savings Optimizer"])

with tab14:
    st.header("3️⃣ Personalized Financial Growth Roadmap 📅🚀")
    st.write("Get a customized roadmap based on your financial goals.")
    financial_goal = st.text_input("Enter your financial goal (e.g., Save for a house, Retirement)", value=st.session_state['user_data'].get('financial_goal', ''))
    extra_investment = st.number_input("Enter extra investment amount ($)", min_value=0, value=st.session_state['user_data'].get('extra_investment', 0))

    if st.button("📅 Generate Roadmap"):
        st.session_state['user_data']['financial_goal'] = financial_goal
        st.session_state['user_data']['extra_investment'] = extra_investment
        try:
            response = model.generate_content(f"Create a financial growth roadmap for the goal: {financial_goal} with an extra investment of ${extra_investment}", generation_config={
                "temperature": 0.3,
                "top_k": 50,
                "top_p": 0.9,
                "max_output_tokens": 500
            })
            roadmap = response.text
            st.info(f"📅 **Financial Growth Roadmap:** {roadmap}")
        except Exception as e:
            st.error(f"⚠️ Error generating financial growth roadmap: {e}")

with tab15:
    st.header("4️⃣ Crypto & Stock Market Portfolio Tracker 📈🚀")
    st.write("Track your crypto and stock investments in real-time.")
    portfolio_data = st.text_area("Enter your portfolio (e.g., Bitcoin:2, Tesla:5)", value=st.session_state['user_data'].get('portfolio_data', ''))

    if st.button("📈 Track Portfolio"):
        st.session_state['user_data']['portfolio_data'] = portfolio_data
        try:
            response = model.generate_content(f"Track the following portfolio: {portfolio_data}", generation_config={
                "temperature": 0.3,
                "top_k": 50,
                "top_p": 0.9,
                "max_output_tokens": 500
            })
            portfolio_analysis = response.text
            st.info(f"📈 **Portfolio Analysis:** {portfolio_analysis}")
        except Exception as e:
            st.error(f"⚠️ Error tracking portfolio: {e}")

with tab16:
    st.header("5️⃣ AI-Generated Monthly & Yearly Financial Reports 📊📝")
    st.write("Get detailed financial reports based on your income, expenses, and investments.")
    if st.button("📊 Generate Financial Reports"):
        try:
            response = model.generate_content("Generate monthly and yearly financial reports based on income, expenses, and investments", generation_config={
                "temperature": 0.3,
                "top_k": 50,
                "top_p": 0.9,
                "max_output_tokens": 500
            })
            financial_reports = response.text
            st.info(f"📊 **Financial Reports:** {financial_reports}")
        except Exception as e:
            st.error(f"⚠️ Error generating financial reports: {e}")

with tab17:
    st.header("💡 AI-Powered Tax Calculator & Savings Optimizer 💰📑")
    st.write("Get the best tax-saving strategies based on your salary and investments.")
    salary = st.number_input("Enter your annual salary ($)", min_value=0, value=st.session_state['user_data'].get('salary', 0))
    investments = st.number_input("Enter your total investments ($)", min_value=0, value=st.session_state['user_data'].get('investments', 0))

    if st.button("💰 Calculate Tax Savings"):
        st.session_state['user_data']['salary'] = salary
        st.session_state['user_data']['investments'] = investments
        try:
            response = model.generate_content(f"Calculate tax savings for a salary of ${salary} and investments of ${investments}", generation_config={
                "temperature": 0.3,
                "top_k": 50,
                "top_p": 0.9,
                "max_output_tokens": 500
            })
            tax_savings = response.text
            st.info(f"💰 **Tax Savings:** {tax_savings}")
        except Exception as e:
            st.error(f"⚠️ Error calculating tax savings: {e}")

with tab18:
    st.header("💡 Savings Optimizer")
    st.write("Optimize your savings based on your financial data.")
    if st.button("💡 Optimize Savings"):
        try:
            response = model.generate_content("Optimize savings based on financial data", generation_config={
                "temperature": 0.3,
                "top_k": 50,
                "top_p": 0.9,
                "max_output_tokens": 500
            })
            savings_optimization = response.text
            st.info(f"💡 **Savings Optimization:** {savings_optimization}")
        except Exception as e:
            st.error(f"⚠️ Error optimizing savings: {e}")

st.markdown("---")
st.write("Built with AI🤖")
st.write("👨‍💻Developer:- Abhishek❤️Yadav")
