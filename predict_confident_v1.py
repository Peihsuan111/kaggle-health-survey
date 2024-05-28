import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report

archive_files = glob.glob("archive/*.csv")

# Load and display the first few rows of each CSV file to understand their structure
medications_df = pd.read_csv("archive/medications.csv", encoding="latin1")
diet_df = pd.read_csv("archive/diet.csv", encoding="latin1")
examination_df = pd.read_csv("archive/examination.csv", encoding="latin1")
demographic_df = pd.read_csv("archive/demographic.csv", encoding="latin1")
labs_df = pd.read_csv("archive/labs.csv", encoding="latin1")
questionnaire_df = pd.read_csv("archive/questionnaire.csv", encoding="latin1")

# 數據整合
merged_df = demographic_df.merge(diet_df, on="SEQN", how="inner")
merged_df = merged_df.merge(examination_df, on="SEQN", how="inner")
merged_df = merged_df.merge(labs_df, on="SEQN", how="inner")
merged_df = merged_df.merge(questionnaire_df, on="SEQN", how="inner")

# 特徵工程
merged_df["BMI"] = merged_df["BMXWT"] / (merged_df["BMXHT"] / 100) ** 2
merged_df["Avg_BP"] = (merged_df["BPXSY1"] + 2 * merged_df["BPXDI1"]) / 3

# 創建目標變量：合併重大慢性疾病欄位
merged_df["Chronic_Disease"] = (
    (merged_df["MCQ160A"] == 1)
    | (merged_df["MCQ160B"] == 1)
    | (merged_df["MCQ160C"] == 1)
    | (merged_df["MCQ160F"] == 1)
    | (merged_df["MCQ160E"] == 1)
).astype(int)

# 選擇特徵和目標變量
features = [
    "RIDAGEYR",
    "RIAGENDR",
    "RIDRETH1",
    "DR1TKCAL",
    "DR1TCHOL",
    "BMXWT",
    "BMXHT",
    "BPXSY1",
    "BPXDI1",
    "LBXTC",  # Total Cholesterol
    "LBXHGB",  # Hemoglobin
    "SMQ020",
    "ALQ101",
    "PAQ605",
    "BMI",
    "Avg_BP",
]
X = merged_df[features]
y = merged_df["Chronic_Disease"]

# 填充缺失值
imputer = SimpleImputer(strategy="mean")
X_imputed = imputer.fit_transform(X)

# 保存特徵名稱
feature_names = features

# 分割數據集
X_train, X_test, y_train, y_test = train_test_split(
    X_imputed, y, test_size=0.2, random_state=42
)

# 模型訓練
rf = RandomForestClassifier(random_state=42)
param_grid = {
    "n_estimators": [100, 200],
    "max_depth": [None, 10, 20],
    "min_samples_split": [2, 5],
}
grid_search = GridSearchCV(rf, param_grid, cv=5, scoring="accuracy")
grid_search.fit(X_train, y_train)


def predict_risk_with_confidence(new_data):
    # 必要特徵列表
    required_features = set(features)
    provided_features = set(new_data.keys())
    # 填補缺失特徵
    missing_features = required_features - provided_features
    for feature in missing_features:
        new_data[feature] = np.nan
    new_data_df = pd.DataFrame([new_data])
    # 計算衍生特徵
    if "BMXWT" in new_data_df.columns and "BMXHT" in new_data_df.columns:
        new_data_df["BMI"] = new_data_df["BMXWT"] / (new_data_df["BMXHT"] / 100) ** 2
    if "BPXSY1" in new_data_df.columns and "BPXDI1" in new_data_df.columns:
        new_data_df["Avg_BP"] = (new_data_df["BPXSY1"] + 2 * new_data_df["BPXDI1"]) / 3
    # 重新排列特徵順序
    new_data_df = new_data_df[feature_names]
    # 填充缺失值
    new_data_df_imputed = imputer.transform(new_data_df)
    # 進行預測
    predicted_risk = grid_search.predict(new_data_df_imputed)
    predicted_prob = grid_search.predict_proba(new_data_df_imputed)
    # 計算信心水準
    provided_feature_count = len(provided_features)
    total_feature_count = len(required_features)
    feature_completeness = provided_feature_count / total_feature_count
    # 特徵重要性
    importances = grid_search.best_estimator_.feature_importances_
    importance_sum = sum(importances)
    # 計算提供特徵的總重要性分數
    provided_importance_sum = sum(
        importances[feature_names.index(f)]
        for f in provided_features
        if f in feature_names
    )
    # 信心水準計算
    confidence = (provided_importance_sum / importance_sum) * feature_completeness
    # 分級風險
    risk_level = "低風險"
    if predicted_prob[0][predicted_risk[0]] >= 0.75:
        risk_level = "高風險"
    elif predicted_prob[0][predicted_risk[0]] >= 0.5:
        risk_level = "中風險"
    return risk_level, confidence


# ------------------------------------------------#to-do
# 模型效用評估
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# 模型評估
y_pred = grid_search.predict(X_test)
print(classification_report(y_test, y_pred))

# 混淆矩陣
cm = confusion_matrix(y_test, y_pred, labels=grid_search.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=grid_search.classes_)
disp.plot()
plt.title("Confusion Matrix")
plt.show()

# 特徵重要性
importances = grid_search.best_estimator_.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure()
plt.title("Feature Importances")
plt.bar(range(X.shape[1]), importances[indices], align="center")
plt.xticks(range(X.shape[1]), [features[i] for i in indices], rotation=90)
plt.xlim([-1, X.shape[1]])
plt.show()

# 示範數據示範1
# 示例預測

new_data_example1 = {
    "RIDAGEYR": 55,
    "BMXWT": 70,
    "BMXHT": 170,
    "BPXSY1": 140,
    "BPXDI1": 90,
    "DR1TKCAL": 2000,
    "DR1TCHOL": 300,
    "LBXTC": 200,
    "LBXHGB": 15,
    "SMQ020": 0,
    "ALQ101": 1,
    "PAQ605": 2,
    "RIAGENDR": 1,
    "RIDRETH1": 3,
}
predicted_risk1, confidence1 = predict_risk_with_confidence(new_data_example1)
print(f"Predicted Risk Level: {predicted_risk1}, Confidence: {confidence1:.2f}")
# 示範數據示範2
new_data_example2 = {
    "RIDAGEYR": 45,
    # "BMXWT": 85,
    # "BMXHT": 160,
    # "BPXSY1": 125,
    # "BPXDI1": 80,
    # "DR1TKCAL": 2500,
    # "DR1TCHOL": 350,
    # "LBXTC": 210,
    # "LBXHGB": 13,
    # "SMQ020": 1,
    # "ALQ101": 0,
    # "PAQ605": 3,
    # "RIAGENDR": 1,
    # "RIDRETH1": 3,
}
predicted_risk2, confidence2 = predict_risk_with_confidence(new_data_example2)
print(f"Predicted Risk Level: {predicted_risk2}, Confidence: {confidence2:.2f}")
