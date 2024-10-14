from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import hamming_loss, classification_report, f1_score
from scipy.stats import randint
import joblib
import ast
import pandas as pd
import numpy as np
import gc

# 데이터 로드 및 전처리
df = pd.read_csv('bg_dataset.csv')
df['action'] = df['action'].apply(ast.literal_eval)

# 특징과 레이블 분리
X = df[['target_x', 'target_y',
        'vwall1_x', 'vwall1_y', 'vwall2_x', 'vwall2_y', 'vwall3_x', 'vwall3_y',
        'hwall1_x', 'hwall1_y', 'hwall2_x', 'hwall2_y', 'hwall3_x', 'hwall3_y',
        'vobstacle_x', 'vobstacle_y', 'hobstacle_x', 'hobstacle_y']].astype('int8')
y = df['action']  # 여러 개의 최적 각도를 포함하는 리스트

# 레이블 이진 인코딩
mlb = MultiLabelBinarizer(classes=range(0, 182))  # 0~181까지의 각도 (181은 'reset'에 해당)

y_encoded = mlb.fit_transform(y).astype('uint8')

# 데이터 분할 (훈련 세트와 테스트 세트로만 분할)
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2)

# 메모리 절약을 위해 사용하지 않는 데이터 삭제
del df, X, y, y_encoded
gc.collect()

# 튜닝할 하이퍼파라미터와 그 분포 설정
param_dist = {
    'estimator__n_estimators': randint(100, 500),
    'estimator__max_depth': randint(5, 20),
    'estimator__min_samples_split': randint(2, 10),
    'estimator__min_samples_leaf': randint(1, 5),
    'estimator__max_features': ['sqrt', None]
}

# 모델 생성
rf_classifier = MultiOutputClassifier(RandomForestClassifier())

# 랜덤 서치 객체 생성
random_search = RandomizedSearchCV(
    estimator=rf_classifier,
    param_distributions=param_dist,
    n_iter=5,  # 시도할 조합의 수
    scoring='f1_micro',  # 다중 레이블에 적합한 지표 사용
    n_jobs=-1,
    cv=5,
    verbose=1,
    return_train_score=False
)

# 모델 학습 (훈련 세트에서 하이퍼파라미터 튜닝)
random_search.fit(X_train, y_train)

# 메모리 절약을 위해 불필요한 변수 삭제
del rf_classifier, param_dist
gc.collect()

# 최적의 하이퍼파라미터로 모델 재학습 (전체 훈련 세트 사용)
best_params = random_search.best_params_
final_rf_classifier = RandomForestClassifier(
    n_estimators=best_params['estimator__n_estimators'],
    max_depth=best_params['estimator__max_depth'],
    min_samples_split=best_params['estimator__min_samples_split'],
    min_samples_leaf=best_params['estimator__min_samples_leaf'],
    max_features=best_params['estimator__max_features']
)
final_model = MultiOutputClassifier(final_rf_classifier)
final_model.fit(X_train, y_train)

print("최적의 하이퍼파라미터:", best_params)
print("최고 교차 검증 F1-Score (Micro):", random_search.best_score_)

# 모델 평가
y_pred = final_model.predict(X_test)

# Hamming Loss 계산 (잘못 예측된 레이블 비율)
hamming = hamming_loss(y_test, y_pred)
print(f'Hamming Loss: {hamming:.4f}')

# F1-Score 계산
f1_micro = f1_score(y_test, y_pred, average='micro')
f1_macro = f1_score(y_test, y_pred, average='macro')
print(f'F1-Score (Micro): {f1_micro:.4f}')
print(f'F1-Score (Macro): {f1_macro:.4f}')

# 상세한 성능 보고서
report = classification_report(y_test, y_pred)
print("Classification Report:")
print(report)

# 성능 보고서 텍스트로 저장
with open('bg_randomforest_report.txt', 'w') as f:
    f.write(report)

# 모델 저장
joblib.dump(final_model, 'bg_randomforest.pkl')
joblib.dump(mlb, 'bg_randomforest_mlb.pkl')