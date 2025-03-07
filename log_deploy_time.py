import sys
import mlflow

# If you pass an argument, use it as the deploy time; otherwise default to 300
deploy_time = float(sys.argv[1]) if len(sys.argv) > 1 else 300

with mlflow.start_run():
    mlflow.log_metric("deploy_time", deploy_time)
    mlflow.set_tag("stage", "deploy")
    mlflow.log_param("pipeline_version", "1.0")
    mlflow.set_tag("project", "CI/CD Optimization")

