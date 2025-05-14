module "agent" {
  source = "github.com/VinodKumarKP/capgemini_terraform_aws_bedrock_agent_modules?ref=v1.0.0"  # Pin to specific version

  agent_name                  = "${var.component_id}-${var.agent_name}"
  lambda_function_path        = "${path.cwd}/lambda_code"
  lambda_function_description = ""
  lambda_function_name        = "get-product-info"
  
  # Use variable references instead of hardcoded values
  lambda_environment_variables = {
    "ENVIRONMENT_VARIABLE_1" = var.environment_var_1
    "ENVIRONMENT_VARIABLE_2" = var.environment_var_2
  }
  
  functions_json_file = "${path.cwd}/functions_detail.json"
  lambda_handler      = "product_info.index.lambda_handler"
}