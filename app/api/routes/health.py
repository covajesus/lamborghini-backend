from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def healthcheck() -> dict[str, str]:
    """
    Liveness probe for the API process.

    @return: Status payload with value "ok"
    """
    return {"status": "ok"}
