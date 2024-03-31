from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter


play_list_schema = extend_schema(
    parameters=[
        OpenApiParameter(
            "genres",
            type={
                "type": "list",
                "items": {"type": "number"},
            },
            description="Filter by Genres id (ex. ?genres=1,3)",
        ),
        OpenApiParameter(
            "actors",
            type={
                "type": "list",
                "items": {"type": "number"},
            },
            description="Filter by Actors id (ex. ?actors=1,3)",
        ),
        OpenApiParameter(
            "title",
            type=OpenApiTypes.STR,
            description="Filter by Play title (ex. ?title=Test)",
        ),
    ]
)

performance_list_schema = extend_schema(
    parameters=[
        OpenApiParameter(
            "play",
            type=OpenApiTypes.INT,
            description="Filter by Play id (ex. ?play=3)",
        ),
        OpenApiParameter(
            "date",
            type=OpenApiTypes.DATE,
            description=(
                "Filter by datetime of Performance " "(ex. ?date=2023-05-05)"
            ),
        ),
    ]
)
