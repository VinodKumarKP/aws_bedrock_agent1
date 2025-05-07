module "agent" {
  source = "github.com/VinodKumarKP/capgemini_terraform_aws_bedrock_agent_modules"

  agent_name                  = "${var.component_id}-${var.agent_name}"
  lambda_function_path        = "${path.cwd}/lambda_code"
  lambda_function_description = ""
  lambda_function_name        = "get-product-info"
  lambda_environment_variables = {
    "ENVIRONMENT_VARIABLE_1" = "VALUE_1"
    "ENVIRONMENT_VARIABLE_2" = "VALUE_2"
  }
  # agent_action_group_api_schema = "${path.cwd}/schema.yaml"
  functions_json_file = "${path.cwd}/functions_detail.json"
  lambda_handler      = "product_info.index.lambda_handler"
}