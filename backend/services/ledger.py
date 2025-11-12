from ..models.token import DominionToken

def log_token_event(token: DominionToken):
    """Log token issuance event to the Dominion ledger"""
    # For now, just print or append to a file/db
    print(f"""
    [LEDGER] Issued {token.role} token for order #{token.order_id}
          Holder: {token.email}
          Token ID: {token.token_id}
          Issued at: {token.issued_at}
          Verifiable with Dominion public key
    """)
    # Future: persist to Postgres or broadcast to Grafana lineage dashboards
