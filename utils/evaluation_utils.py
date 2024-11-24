import json
from datetime import datetime
from sklearn.metrics import accuracy_score, f1_score, recall_score

def is_time_period_correct(pred_start, pred_end, true_start, true_end):
    """
    Strictly compare predicted and true time periods.

    Parameters:
        pred_start (str): Predicted start time as a string (e.g., "2024-11-20 09:17").
        pred_end (str): Predicted end time as a string (e.g., "2024-11-20 11:25").
        true_start (str): True start time as a string.
        true_end (str): True end time as a string.

    Returns:
        bool: True if both start and end times match exactly, False otherwise.
    """
    # Convert strings to datetime objects
    pred_start_dt = datetime.strptime(pred_start, "%Y-%m-%d %H:%M")
    pred_end_dt = datetime.strptime(pred_end, "%Y-%m-%d %H:%M")
    true_start_dt = datetime.strptime(true_start, "%Y-%m-%d %H:%M")
    true_end_dt = datetime.strptime(true_end, "%Y-%m-%d %H:%M")

    # Check for exact match
    return pred_start_dt == true_start_dt and pred_end_dt == true_end_dt

def evaluate_label_single(pred, true, weights=None):
    """
    Evaluate a single pair of prediction and true label.

    Parameters:
        pred (dict): Predicted label.
        true (dict): True label.
        weights (dict): Weights for each field except Spam.

    Returns:
        dict: Evaluation results for each field and overall score.
    """
    # print(pred)
    if weights is None:
        # Default weights (Spam is NOT included in the score)
        weights = {
            "Time_Sensitive": 0.2,
            "Type": 0.15,
            "Category": 0.15,
            "Format": 0.1,
            "Time Period": 0.2,
            "Priority_Level": 0.2,
        }

    # Initialize results
    results = {"Field": {}, "Overall Weighted Score": 0}

    # Spam correctness (Denominator)
    spam_correct = 1 if pred["Spam"] == true["Spam"] else 0
    results["Field"]["Spam"] = spam_correct

    # Evaluate fields
    for field in true.keys():
        if field in ["Time_Sensitive", "Type", "Category", "Format"]:
            # Categorical fields
            results["Field"][field] = 1 if pred[field] == true[field] else 0
        elif field in ["Start", "End"]:
            # Time Period
            # If not time sensitive, this will automatically get 1
            if results["Field"]["Time_Sensitive"] == 0:
                results["Field"]["Time Period"] = 1
            else:
                time_correct = is_time_period_correct(
                    pred["Start"], pred["End"], true["Start"], true["End"]
                )
                results["Field"]["Time Period"] = 1 if time_correct else 0
        elif field == "Priority_Level":
            # Priority Level (Relaxed Match)
            priority_map = {"Low": 1, "Medium": 2, "High": 3, "Urgent": 4}
            pred_priority = priority_map[pred[field]]
            true_priority = priority_map[true[field]]
            results["Field"]["Priority_Level"] = 1 if abs(pred_priority - true_priority) <= 1 else 0

    # Calculate weighted score using fields except Spam
    weighted_score = sum(
        results["Field"].get(field, 0) * weights.get(field, 0)
        for field in weights.keys()
    )
    results["Overall Weighted Score"] = weighted_score if spam_correct == 1 else 0
    return results

def calculate_overall_metrics(results_list):
    """
    Calculate overall ACC, F1, and Recall for binary fields, ACC for categorical fields,
    and an averaged weighted score.

    Parameters:
        results_list (list of dict): List of evaluation results for individual predictions.

    Returns:
        dict: Overall metrics for binary fields, categorical fields, and average weighted score.
    """
    # Initialize storage
    binary_fields = ["Spam", "Time_Sensitive"]
    categorical_fields = ["Time Period", "Type", "Category", "Format", "Priority_Level"]

    binary_true = {field: [] for field in binary_fields}
    binary_pred = {field: [] for field in binary_fields}

    categorical_correct = {field: 0 for field in categorical_fields}
    categorical_total = {field: 0 for field in categorical_fields}

    total_weighted_score = 0
    num_results = len(results_list)

    # Aggregate results
    for result in results_list:
        total_weighted_score += result["Overall Weighted Score"]
        for field in result["Field"]:
            if field in binary_fields:
                binary_true[field].append(1)  # True value is always "correct"
                binary_pred[field].append(result["Field"][field])  # Append prediction (0 or 1)
            elif field in categorical_fields:
                categorical_total[field] += 1
                if result["Field"][field] == 1:
                    categorical_correct[field] += 1

    # Calculate metrics for binary fields
    binary_metrics = {}
    for field in binary_fields:
        binary_metrics[field] = {
            "ACC": accuracy_score(binary_true[field], binary_pred[field]),
            "F1": f1_score(binary_true[field], binary_pred[field]),
            "Recall": recall_score(binary_true[field], binary_pred[field]),
        }

    # Calculate accuracy for categorical fields
    categorical_metrics = {
        field: categorical_correct[field] / categorical_total[field]
        for field in categorical_fields
    }

    # Calculate averaged weighted score
    averaged_weighted_score = total_weighted_score / num_results

    return {
        "Binary Metrics": binary_metrics,
        "Categorical Metrics": categorical_metrics,
        "Averaged Weighted Score": averaged_weighted_score,
    }
