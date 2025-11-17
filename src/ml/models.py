"""Modelos de Machine Learning"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import streamlit as st
from typing import Tuple, Dict, Any

from ..config.settings import ML_CONFIG


def prepare_ml_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Prepara dados para ML"""
    if df.empty:
        return pd.DataFrame(), pd.Series()

    features = [f for f in ML_CONFIG['features'] if f in df.columns]
    target = ML_CONFIG['target']

    if not features or target not in df.columns:
        return pd.DataFrame(), pd.Series()

    # Remover NaNs
    df_clean = df[features + [target]].dropna()

    X = df_clean[features]
    y = df_clean[target]

    return X, y


def train_random_forest(df: pd.DataFrame) -> Dict[str, Any]:
    """Treina modelo Random Forest"""
    X, y = prepare_ml_data(df)

    if X.empty or y.empty:
        return {'error': 'Dados insuficientes'}

    # Encode target
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Split dados
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded,
        test_size=ML_CONFIG['test_size'],
        random_state=ML_CONFIG['random_forest']['random_state'],
        stratify=y_encoded
    )

    # Treinar modelo
    rf = RandomForestClassifier(**ML_CONFIG['random_forest'])
    rf.fit(X_train, y_train)

    # Predições
    y_pred = rf.predict(X_test)

    # Métricas
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    class_report = classification_report(
        y_test, y_pred,
        target_names=le.classes_,
        output_dict=True
    )

    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': rf.feature_importances_
    }).sort_values('importance', ascending=False)

    return {
        'model': rf,
        'label_encoder': le,
        'accuracy': accuracy,
        'confusion_matrix': conf_matrix,
        'classification_report': class_report,
        'feature_importance': feature_importance,
        'X_test': X_test,
        'y_test': y_test,
        'y_pred': y_pred
    }


def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """Detecta anomalias com Isolation Forest"""
    features = [f for f in ML_CONFIG['features'][:-1] if f in df.columns]  # Excluir target

    if not features:
        return df

    df_clean = df[features].dropna()

    if df_clean.empty:
        return df

    # Normalizar dados
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_clean)

    # Treinar Isolation Forest
    iso_forest = IsolationForest(**ML_CONFIG['isolation_forest'])
    predictions = iso_forest.fit_predict(X_scaled)
    scores = iso_forest.score_samples(X_scaled)

    # Adicionar resultados ao DataFrame original
    df_result = df.copy()
    df_result['anomaly'] = 0
    df_result['anomaly_score'] = 0.0

    df_result.loc[df_clean.index, 'anomaly'] = predictions
    df_result.loc[df_clean.index, 'anomaly_score'] = scores

    # Converter: -1 para anomalia, 1 para normal
    df_result['is_anomaly'] = df_result['anomaly'] == -1

    return df_result


def get_ml_insights(ml_results: Dict[str, Any]) -> Dict[str, Any]:
    """Extrai insights dos resultados de ML"""
    if 'error' in ml_results:
        return ml_results

    insights = {
        'accuracy_percentage': ml_results['accuracy'] * 100,
        'top_features': ml_results['feature_importance'].head(3).to_dict('records'),
        'class_performance': {},
        'total_predictions': len(ml_results['y_test'])
    }

    # Performance por classe
    for class_name, metrics in ml_results['classification_report'].items():
        if isinstance(metrics, dict):
            insights['class_performance'][class_name] = {
                'precision': metrics.get('precision', 0) * 100,
                'recall': metrics.get('recall', 0) * 100,
                'f1_score': metrics.get('f1-score', 0) * 100
            }

    return insights
