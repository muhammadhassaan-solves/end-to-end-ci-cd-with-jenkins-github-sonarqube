import mlflow

# Replace with actual deploy time (fetch dynamically if possible)
deploy_time = 300  

with mlflow.start_run():
    mlflow.log_metric("deploy_time", deploy_time)
    mlflow.log_param("pipeline_stage", "deploy")
    mlflow.set_tag("project", "CI/CD Optimization")
