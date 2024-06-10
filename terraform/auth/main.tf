resource "aws_ecs_cluster" "auth_cluster" {
  name = "auth-cluster"
}

resource "aws_ecs_task_definition" "auth_task" {
  family                   = "auth-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"

  container_definitions = jsonencode([
    {
      name  = "auth-container"
      image = "your-auth-ecr-repo-url:latest"
      essential = true
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
    }
  ])
}

resource "aws_ecs_service" "auth_service" {
  name            = "auth-service"
  cluster         = aws_ecs_cluster.auth_cluster.id
  task_definition = aws_ecs_task_definition.auth_task.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = ["your-subnet-id"]
    security_groups  = ["your-security-group-id"]
    assign_public_ip = true
  }
}
