import mlflow

with open("build_time.txt", "r") as f:
    build_time = int(f.read().strip())

with mlflow.start_run():
    mlflow.log_metric("build_time", build_time)
    mlflow.set_tag("stage", "build")
    mlflow.log_param("pipeline_version", "1.0")
    mlflow.set_tag("project", "CI/CD Optimization")

print(f"Logged build_time: {build_time} seconds to MLflow")


