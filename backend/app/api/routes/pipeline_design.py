from fastapi import APIRouter

from app.engineering_core.pipelines.calculator import (
    PipelineInput,
    PipelineResult,
    calculate_pipeline,
)

router = APIRouter(
    prefix="/pipeline-design",
    tags=["Pipeline Design"],
)


@router.post(
    "/calculate",
    response_model=PipelineResult,
)
def calculate(data: PipelineInput):
    return calculate_pipeline(data)