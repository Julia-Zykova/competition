from drf_yasg import openapi

list_photos = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "count": openapi.Schema(type=openapi.TYPE_INTEGER, title="Total count of posts"),
        "next": openapi.Schema(
            type=openapi.TYPE_STRING, title="The URL of the next page",
            format=openapi.FORMAT_URI,
            pattern=f"http://localhost:8000/api/v1/photos/\?page={int}",
        ),
        "previous": openapi.Schema(
            type=openapi.TYPE_STRING, title="The URL of the previous page",
            format=openapi.FORMAT_URI,
            pattern=f"http://localhost:8000/api/v1/photos/\?page={int}",
        ),
        "results": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "title": openapi.Schema(type=openapi.TYPE_STRING),
                    "author": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "email": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                format=openapi.FORMAT_EMAIL,
                            ),
                            "get_full_name": openapi.Schema(type=openapi.TYPE_STRING, default="Иванов Иван")
                        },
                    ),
                    "image": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        pattern=f"/media/photos/{int}/{int}/{int}/file/{str}",
                        format=openapi.FORMAT_URI,
                    ),
                    "photo_small": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        pattern=f"/media/CACHE/images/photos/{int}/{int}/{int}/file/{str}/{str}",
                        format=openapi.FORMAT_URI,
                    ),
                    "photo_big": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        pattern=f"/media/CACHE/images/photos/{int}/{int}/{int}/file/{str}/{str}",
                        format=openapi.FORMAT_URI,
                    ),
                    "description": openapi.Schema(type=openapi.TYPE_STRING),
                    "comments": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "voices": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "pub_date": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        default="2024-06-09T16:12:30.010854+03:00",
                        format=openapi.FORMAT_DATETIME,
                    ),
                    "state": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        enum=["in_moderation", "approved", "on_delete"]
                    ),
                }
            )
        ),
    },
)

def errors_schema(extra):
    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "type": openapi.Schema(type=openapi.TYPE_STRING, default=extra["type"]),
            "message": openapi.Schema(type=openapi.TYPE_STRING, default=extra["message"]),
            "translation_key": openapi.Schema(type=openapi.TYPE_STRING, default=extra["translation_key"]),
            "debug_message": openapi.Schema(type=openapi.TYPE_STRING, default=extra["debug_message"]),
            "backtrace": openapi.Schema(type=openapi.TYPE_STRING, default=extra["backtrace"]),

        }
    )


invalid_inputs = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "type": openapi.Schema(type=openapi.TYPE_STRING, default="InvalidInputsError"),
        "message": openapi.Schema(type=openapi.TYPE_STRING, default="Invalid request data"),
        "translation_key": openapi.Schema(type=openapi.TYPE_STRING, default="invalid_request_data"),
        "debug_message": openapi.Schema(type=openapi.TYPE_STRING, description="Might be null or str"),
        "backtrace": openapi.Schema(type=openapi.TYPE_STRING, description="Traceback of error", default=[
            "Traceback (most recent call last):",
            "File '/path/competition/.venv/lib/python3.10/site-packages/service_objects"
            "/services.py', line 195, in service_clean",
            "raise InvalidInputsError(errors, self.non_field_errors())",
            "service_objects.errors.InvalidInputsError: ({'orderby': [ValidationError(['Выберите корректный вариант. "
            "some_string нет среди допустимых значений.'])]}, [])"
        ]),
        "details": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "orderby": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    default=[
                        {
                            "translation_key": "invalid_choice",
                            "message": "Выберите корректный вариант. some_string нет среди допустимых значений."
                        }
                    ],
                )
            },
        ),
        "additional_info": openapi.Schema(type=openapi.TYPE_STRING, description="Might be null or str"),
    }
)

