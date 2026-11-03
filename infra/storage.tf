resource "azurerm_storage_account" "analysis" {
  name                            = "stcianalysis001"
  resource_group_name             = data.azurerm_resource_group.main.name
  location                        = data.azurerm_resource_group.main.location
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false
}
resource "azurerm_storage_container" "logs" {
  name                  = "logs"
  storage_account_id    = azurerm_storage_account.analysis.id
  container_access_type = "private"
}
resource "azurerm_storage_container" "reports" {
  name                  = "reports"
  storage_account_id    = azurerm_storage_account.analysis.id
  container_access_type = "private"
}
resource "azurerm_storage_container" "samples" {
  name                  = "samples"
  storage_account_id    = azurerm_storage_account.analysis.id
  container_access_type = "private"
}
