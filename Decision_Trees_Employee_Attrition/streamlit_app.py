import streamlit as st
import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.preprocessing import PolynomialFeatures

st.set_page_config(page_title="Employee Attrition Predictor",
                   page_icon="🚶‍♂️")

st.title("🚶‍♂️ Employee Attrition Predictor 🚶‍♂️")

st.markdown("""Created by: Hannan Khan  
[GitHub](https://github.com/hannankhan888) | [LinkedIn](https://www.linkedin.com/in/hannankhan888/)""")
st.markdown("This app predicts whether an employee will churn based on a number of features.")
st.markdown("The full project can be found on GitHub [here]("
            "https://github.com/hannankhan888/Data_Science_Portfolio/tree/main/Decision_Trees_Employee_Attrition).")
st.caption("Enter the details of the employee below, and the result (on the right side) will update automatically.")

col1, col2 = st.columns(2)

with col1:
    placeholder = st.empty()

    age = placeholder.number_input("Employee Age", min_value=0, key='age')

    daily_rate = st.number_input("Daily Rate", min_value=0, key='daily_rate')

    department = {"Dep_HR": 0,
                  "Dep_R&D": 56,
                  "Dep_Sales": 4}
    dept = st.selectbox("Employee Department", department, key='department')
    department = dict.fromkeys(department, 0)
    department[dept] = 1

    distance_from_home = st.number_input("Distance from home", min_value=0,
                                         key='dist_from_home')

    no_yes = ['No', 'Yes']
    divorced = st.selectbox("Divorced?", no_yes, key='divorced')
    divorced = no_yes.index(divorced)

    fields = {"Edu_HR": 0,
              "Edu_Life_Sci": 0,
              "Edu_Marketing": 0,
              "Edu_Medical": 0,
              "Edu_Other": 0,
              "Edu_Technical_Deg": 0}
    education_field = st.selectbox("Employee's Field of Education?", fields,
                                   key='education_field')
    fields = dict.fromkeys(fields, 0)
    fields[education_field] = 1

    education_types = ['Below College', 'College', 'Bachelor', 'Master', 'Doctor']
    education = st.selectbox("Education Level", education_types, key='education_types')
    education = education_types.index(education) + 1

    employee_count = 1

    employee_number = st.number_input("Employee Number", min_value=1, key='emp_number')

    satisfaction = ['Low', 'Medium', 'High', 'Very High']
    environment_satisfaction = st.selectbox("Environment Satisfaction", satisfaction, key='env_satisfaction')
    environment_satisfaction = satisfaction.index(environment_satisfaction) + 1

    genders = ['Male', 'Female']
    gender = st.selectbox("Gender", genders, key='gender')
    gender = genders.index(gender)

    hourly_rate = st.number_input("Hourly Rate", min_value=0, key='hourly_rate')

    job_involvement = st.selectbox("Job Involvement", satisfaction, key='job_involvement')
    job_involvement = satisfaction.index(job_involvement) + 1

    job_level = st.number_input("Job Level", min_value=1, max_value=5, key='job_level')

    job_satisfaction = st.selectbox("Job Satisfaction", satisfaction, key='job_satisfaction')
    job_satisfaction = satisfaction.index(job_satisfaction) + 1

    jobs = {"Job_HR": 0,
            "Job_Healthcare_Rep": 0,
            "Job_Lab_Tech": 0,
            "Job_Manager": 0,
            "Job_Manuf_Dir": 0,
            "Job_Research_Dir": 0,
            "Job_Research_Sci": 0,
            "Job_Sales_Exec": 0,
            "Job_Sales_Rep": 0}
    job = st.selectbox("Job Title", jobs, key='job_title')
    jobs = dict.fromkeys(jobs, 0)
    jobs[job] = 1

    log_distance_from_home = np.log10(distance_from_home)
    if np.log10(distance_from_home) == -np.inf:
        log_distance_from_home = 0

    log_job_level = np.log10(job_level)

    married = st.selectbox("Married?", no_yes, key='married')
    married = no_yes.index(married)

    monthly_income = st.number_input("Monthly Income", min_value=0, key='monthly_income')

    log_monthly_income = np.log10(monthly_income)
    if log_monthly_income == -np.inf:
        log_monthly_income = 0

    monthly_rate = st.number_input("Monthly Rate", min_value=0, key='monthly_rate')

    non_travel = st.selectbox("Non-Travel Employee?", no_yes, key='non_travel')
    non_travel = no_yes.index(non_travel)

    num_companies_worked = st.number_input("Number of Companies Worked", min_value=1,
                                           key='num_companies_worked')

    log_num_companies_worked = np.log10(num_companies_worked)
    if log_num_companies_worked == -np.inf:
        log_num_companies_worked = 0

    over_18 = st.selectbox("Over 18", no_yes, key='over_18')
    over_18 = no_yes.index(over_18)

    overtime = st.selectbox("Overtime", no_yes, key='overtime')
    overtime = no_yes.index(overtime)

    percent_salary_hike = st.number_input("Percent Salary Hike", min_value=0, key='percent_salary_hike')

    log_percent_salary_hike = np.log10(percent_salary_hike)
    if log_percent_salary_hike == -np.inf:
        log_percent_salary_hike = 0

    ratings = ['Low', 'Good', 'Excellent', 'Outstanding']
    performance_rating = st.selectbox("Performance Rating", ratings, key='performance_rating')
    performance_rating = ratings.index(performance_rating) + 1

    relationship_satisfaction = st.selectbox("Relationship Satisfaction", satisfaction,
                                             key='relationship_satisfaction')
    relationship_satisfaction = satisfaction.index(relationship_satisfaction) + 1

    overall_satisfaction = environment_satisfaction + job_satisfaction + relationship_satisfaction

    single = st.selectbox("Single?", no_yes, key='single')
    single = no_yes.index(single)

    standard_hours = 80

    stock_option_level = st.number_input("Stock Option Level", min_value=0, max_value=3,
                                         key='stock_option_level')

    total_working_years = st.number_input("Total Working Years", min_value=0, key='total_working_years')

    log_total_working_years = np.log10(total_working_years)
    if log_total_working_years == -np.inf:
        log_total_working_years = 0

    num_years_at_each_company = total_working_years / num_companies_worked

    training_times_last_year = st.number_input("Training Times Last Year", min_value=0,
                                               max_value=10, key='training_times_last_yr')

    travel_frequently = st.selectbox("Travel Frequently?", no_yes, key='travel_frequent')
    travel_frequently = no_yes.index(travel_frequently)

    travel_rarely = st.selectbox("Travel Rarely?", no_yes, key='travel_rarely')
    travel_rarely = no_yes.index(travel_rarely)

    balance = ['Bad', 'Good', 'Better', 'Best']
    work_life_balance = st.selectbox("Work/Life Balance", balance, key='work_life_balance')
    work_life_balance = balance.index(work_life_balance) + 1

    years_at_company = st.number_input("Years At Company", min_value=1, key='years_at_company')

    log_years_at_company = np.log10(years_at_company)

    years_at_other_companies = st.number_input("Years At Other Companies", min_value=0,
                                               key='years_at_other_companies')

    years_in_current_role = st.number_input("Years In Current Role", min_value=0,
                                            key='years_in_current_role')

    years_since_last_promotion = st.number_input("Years Since Last Promotion", min_value=0,
                                                 key='years_since_last_promotion')

    years_with_curr_manager = st.number_input("Years With Current Manager", min_value=0,
                                              key='years_with_curr_manager')

    # we fill a dict to be able to send to a DataFrame
    emp_dict = {'Age': age,
                'DailyRate': daily_rate,
                'DistanceFromHome': distance_from_home,
                'Divorced': divorced,
                'Education': education,
                'EmployeeCount': employee_count,
                'EmployeeNumber': employee_number,
                'EnvironmentSatisfaction': environment_satisfaction,
                'Gender': gender,
                'HourlyRate': hourly_rate,
                'JobInvolvement': job_involvement,
                'JobLevel': job_level,
                'JobSatisfaction': job_satisfaction,
                'LogDistanceFromHome': log_distance_from_home,
                'LogJobLevel': log_job_level,
                'LogMonthlyIncome': log_monthly_income,
                'LogNumCompaniesWorked': log_num_companies_worked,
                'LogPercentSalaryHike': log_percent_salary_hike,
                'LogTotalWorkingYears': log_total_working_years,
                'LogYearsAtCompany': log_years_at_company,
                'Married': married,
                'MonthlyIncome': monthly_income,
                'MonthlyRate': monthly_rate,
                'Non-Travel': non_travel,
                'NumCompaniesWorked': num_companies_worked,
                'NumYearsAtEachCompany': num_years_at_each_company,
                'Over18': over_18,
                'OverTime': overtime,
                'OverallSatisfaction': overall_satisfaction,
                'PercentSalaryHike': percent_salary_hike,
                'PerformanceRating': performance_rating,
                'RelationshipSatisfaction': relationship_satisfaction,
                'Single': single,
                'StandardHours': standard_hours,
                'StockOptionLevel': stock_option_level,
                'TotalWorkingYears': total_working_years,
                'TrainingTimesLastYear': training_times_last_year,
                'Travel_Frequently': travel_frequently,
                'Travel_Rarely': travel_rarely,
                'WorkLifeBalance': work_life_balance,
                'YearsAtCompany': years_at_company,
                'YearsAtOtherCompanies': years_at_other_companies,
                'YearsInCurrentRole': years_in_current_role,
                'YearsSinceLastPromotion': years_since_last_promotion,
                'YearsWithCurrManager': years_with_curr_manager}

    # we merge other dicts
    emp_dict.update(department)
    emp_dict.update(fields)
    emp_dict.update(jobs)

    # we send the employee dict to a Dataframe:
    df = pd.DataFrame(emp_dict, index=[0]).sort_index(axis=1)

    # calculate polynomial features
    PF = PolynomialFeatures(degree=2, include_bias=False)
    df_pf = PF.fit_transform(df)

