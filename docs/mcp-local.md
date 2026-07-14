# MCP Local

Commande stdio à brancher dans un client MCP local:

```json
{
  "mcpServers": {
    "fdj-history": {
      "command": "python",
      "args": ["C:\\projets\\mesjeux\\mcp\\fdj_mcp_server.py"]
    }
  }
}
```

Outils exposés:

- `list_games`
- `get_last_result`
- `get_history`
- `search_history`
- `get_statistics`
- `get_snapshot`
- `compare_grid_to_result`
- `generate_balanced_loto_grid`
- `export_csv`

Le serveur lit directement l’historique normalisé local dans `data/*.json` et peut aussi exporter les CSV sur demande.

