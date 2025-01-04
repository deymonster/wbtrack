from pvz_client.api_auth import ApiAuth
from pvz_client.models.AuthModel import TokenResponse


async def main():
    auth_base_path = "https://r-point.wb.ru"
    api_auth = ApiAuth(auth_base_path=auth_base_path, base_path=auth_base_path)
    phone = "79282951709"
    try:
        code_response = await api_auth.login(phone=phone)
        print("Code requested successfully:", code_response)
    except HTTPException as e:
        print(f"Error requesting code: {e}")
        return

    code = input("Enter code received via SMS: ")
    temp_token = code_response.data

    try:
        token_response = await api_auth.validate(code=code, token=temp_token)
        print("Connected successfully, tokens received:")
        print(token_response)
    except HTTPException as e:
        print(f"Error validating code: {e}")
        return


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())