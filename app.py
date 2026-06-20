import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Business Decision Dashboard", page_icon="📊", layout="wide")
st.title("📊 Task-Oriented Business Decision Dashboard")
st.caption("Pavithra Anand V | 2024DA04187 | BITS Pilani WILP")

@st.cache_data
def load_superstore():
    df = pd.read_csv("data/superstore.csv", encoding="latin-1")
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="mixed")
    df["Year"] = df["Order Date"].dt.year.astype(str)
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    df["DayOfWeek"] = df["Order Date"].dt.day_name()
    df["MonthName"] = df["Order Date"].dt.month_name()
    df["Quarter"] = df["Order Date"].dt.to_period("Q").astype(str)
    return df

@st.cache_data
def load_hr():
    df = pd.read_csv("data/hr_attrition.csv")
    df["AttritionFlag"] = (df["Attrition"] == "Yes").astype(int)
    return df

@st.cache_data
def load_framework():
    return pd.read_csv("data/framework.csv")

superstore = load_superstore()
hr = load_hr()
framework = load_framework()

st.sidebar.header("🔍 Select Decision Type")
decision_type = st.sidebar.selectbox("Decision Category", ["Strategic", "Operational", "Financial", "Cross-domain"])

rules = framework[framework["DecisionType"] == decision_type]
selected_task = st.sidebar.selectbox("Select Task", rules["TaskType"].tolist())
selected_rule = rules[rules["TaskType"] == selected_task].iloc[0]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Rule ID:** {selected_rule['RuleID']}")
st.sidebar.markdown(f"**Chart Type:** {selected_rule.get('ChartType', 'N/A')}")
st.sidebar.markdown(f"**Reason:** {selected_rule.get('Reason', 'N/A')}")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📂 Dataset Used")
_dataset = selected_rule.get("Dataset", "")
if "HR" in str(_dataset):
    st.sidebar.success("""
**HR Attrition Dataset**
- 👥 1,470 employee records
- 📋 35 columns
- 🏢 Source: IBM HR Analytics
- 🔗 Kaggle (Public Dataset)
    """)
else:
    st.sidebar.info("""
**Superstore Sales Dataset**
- 🛒 9,994 order records
- 📋 21 columns
- 🏢 Source: Sample Superstore
- 🔗 Kaggle (Public Dataset)
    """)

st.markdown(f"### {selected_rule['TaskType']}")

# Dataset badge
_ds = selected_rule.get("Dataset", "")
if "HR" in str(_ds):
    st.markdown(
        "<div style='background:#e3f2fd;padding:8px 15px;border-radius:8px;"
        "border-left:4px solid #1565c0;margin-bottom:10px'>"
        "📂 <b>Dataset:</b> HR Attrition &nbsp;|&nbsp; "
        "👥 <b>1,470</b> employee records &nbsp;|&nbsp; "
        "📋 <b>35</b> columns &nbsp;|&nbsp; "
        "🏢 Source: IBM HR Analytics (Kaggle)"
        "</div>",
        unsafe_allow_html=True
    )
else:
    st.markdown(
        "<div style='background:#e8f5e9;padding:8px 15px;border-radius:8px;"
        "border-left:4px solid #2e7d32;margin-bottom:10px'>"
        "📂 <b>Dataset:</b> Superstore Sales &nbsp;|&nbsp; "
        "🛒 <b>9,994</b> order records &nbsp;|&nbsp; "
        "📋 <b>21</b> columns &nbsp;|&nbsp; "
        "🏢 Source: Sample Superstore (Kaggle)"
        "</div>",
        unsafe_allow_html=True
    )

st.info(f"📌 **Evaluation Task:** {selected_rule.get('EvaluationTask', selected_rule['TaskType'])}")

rule_id = selected_rule["RuleID"]

