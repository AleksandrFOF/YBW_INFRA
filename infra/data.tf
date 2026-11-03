data "azurerm_resource_group" "main" {
  name = "rg-poc-demo"
}

data "azurerm_cognitive_account" "openai" {
  name                = "aoai-ci-poc"
  resource_group_name = "rg-poc-demo"
}
