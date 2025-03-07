import mlflow

# Replace with actual build time (fetch dynamically if possible)
build_time = 120  

with mlflow.start_run():
    mlflow.log_metric("build_time", build_time)
    mlflow.log_param("pipeline_stage", "build")
    mlflow.set_tag("project", "CI/CD Optimization")
