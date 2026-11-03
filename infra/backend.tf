terraform {
  backend "azurerm" {
    resource_group_name  = "rg-tfstate-poc"
    storage_account_name = "tfstatepoc12345"
    container_name       = "tfstate"
    key                  = "infra.tfstate"
  }
}
