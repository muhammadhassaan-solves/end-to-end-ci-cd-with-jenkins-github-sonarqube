import mlflow

with open("deploy_time.txt", "r") as f:
    deploy_time = int(f.read().strip())

with mlflow.start_run():
    mlflow.log_metric("deploy_time", deploy_time)
    mlflow.set_tag("stage", "deploy")
    mlflow.log_param("pipeline_version", "1.0")
    mlflow.set_tag("project", "CI/CD Optimization")

print(f"Logged deploy_time: {deploy_time} seconds to MLflow")
