from openenv_cli import Client

# Replace with your real API key if required
api_key = "demo-key-or-your-secret"

def init_email_env():
    # Create a client session
    with Client(api_key=api_key) as client:
        print("[*] Connecting to openenv-cli service...")
        client.connect()

        # Define your environment payload
        payload = {
            "env": "email-triage-env",
            "categories": ["urgent", "follow-up", "archive"],
            "rules": [
                {"if": "subject contains 'invoice'", "action": "flag urgent"},
                {"if": "sender is newsletter", "action": "archive"},
                {"if": "subject contains 'meeting'", "action": "mark follow-up"}
            ],
            "actions": ["categorize inbox", "flag urgent", "archive newsletters"]
        }

        # Sync the environment setup
        response = client.sync_data(payload)
        print("[+] Environment initialized:", response)

        # Disconnect gracefully
        client.disconnect()
        print("[-] Connection closed.")

if __name__ == "__main__":
    init_email_env()