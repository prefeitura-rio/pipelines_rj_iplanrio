# Pipelines RJ-Iplanrio

## Táxi.Rio

Parâmetros para dump completo de collections do MongoDB:

- `races`:
  - `freq`: ME
  - `dump_mode`: overwrite
- `rankingraces`:
  - `freq`: 7D
  - `dump_mode`: overwrite
- `passengers`
  - `freq`: 2ME
  - `dump_mode`: overwrite

# Melhorias

- Adicionar testes unitários para tarefas
- Criar pipelines genéricas para dumps de MongoDB
