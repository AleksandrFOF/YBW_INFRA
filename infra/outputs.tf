output "openai_endpoint" {
  value = data.azurerm_cognitive_account.openai.endpoint
}
output "storage_account_name" {
  value = azurerm_storage_account.analysis.name
}
