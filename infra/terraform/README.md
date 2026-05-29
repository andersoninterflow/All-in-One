# Terraform

Este diretorio reserva infraestrutura como codigo para ambientes homologados.
O baseline nao cria cloud resources nem segredos automaticamente. Providers,
remote state, KMS/Vault, bancos gerenciados, mensageria, storage e DNS devem
ser escolhidos em ADR antes de aplicar um plano.