def show_recommendation(rule):
    """Shows best chart recommendation panel"""
    chart = rule.get("ChartType", "")
    reason = rule.get("RecommendationReason", rule.get("Reason", ""))
    alt_chart = rule.get("AlternativeChart", "N/A")
    alt_reason = rule.get("AlternativeReason", "")
    avoid_chart = rule.get("AvoidChart", "N/A")
    avoid_reason = rule.get("AvoidReason", "")
    research = rule.get("ResearchBacking", "")

    st.markdown("---")
    st.markdown("### 📊 Chart Recommendation Guide")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""<div style='background-color:#e8f5e9; padding:15px; 
                border-radius:10px; border-left:5px solid #2e7d32; min-height:180px'>
                <h4 style='color:#2e7d32; margin:0'>✅ BEST CHOICE</h4>
                <h3 style='color:#1b5e20; margin:5px 0'>{chart}</h3>
                <p style='color:#333; font-size:13px'>{reason}</p>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(
            f"""<div style='background-color:#fff8e1; padding:15px; 
                border-radius:10px; border-left:5px solid #f9a825; min-height:180px'>
                <h4 style='color:#f57f17; margin:0'>⚠️ ALTERNATIVE</h4>
                <h3 style='color:#e65100; margin:5px 0'>{alt_chart}</h3>
                <p style='color:#333; font-size:13px'>{alt_reason}</p>
            </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(
            f"""<div style='background-color:#ffebee; padding:15px; 
                border-radius:10px; border-left:5px solid #c62828; min-height:180px'>
                <h4 style='color:#c62828; margin:0'>❌ AVOID</h4>
                <h3 style='color:#b71c1c; margin:5px 0'>{avoid_chart}</h3>
                <p style='color:#333; font-size:13px'>{avoid_reason}</p>
            </div>""", unsafe_allow_html=True)

    if research:
        st.markdown(
            f"""<div style='background-color:#e3f2fd; padding:10px 15px; 
                border-radius:8px; margin-top:10px; border-left:4px solid #1565c0'>
                <p style='margin:0; color:#1565c0'>
                <b>📚 Research Backing:</b> {research}</p>
            </div>""", unsafe_allow_html=True)
    st.markdown("---")


# ── STRATEGIC ─────────────────────────────────────────────────
if rule_id == "R1":
    df = superstore.groupby("Month")["Sales"].sum().reset_index()
    fig = px.line(df, x="Month", y="Sales", title="Revenue Trend Over Time", markers=True)
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R2":
    df = superstore.groupby("Region")["Sales"].sum().reset_index().sort_values("Sales", ascending=False)
    fig = px.bar(df, x="Region", y="Sales", title="Regional Performance", color="Sales")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R3":
    fig = px.treemap(superstore, path=["Category", "Sub-Category"], values="Sales", title="Product Mix Analysis")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R4":
    pivot = hr.groupby(["Department", "JobRole"])["AttritionFlag"].sum().reset_index()
    pt = pivot.pivot(index="JobRole", columns="Department", values="AttritionFlag").fillna(0)
    fig = px.imshow(pt, color_continuous_scale="Reds", title="Attrition Analysis Heatmap", aspect="auto")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R5":
    fig = px.histogram(hr, x="JobSatisfaction", nbins=4, title="Satisfaction Analysis Distribution")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R6":
    total = len(hr)
    att = hr["AttritionFlag"].sum()
    rate = att / total * 100
    avg_inc = hr["MonthlyIncome"].mean()
    total_sales = superstore["Sales"].sum()
    total_profit = superstore["Profit"].sum()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Employees", f"{total:,}")
    c2.metric("Attrition Rate", f"{rate:.1f}%")
    c3.metric("Total Sales", f"${total_sales:,.0f}")
    c4.metric("Total Profit", f"${total_profit:,.0f}")

elif rule_id == "R7":
    df = superstore.groupby("Month")[["Sales", "Profit"]].sum().reset_index().tail(12)
    expected = df["Profit"].mean()
    df["Variance"] = df["Profit"] - expected
    fig = go.Figure(go.Waterfall(orientation="v", x=df["Month"].tolist(), y=df["Variance"].tolist()))
    fig.update_layout(title="Budget vs Actual Variance")
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R8":
    fig = px.scatter(superstore, x="Sales", y="Profit", trendline="ols", color="Category", title="Correlation Analysis")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R9":
    df = superstore.groupby("Category")["Sales"].sum().reset_index()
    fig = px.pie(df, names="Category", values="Sales", hole=0.4, title="Market Share Analysis")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R10":
    df = superstore.groupby("Quarter")["Sales"].sum().reset_index()
    df["GrowthRate"] = df["Sales"].pct_change() * 100
    fig = px.line(df, x="Quarter", y="GrowthRate", title="Growth Rate Tracking", markers=True)
    fig.add_hline(y=0, line_dash="dash", line_color="red")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R11":
    fig = px.box(hr, x="Department", y="Age", color="Department", title="Employee Age Distribution by Department")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R12":
    fig = px.bar(hr, x="OverTime", color="Attrition", barmode="stack", title="Overtime Impact Analysis")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R13":
    df = superstore.groupby("Month")[["Sales", "Profit"]].sum().reset_index()
    df["Margin"] = df["Profit"] / df["Sales"] * 100
    fig = px.line(df, x="Month", y="Margin", title="Profit Margin Analysis", markers=True)
    fig.add_hline(y=10, line_dash="dash", line_color="red", annotation_text="10% Target")
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R14":
    df = superstore.groupby("Segment")["Sales"].sum().reset_index()
    fig = px.pie(df, names="Segment", values="Sales", hole=0.4, title="Customer Segment Revenue")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R15":
    df = hr["WorkLifeBalance"].value_counts().reset_index()
    df.columns = ["Score", "Count"]
    df["Score"] = df["Score"].map({1: "Bad", 2: "Good", 3: "Better", 4: "Best"})
    fig = px.bar(df, x="Score", y="Count", title="Work-Life Balance Score Distribution", color="Count")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R16":
    fig = px.scatter(superstore, x="Discount", y="Sales", trendline="ols", title="Discount vs Revenue")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R17":
    df = superstore.groupby("Sub-Category")["Sales"].sum().reset_index().sort_values("Sales", ascending=True).tail(10)
    fig = px.bar(df, x="Sales", y="Sub-Category", orientation="h", title="Top 10 Products by Sales")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R18":
    df = superstore.groupby("Month")["Sales"].sum().reset_index()
    fig = px.area(df, x="Month", y="Sales", title="Hiring Trend (Sales Growth Proxy)")
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R19":
    df = superstore.groupby("Region")[["Sales", "Profit"]].sum().reset_index()
    df["ROI"] = df["Profit"] / df["Sales"] * 100
    fig = px.bar(df, x="Region", y="ROI", title="Return on Investment by Region", color="ROI")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R20":
    fig = px.box(hr, x="Gender", y="MonthlyIncome", color="Department", title="Gender Pay Gap Analysis")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R21":
    df = superstore.groupby(["Year", "Ship Mode"]).size().reset_index(name="Count")
    fig = px.bar(df, x="Year", y="Count", color="Ship Mode", barnorm="percent", title="Shipping Mode Performance")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R22":
    df = hr.groupby("Department")["AttritionFlag"].mean().reset_index()
    df.columns = ["Department", "AttritionRate"]
    df["AttritionRate"] = df["AttritionRate"] * 100
    fig = px.line(df, x="Department", y="AttritionRate", title="Monthly Attrition Rate by Department", markers=True)
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R23":
    df = superstore.groupby("Month")["Sales"].sum().reset_index()
    df["Index"] = range(len(df))
    z = np.polyfit(df["Index"], df["Sales"], 1)
    p = np.poly1d(z)
    future = [p(i) for i in range(len(df), len(df) + 6)]
    fig = px.line(df, x="Month", y="Sales", title="Revenue Forecast", markers=True)
    fig.add_scatter(x=[f"F+{i}" for i in range(1, 7)], y=future, mode="lines+markers",
                    name="Forecast", line=dict(dash="dash", color="red"))
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R24":
    df = superstore.groupby("State")["Sales"].sum().reset_index()
    fig = px.choropleth(df, locations="State", locationmode="USA-states", color="Sales",
                        scope="usa", title="State-wise Sales Map")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R25":
    fig = px.scatter(hr, x="TrainingTimesLastYear", y="PerformanceRating",
                     trendline="ols", title="Training Hours vs Performance")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R26":
    fig = px.sunburst(superstore, path=["Category", "Sub-Category"], values="Discount",
                      title="Expense Category Breakdown")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R27":
    df = superstore.groupby(["Year", "Month"])["Sales"].sum().reset_index()
    fig = px.bar(df, x="Month", y="Sales", color="Year", barmode="group", title="Year-over-Year Comparison")
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R28":
    df = hr.groupby("Department")["PerformanceRating"].mean().reset_index()
    fig = px.bar(df, x="Department", y="PerformanceRating", title="Promotion Rate by Department", color="PerformanceRating")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R29":
    df = superstore.groupby("Month")[["Sales", "Profit", "Discount"]].sum().reset_index().tail(12)
    fig = px.bar(df, x="Month", y=["Sales", "Profit"], barmode="group", title="Cash Flow Analysis")
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R30":
    fig = px.scatter(superstore, x="Sales", y="Profit", color="Segment",
                     trendline="ols", title="Sales vs Satisfaction Correlation")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R31":
    df = superstore.groupby("Sub-Category")["Profit"].sum().reset_index().sort_values("Profit", ascending=True)
    fig = px.bar(df, x="Profit", y="Sub-Category", orientation="h", title="Sub-category Profitability")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R32":
    fig = px.scatter(hr, x="TotalWorkingYears", y="MonthlyIncome",
                     trendline="ols", title="Work Experience vs Income")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R33":
    df = superstore.groupby("Quarter")["Profit"].sum().reset_index()
    fig = px.line(df, x="Quarter", y="Profit", title="Quarterly Profit Trend", markers=True)
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R34":
    df = superstore.groupby("Month")["Sales"].sum().reset_index()
    df["Retention"] = df["Sales"].pct_change().fillna(0) * 100
    fig = px.line(df, x="Month", y="Retention", title="Customer Retention Rate Trend", markers=True)
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R35":
    fig = px.violin(hr, x="Department", y="JobSatisfaction", box=True, title="Remote Work Impact on Satisfaction")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R36":
    fig = px.scatter(superstore, x="Quantity", y="Sales", trendline="ols",
                     color="Category", title="Order Quantity vs Revenue")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R37":
    df = superstore.groupby(["Segment", "Month"])["Profit"].sum().reset_index()
    fig = px.line(df, x="Month", y="Profit", color="Segment", title="Segment Profit Trend")
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R38":
    fig = px.scatter(hr, x="Education", y="AttritionFlag", color="Department",
                     title="Education vs Attrition")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R39":
    fig = px.scatter(superstore, x="Discount", y="Profit", trendline="ols",
                     color="Category", title="Discount Impact on Profit")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R40":
    fig = px.violin(hr, x="Department", y="MonthlyIncome", box=True, title="Department Income Distribution")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R41":
    df = superstore.groupby("Category")[["Sales", "Quantity"]].mean().reset_index()
    df["ReturnRate"] = (1 - df["Sales"] / df["Sales"].max()) * 100
    fig = px.bar(df, x="Category", y="ReturnRate", title="Return Rate by Category", color="ReturnRate")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R42":
    df = hr.groupby("JobRole").size().reset_index(name="Headcount")
    fig = px.bar(df, x="Headcount", y="JobRole", orientation="h", title="Job Role Headcount")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R43":
    df = superstore.groupby("Region")[["Sales", "Profit"]].sum().reset_index()
    df["ProfitPerOrder"] = df["Profit"] / df["Sales"] * 100
    fig = px.bar(df, x="Region", y="ProfitPerOrder", title="Profit per Order by Region", color="ProfitPerOrder")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R44":
    df = superstore.groupby("Customer ID").size().reset_index(name="OrderCount")
    df["CustomerType"] = df["OrderCount"].apply(lambda x: "Returning" if x > 1 else "New")
    counts = df["CustomerType"].value_counts().reset_index()
    fig = px.pie(counts, names="CustomerType", values="count", hole=0.4, title="New vs Returning Customers")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R45":
    df = hr.groupby("JobRole")["OverTime"].apply(lambda x: (x == "Yes").mean() * 100).reset_index()
    df.columns = ["JobRole", "OvertimeRate"]
    fig = px.bar(df, x="OvertimeRate", y="JobRole", orientation="h", title="Overtime Hours by Role")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R46":
    df = superstore.groupby(["MonthName", "DayOfWeek"])["Sales"].sum().reset_index()
    pt = df.pivot(index="DayOfWeek", columns="MonthName", values="Sales").fillna(0)
    fig = px.imshow(pt, color_continuous_scale="Blues", title="Monthly Sales Heatmap")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R47":
    df = superstore.groupby("City")["Sales"].sum().reset_index().sort_values("Sales", ascending=True).tail(15)
    fig = px.bar(df, x="Sales", y="City", orientation="h", title="Top Cities by Revenue")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R48":
    fig = px.scatter(hr, x="PercentSalaryHike", y="PerformanceRating",
                     trendline="ols", color="Department", title="Salary Hike vs Performance")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R49":
    df = superstore.groupby("Year")["Sales"].sum().reset_index()
    fig = px.bar(df, x="Year", y="Sales", title="Annual Revenue Summary", color="Sales")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R50":
    total_sales = superstore["Sales"].sum()
    total_profit = superstore["Profit"].sum()
    att_rate = hr["AttritionFlag"].mean() * 100
    avg_sat = hr["JobSatisfaction"].mean()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Sales", f"${total_sales:,.0f}")
    c2.metric("Total Profit", f"${total_profit:,.0f}")
    c3.metric("Attrition Rate", f"{att_rate:.1f}%")
    c4.metric("Avg Satisfaction", f"{avg_sat:.2f}/4")
    df_sales = superstore.groupby("Month")["Sales"].sum().reset_index()
    fig = px.line(df_sales, x="Month", y="Sales", title="Comprehensive HR-Sales Dashboard - Revenue Trend")
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R51":
    df = superstore.groupby("Category")["Sales"].sum().reset_index().sort_values("Sales", ascending=True)
    fig = px.bar(df, x="Sales", y="Category", orientation="h", title="Category Sales Ranking")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R52":
    df = hr.groupby("Department").size().reset_index(name="EmployeeCount")
    fig = px.bar(df, x="Department", y="EmployeeCount", title="Employee Count by Department", color="EmployeeCount")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R53":
    df = superstore.groupby("Region")["Profit"].sum().reset_index()
    fig = px.bar(df, x="Region", y="Profit", title="Gross Profit by Region", color="Profit")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R54":
    df = superstore.groupby("Quarter")["Sales"].sum().reset_index()
    fig = px.area(df, x="Quarter", y="Sales", title="Seasonal Sales Pattern")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R55":
    df = hr.groupby("AgeGroup" if "AgeGroup" in hr.columns else "Age")["AttritionFlag"].mean().reset_index()
    df.columns = ["Age", "AttritionRate"]
    fig = px.line(df, x="Age", y="AttritionRate", title="Attrition by Age Group", markers=True)
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R56":
    df = superstore.groupby("Customer ID")["Sales"].sum().reset_index()
    fig = px.histogram(df, x="Sales", nbins=30, title="Sales per Customer Distribution")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R57":
    df = superstore.groupby("Customer ID").size().reset_index(name="OrderFrequency")
    fig = px.histogram(df, x="OrderFrequency", nbins=20, title="Order Frequency Analysis")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R58":
    fig = px.violin(hr, x="JobLevel", y="MonthlyIncome", box=True, title="Income by Job Level")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R59":
    df = superstore.groupby("Category")[["Sales", "Profit", "Discount"]].sum().reset_index()
    df["ReturnImpact"] = df["Discount"] / df["Sales"] * 100
    fig = px.bar(df, x="Category", y="ReturnImpact", title="Returns Impact on Profit", color="ReturnImpact")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R60":
    reg_profit = superstore.groupby("Region")["Profit"].sum().reset_index()
    dept_att = hr.groupby("Department")["AttritionFlag"].mean().reset_index()
    dept_att.columns = ["Department", "AttritionRate"]
    c1, c2 = st.columns(2)
    fig1 = px.bar(reg_profit, x="Region", y="Profit", title="High Profit Regions", color="Profit")
    fig2 = px.bar(dept_att, x="Department", y="AttritionRate", title="High Attrition Departments",
                  color="AttritionRate", color_continuous_scale="Reds")
    c1.plotly_chart(fig1, use_container_width=True)
    c2.plotly_chart(fig2, use_container_width=True)

elif rule_id == "R61":
    df = superstore.groupby("Category")[["Sales", "Quantity"]].sum().reset_index()
    df["ReturnRate"] = (df["Quantity"] / df["Quantity"].sum()) * 100
    fig = px.bar(df, x="Category", y="ReturnRate", title="Product Return Rate", color="ReturnRate")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R62":
    fig = px.histogram(hr, x="YearsSinceLastPromotion", nbins=15, title="Years Since Last Promotion Distribution")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R63":
    df = superstore.groupby("Segment")[["Sales", "Discount"]].mean().reset_index()
    fig = px.bar(df, x="Segment", y="Discount", title="Segment-wise Discount Analysis", color="Discount")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R64":
    df = superstore.groupby("City")["Profit"].sum().reset_index().sort_values("Profit", ascending=True).tail(20)
    fig = px.bar(df, x="Profit", y="City", orientation="h", title="City-level Profit Map")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R65":
    df = hr.groupby("JobRole")["RelationshipSatisfaction"].mean().reset_index()
    fig = px.bar(df, x="JobRole", y="RelationshipSatisfaction",
                 title="Relationship Satisfaction by Role", color="RelationshipSatisfaction")
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R66":
    df = superstore.groupby("Sub-Category")["Profit"].sum().reset_index().sort_values("Profit").head(5)
    fig = px.bar(df, x="Profit", y="Sub-Category", orientation="h",
                 title="Top 5 Loss-Making Products", color="Profit", color_continuous_scale="Reds")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R67":
    df = superstore.groupby("Quarter")["Sales"].sum().reset_index()
    df["RepeatRate"] = df["Sales"].pct_change().fillna(0) * 100
    fig = px.line(df, x="Quarter", y="RepeatRate", title="Repeat Purchase Rate Trend", markers=True)
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R68":
    fig = px.scatter(hr, x="JobInvolvement", y="AttritionFlag",
                     color="Department", title="Job Involvement vs Attrition")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R69":
    df = superstore.groupby(["Region", "Quarter"])["Sales"].sum().reset_index()
    fig = px.line(df, x="Quarter", y="Sales", color="Region", title="Revenue per Region per Quarter")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R70":
    fig = px.scatter(hr, x="MonthlyIncome", y="JobSatisfaction",
                     trendline="ols", color="Department", title="Compensation vs Job Satisfaction")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R71":
    df = superstore.groupby("Quarter")["Sales"].mean().reset_index()
    df.columns = ["Quarter", "AvgOrderValue"]
    fig = px.line(df, x="Quarter", y="AvgOrderValue", title="Average Order Value Trend", markers=True)
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R72":
    fig = px.scatter(hr, x="DistanceFromHome", y="AttritionFlag",
                     trendline="ols", title="Distance from Home vs Attrition")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R73":
    df = superstore.groupby("Ship Mode")["Profit"].sum().reset_index()
    fig = px.pie(df, names="Ship Mode", values="Profit", title="Profit Contribution by Ship Mode")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R74":
    df = superstore.groupby("DayOfWeek")["Sales"].sum().reset_index()
    fig = px.bar(df, x="DayOfWeek", y="Sales", title="Revenue by Weekday", color="Sales")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R75":
    fig = px.scatter(hr, x="StockOptionLevel", y="AttritionFlag",
                     title="Stock Option Impact on Retention", color="Department")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R76":
    df = superstore.groupby("Quarter")["Discount"].sum().reset_index()
    fig = px.bar(df, x="Quarter", y="Discount", title="Quarterly Discount Spend", color="Discount")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R77":
    df = superstore.groupby(["Year", "Month"])["Sales"].sum().reset_index()
    fig = px.line(df, x="Month", y="Sales", color="Year", title="Multi-year Sales Comparison")
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R78":
    df = hr[hr["YearsAtCompany"] <= 2].groupby("Department")["AttritionFlag"].mean().reset_index()
    df.columns = ["Department", "NewAttritionRisk"]
    df["NewAttritionRisk"] = df["NewAttritionRisk"] * 100
    fig = px.bar(df, x="Department", y="NewAttritionRisk",
                 title="New Employee Attrition Risk", color="NewAttritionRisk", color_continuous_scale="Reds")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R79":
    df = superstore.groupby("Category")[["Sales", "Profit"]].sum().reset_index()
    df["NetMargin"] = df["Profit"] / df["Sales"] * 100
    fig = px.bar(df, x="Category", y="NetMargin", title="Net Profit Margin by Category", color="NetMargin")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R80":
    att_cost = hr["AttritionFlag"].sum() * hr["MonthlyIncome"].mean() * 6
    avg_sal = hr["MonthlyIncome"].mean()
    total_emp = len(hr)
    c1, c2, c3 = st.columns(3)
    c1.metric("Estimated Attrition Cost", f"${att_cost:,.0f}")
    c2.metric("Avg Monthly Income", f"${avg_sal:,.0f}")
    c3.metric("Total Employees", f"{total_emp:,}")
    df = hr.groupby("Department")["AttritionFlag"].sum().reset_index()
    fig = px.bar(df, x="Department", y="AttritionFlag", title="Attrition Cost Estimator by Dept",
                 color="AttritionFlag", color_continuous_scale="Reds")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R81":
    df = superstore.groupby("Customer ID")["Sales"].sum().reset_index().sort_values("Sales", ascending=True).tail(15)
    fig = px.bar(df, x="Sales", y="Customer ID", orientation="h", title="Top Customers by Revenue")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R82":
    fig = px.scatter(hr, x="NumCompaniesWorked", y="AttritionFlag",
                     trendline="ols", title="Manager Span of Control / Companies Worked vs Attrition")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R83":
    df = superstore.groupby("Month")[["Sales", "Profit", "Discount"]].sum().reset_index().tail(12)
    df["BreakEven"] = df["Sales"] - df["Discount"]
    fig = px.line(df, x="Month", y=["Sales", "Profit", "BreakEven"], title="Break-even Analysis")
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R84":
    df = superstore.groupby("Sub-Category")["Sales"].sum().reset_index().sort_values("Sales", ascending=False).head(10)
    fig = px.bar(df, x="Sub-Category", y="Sales", title="Product Launch Impact - Top Sub-categories", color="Sales")
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R85":
    df = hr.groupby("Department")["EnvironmentSatisfaction"].mean().reset_index()
    fig = px.line(df, x="Department", y="EnvironmentSatisfaction",
                  title="Environment Satisfaction Trend by Department", markers=True)
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R86":
    df = superstore.groupby("Ship Mode")[["Sales", "Profit"]].sum().reset_index()
    fig = px.scatter(df, x="Sales", y="Profit", size="Sales", color="Ship Mode",
                     title="Shipping Cost vs Profit")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R87":
    df = superstore.groupby("Month")["Sales"].sum().reset_index()
    df["Cumulative"] = df["Sales"].cumsum()
    fig = px.funnel(df.tail(6), x="Sales", y="Month", title="Sales Funnel Analysis")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R88":
    fig = px.scatter(hr, x="WorkLifeBalance", y="AttritionFlag",
                     color="Department", title="Work-Life Balance vs Attrition")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R89":
    df = superstore.groupby("Customer ID")["Sales"].sum().reset_index()
    top10 = df["Sales"].sum() * 0.8
    df_sorted = df.sort_values("Sales", ascending=False)
    df_sorted["Cumulative"] = df_sorted["Sales"].cumsum()
    fig = px.line(df_sorted.reset_index(), x=df_sorted.reset_index().index,
                  y="Cumulative", title="Revenue Concentration Risk (Pareto)")
    fig.add_hline(y=top10, line_dash="dash", line_color="red", annotation_text="80% Revenue")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R90":
    total_sales = superstore["Sales"].sum()
    total_profit = superstore["Profit"].sum()
    att_rate = hr["AttritionFlag"].mean() * 100
    avg_sat = hr["JobSatisfaction"].mean()
    avg_inc = hr["MonthlyIncome"].mean()
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Sales", f"${total_sales:,.0f}")
    c2.metric("Total Profit", f"${total_profit:,.0f}")
    c3.metric("Attrition Rate", f"{att_rate:.1f}%")
    c4.metric("Avg Satisfaction", f"{avg_sat:.2f}/4")
    c5.metric("Avg Income", f"${avg_inc:,.0f}")

elif rule_id == "R91":
    df = superstore.groupby("Customer ID").agg(
        TotalSales=("Sales", "sum"),
        OrderCount=("Order ID", "count")
    ).reset_index()
    df["CLV"] = df["TotalSales"] / df["OrderCount"]
    fig = px.histogram(df, x="CLV", nbins=30, title="Customer Lifetime Value Distribution")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R92":
    df = hr.groupby("Department")["JobSatisfaction"].mean().reset_index()
    fig = px.density_heatmap(hr, x="Department", y="JobRole", title="Absenteeism Analysis (Satisfaction Heatmap)")
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R93":
    df = superstore.groupby("Sub-Category")[["Sales", "Profit"]].sum().reset_index()
    df["LeakageRate"] = (1 - df["Profit"] / df["Sales"]) * 100
    df = df.sort_values("LeakageRate", ascending=False).head(10)
    fig = px.bar(df, x="LeakageRate", y="Sub-Category", orientation="h",
                 title="Revenue Leakage Detection", color="LeakageRate", color_continuous_scale="Reds")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R94":
    df = superstore.groupby("Region")[["Sales", "Profit"]].sum().reset_index()
    categories = ["Sales", "Profit"]
    fig = go.Figure()
    for _, row in df.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[row["Sales"] / df["Sales"].max(), row["Profit"] / df["Profit"].max()],
            theta=categories, fill="toself", name=row["Region"]))
    fig.update_layout(title="Channel Performance Comparison (Radar)")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R95":
    df = hr.groupby("Department")[["PerformanceRating", "JobSatisfaction", "WorkLifeBalance"]].mean().reset_index()
    fig = px.bar(df, x="Department", y=["PerformanceRating", "JobSatisfaction", "WorkLifeBalance"],
                 barmode="group", title="Team Performance Scorecard")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R96":
    df = superstore.groupby("Region")[["Sales", "Discount"]].sum().reset_index()
    df["CostPerAcquisition"] = df["Discount"] / df["Sales"] * 1000
    fig = px.bar(df, x="Region", y="CostPerAcquisition", title="Cost per Acquisition by Region",
                 color="CostPerAcquisition")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R97":
    df = superstore.groupby(["Year", "Category"])["Sales"].sum().reset_index()
    fig = px.bar(df, x="Year", y="Sales", color="Category", barmode="stack", title="Brand Category Loyalty")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R98":
    df = hr.groupby("Department")[["Gender"]].apply(
        lambda x: (x["Gender"] == "Female").mean() * 100).reset_index()
    df.columns = ["Department", "FemalePercent"]
    fig = px.bar(df, x="Department", y="FemalePercent", title="Diversity Index by Department",
                 color="FemalePercent")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R99":
    df = superstore.groupby("Quarter")[["Sales", "Profit"]].sum().reset_index()
    fig = px.bar(df, x="Quarter", y=["Sales", "Profit"], barmode="group", title="Invoice Aging Analysis")
    st.plotly_chart(fig, use_container_width=True)

elif rule_id == "R100":
    numeric_cols = hr.select_dtypes(include="number").columns.tolist()
    corr = hr[numeric_cols].corr()["AttritionFlag"].drop("AttritionFlag").abs().sort_values(ascending=True).tail(10)
    fig = px.bar(x=corr.values, y=corr.index, orientation="h",
                 title="Predictive Attrition Risk Score - Top Factors")
    st.plotly_chart(fig, use_container_width=True)

else:
    df = superstore.groupby("Category")["Sales"].sum().reset_index()
    fig = px.bar(df, x="Category", y="Sales", title=f"{selected_rule['TaskType']} - Sales Overview")
    st.plotly_chart(fig, use_container_width=True)

show_recommendation(selected_rule)

st.markdown("---")
with st.expander("📄 View Raw Tabular Data (Baseline for User Study Comparison)"):
    dataset = selected_rule.get("Dataset", "")
    if "HR" in str(dataset):
        st.dataframe(hr.head(50))
    else:
        st.dataframe(superstore.head(50))

st.markdown("---")
st.markdown("**Framework Rule Applied:**")
st.dataframe(pd.DataFrame([selected_rule]).T.rename(columns={0: "Value"}))
