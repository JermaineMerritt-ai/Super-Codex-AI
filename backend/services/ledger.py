
def log_token_event(signed_token: str, role: str, email: str, order_id: str):
      # For now, just print or append to a file/db
            print(f"""
            [LEDGER] Issued {role} token for order #{order_id}
                  Holder: {email}
                  Token: {signed_token[:30]}...
                  Verifiable with Dominion public key
            """)
      # Future: persist to Postgres or broadcast to Grafana lineage dashboards
