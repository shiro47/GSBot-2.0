from fastapi.responses import JSONResponse
from fastapi_discord import RateLimited, Unauthorized
from fastapi_discord.exceptions import ClientSessionNotInitialized, InvalidToken


async def unauthorized_error_handler(_, e: Unauthorized):
    return JSONResponse({"error": "Unauthorized"}, status_code=401)


async def rate_limit_error_handler(_, e: RateLimited):
    return JSONResponse(
        {"error": "RateLimited", "retry": e.retry_after, "message": e.message},
        status_code=429,
    )

async def client_session_error_handler(_, e: ClientSessionNotInitialized):
    return JSONResponse({"error": "Internal Error"}, status_code=500)

async def invalid_token_error_handler(_, e: InvalidToken):
    return JSONResponse({"error": "Invalid code"}, status_code=500)

def include_app(app):
    app.add_exception_handler(Unauthorized, unauthorized_error_handler)
    app.add_exception_handler(RateLimited, rate_limit_error_handler)
    app.add_exception_handler(ClientSessionNotInitialized, client_session_error_handler)
    app.add_exception_handler(InvalidToken, invalid_token_error_handler)
