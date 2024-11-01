# Pipelines RJ-Iplanrio

## Taxirio

Parâmetros para dump completo de collections do MongoDB:

- `races`:
  - `freq`: M
  - `dump_mode`: overwrite
- `rankingraces`:
  - `freq`: 7D
  - `dump_mode`: overwrite
  - `memory_limit`: 4Gi
- `passengers`
  - `freq`: 2M
  - `dump_mode`: overwrite

# Melhorias

- Adicionar testes unitários para tarefas
- Criar pipelines genéricas para dumps de MongoDB
