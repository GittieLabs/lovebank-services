import json
from key_management_service.get_secrets import get_secret

if __name__ == "__main__":
    secret_name = "lovebank-secret"
    response = get_secret(secret_name)

    secret_dict = json.loads(response)
    print(secret_dict["KAMATERA_VM_URL"])