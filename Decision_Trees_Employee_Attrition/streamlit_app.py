import streamlit as st
import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.preprocessing import PolynomialFeatures

st.set_page_config(page_title="Employee Attrition Predictor",
                   page_icon="🚶‍♂️")

st.title("Employee Attrition Predictor")

st.markdown("This app predicts whether an employee will churn based on a number of features.")
st.caption("Enter the details of the employee below, and the result (on the right side) will update automatically.")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Employee Age", min_value=0)

    daily_rate = st.number_input("Daily Rate", min_value=0)

    department = {"Dep_HR": 0,
                  "Dep_R&D": 56,
                  "Dep_Sales": 4}
    dept = st.selectbox("Employee Department", department)
    department = dict.fromkeys(department, 0)
    department[dept] = 1

    distance_from_home = st.number_input("Distance from home", min_value=0)

    no_yes = ['No', 'Yes']
    divorced = st.selectbox("Divorced?", no_yes)
    divorced = no_yes.index(divorced)

    fields = {"Edu_HR": 0,
              "Edu_Life_Sci": 0,
              "Edu_Marketing": 0,
              "Edu_Medical": 0,
              "Edu_Other": 0,
              "Edu_Technical_Deg": 0}
    education_field = st.selectbox("Employee's Field of Education?", fields)
    fields = dict.fromkeys(fields, 0)
    fields[education_field] = 1

    education_types = ['Below College', 'College', 'Bachelor', 'Master', 'Doctor']
    education = st.selectbox("Education Level", education_types)
    education = education_types.index(education) + 1

    employee_count = 1

    employee_number = st.number_input("Employee Number", min_value=1)

    satisfaction = ['Low', 'Medium', 'High', 'Very High']
    environment_satisfaction = st.selectbox("Environment Satisfaction", satisfaction)
    environment_satisfaction = satisfaction.index(environment_satisfaction) + 1

    genders = ['Male', 'Female']
    gender = st.selectbox("Gender", genders)
    gender = genders.index(gender)

    hourly_rate = st.number_input("Hourly Rate", min_value=0)

    job_involvement = st.selectbox("Job Involvement", satisfaction)
    job_involvement = satisfaction.index(job_involvement) + 1

    job_level = st.number_input("Job Level", min_value=1, max_value=5)

    job_satisfaction = st.selectbox("Job Satisfaction", satisfaction)
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
    job = st.selectbox("Job Title", jobs)
    jobs = dict.fromkeys(jobs, 0)
    jobs[job] = 1

    log_distance_from_home = np.log10(distance_from_home)
    if np.log10(distance_from_home) == -np.inf:
        log_distance_from_home = 0

    log_job_level = np.log10(job_level)

    married = st.selectbox("Married?", no_yes)
    married = no_yes.index(married)

    monthly_income = st.number_input("Monthly Income", min_value=0)

    log_monthly_income = np.log10(monthly_income)
    if log_monthly_income == -np.inf:
        log_monthly_income = 0

    monthly_rate = st.number_input("Monthly Rate", min_value=0)

    non_travel = st.selectbox("Non-Travel Employee?", no_yes)
    non_travel = no_yes.index(non_travel)

    num_companies_worked = st.number_input("Number of Companies Worked", min_value=1)

    log_num_companies_worked = np.log10(num_companies_worked)
    if log_num_companies_worked == -np.inf:
        log_num_companies_worked = 0

    over_18 = st.selectbox("Over 18", no_yes)
    over_18 = no_yes.index(over_18)

    overtime = st.selectbox("Overtime", no_yes)
    overtime = no_yes.index(overtime)

    percent_salary_hike = st.number_input("Percent Salary Hike", min_value=0)

    log_percent_salary_hike = np.log10(percent_salary_hike)
    if log_percent_salary_hike == -np.inf:
        log_percent_salary_hike = 0

    ratings = ['Low', 'Good', 'Excellent', 'Outstanding']
    performance_rating = st.selectbox("Performance Rating", ratings)
    performance_rating = ratings.index(performance_rating) + 1

    relationship_satisfaction = st.selectbox("Relationship Satisfaction", satisfaction)
    relationship_satisfaction = satisfaction.index(relationship_satisfaction) + 1

    overall_satisfaction = environment_satisfaction + job_satisfaction + relationship_satisfaction

    single = st.selectbox("Single?", no_yes)
    single = no_yes.index(single)

    standard_hours = 80

    stock_option_level = st.number_input("Stock Option Level", min_value=0, max_value=3)

    total_working_years = st.number_input("Total Working Years", min_value=0)

    log_total_working_years = np.log10(total_working_years)
    if log_total_working_years == -np.inf:
        log_total_working_years = 0

    num_years_at_each_company = total_working_years / num_companies_worked

    training_times_last_year = st.number_input("Training Times Last Year", min_value=0, max_value=10)

    travel_frequently = st.selectbox("Travel Frequently?", no_yes)
    travel_frequently = no_yes.index(travel_frequently)

    travel_rarely = st.selectbox("Travel Rarely?", no_yes)
    travel_rarely = no_yes.index(travel_rarely)

    balance = ['Bad', 'Good', 'Better', 'Best']
    work_life_balance = st.selectbox("Work/Life Balance", balance)
    work_life_balance = balance.index(work_life_balance) + 1

    years_at_company = st.number_input("Years At Company", min_value=1)

    log_years_at_company = np.log10(years_at_company)

    years_at_other_companies = st.number_input("Years At Other Companies", min_value=0)

    years_in_current_role = st.number_input("Years In Current Role", min_value=0)

    years_since_last_promotion = st.number_input("Years Since Last Promotion", min_value=0)

    years_with_curr_manager = st.number_input("Years With Current Manager", min_value=0)

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
        st.markdown("<h1>The prediction is that the employee <span style='color: green'>WILL NOT CHURN</span>.</h1>", unsafe_allow_html=True)

st.write(df)