with col2:
    XGB = XGBClassifier()
    XGB.load_model("models/best_XGB.json")
    result = XGB.predict(df_pf)
    if result:
        st.markdown("<h1>The prediction is that the employee <span style='color: red'>WILL "
                    "CHURN</span>.</h1>", unsafe_allow_html=True)
    else:
        st.markdown("<h1>The prediction is that the employee <span style='color: green'>WILL NOT CHURN</span>.</h1>",
                    unsafe_allow_html=True)

st.write(df)


def employee_will_not_churn():
    st.session_state.age = 49
    st.session_state.daily_rate = 279
    st.session_state.department = 'Dep_R&D'
    st.session_state.dist_from_home = 8
    st.session_state.divorced = 'No'
    st.session_state.education_field = 'Edu_Life_Sci'
    st.session_state.education_types = 'College'
    st.session_state.emp_number = 2
    st.session_state.env_satisfaction = 'Very High'
    st.session_state.gender = 'Male'
    st.session_state.hourly_rate = 61
    st.session_state.job_involvement = 'Very High'
    st.session_state.job_level = 5
    st.session_state.job_satisfaction = 'Very High'
    st.session_state.job_title = 'Job_HR'
    st.session_state.married = 'Yes'
    st.session_state.monthly_income = 2300
    st.session_state.monthly_rate = 2300
    st.session_state.non_travel = 'Yes'
    st.session_state.num_companies_worked = 100
    st.session_state.over_18 = 'Yes'
    st.session_state.overtime = 'No'
    st.session_state.percent_salary_hike = 1234
    st.session_state.performance_rating = 'Outstanding'
    st.session_state.relationship_satisfaction = 'Very High'
    st.session_state.single = 'Yes'
    st.session_state.stock_option_level = 3
    st.session_state.total_working_years = 2
    st.session_state.training_times_last_yr = 2
    st.session_state.travel_frequent = 'No'
    st.session_state.travel_rarely = 'Yes'
    st.session_state.work_life_balance = 'Best'
    st.session_state.years_at_company = 10
    st.session_state.years_at_other_companies = 0
    st.session_state.years_in_current_role = 7
    st.session_state.years_since_last_promotion = 1
    st.session_state.years_with_curr_manager = 7


tooltip = 'Updates the form to show an employee that will not churn. Available for convenience.'
clear = st.button("Input 'Will NOT Churn' Data", key=1,
                  on_click=employee_will_not_churn, help=tooltip)
