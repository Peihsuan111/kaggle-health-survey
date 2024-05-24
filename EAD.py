import matplotlib.pyplot as plt
import seaborn as sns

# 年齡分佈
plt.figure(figsize=(10, 6))
sns.histplot(demographic_df["RIDAGEYR"].dropna(), bins=30, kde=True)
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.show()

# BMI分佈
plt.figure(figsize=(10, 6))
sns.histplot(examination_df["BMXBMI"].dropna(), bins=30, kde=True)
plt.title("BMI Distribution")
plt.xlabel("BMI")
plt.ylabel("Frequency")
plt.show()

# 收縮壓和舒張壓的關係
plt.figure(figsize=(10, 6))
sns.scatterplot(x="BPXSY1", y="BPXDI1", data=examination_df)
plt.title("Systolic vs Diastolic Blood Pressure")
plt.xlabel("Systolic Blood Pressure")
plt.ylabel("Diastolic Blood Pressure")
plt.show()

# 計算相關矩陣
numeric_cols = merged_df.select_dtypes(include=[np.number]).columns.tolist()
correlation_matrix = merged_df.corr()

plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Feature Correlation Matrix")
plt.show()

# 性別分佈
plt.figure(figsize=(10, 6))
sns.countplot(x="RIAGENDR", data=demographic_df)
plt.title("Gender Distribution")
plt.xlabel("Gender")
plt.ylabel("Count")
plt.show()

# 吸煙情況
plt.figure(figsize=(10, 6))
sns.countplot(x="SMQ020", data=questionnaire_df)
plt.title("Smoking Status")
plt.xlabel("Smoked at least 100 cigarettes in life")
plt.ylabel("Count")
plt.show()
