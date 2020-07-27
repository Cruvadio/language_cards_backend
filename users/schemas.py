import coreapi
import coreschema
from django.utils.translation import ugettext as _
from rest_framework.schemas import ManualSchema

profile_languages_schema = ManualSchema(
    fields=[
        coreapi.Field(
            "action",
            required=True,
            location="form",
            schema=coreschema.String(
                title=_("Action"),
                description=_("'ADD' to add languages to current user, 'DELETE' to delete languages from current user")
            )
        ),
        coreapi.Field(
            "field",
            required=True,
            location="form",
            schema=coreschema.String(
                title=_("Field name"),
                description=_(
                    "'language_know' to /delete languages to/from known by user, 'languagle_learn' to add/delete languages to/from languages learning by user")
            )
        ),
        coreapi.Field(
            "languages",
            required=True,
            location="form",
            schema=coreschema.Array(
                title=_("Languages"),
                description=_('Languages written capitalized in English (e.q. English, Russian, etc.)')),

        ),
    ],

    description=_("Endpoint for adding and deleting languages to/from current user."),
    encoding="application/json"
)

change_hobbies_schema = ManualSchema(
    fields=[
        coreapi.Field(
            "hobbies",
            required=True,
            location="form",
            schema=coreschema.String(
                title=_("Hobbies"),
                description=_("Field with user hobbies")
            )
        ),
    ],

    description=_("Endpoint for changing user hobbies."),
    encoding="application/json"
)

change_about_schema = ManualSchema(
    fields=[
        coreapi.Field(
            "about",
            required=True,
            location="form",
            schema=coreschema.String(
                title=_("About me"),
                description=_("Field with user self description")
            )
        ),
    ],

    description=_("Endpoint for changing user hobbies."),
    encoding="application/json"
)

change_avatar_schema = ManualSchema(
    fields=[
        coreapi.Field(
            "file",
            required=True,
            location="form",
            schema=coreschema.String(
                title=_("Avatar"),
                description=_("User avatar. Should be raw image, with name.")
            )
        ),
    ],

    description=_("Endpoint for uploading avatar."),
    encoding="multipart/form-data"
)

toggle_follow_schema = ManualSchema(
    fields=[
        coreapi.Field(
            "id",
            required=True,
            location='path',
            schema=coreschema.String(
                title=_("ID"),
                description=_("A unique integer value identifying this profile.")
            )
        )
    ],

    description=_("Endpoint for following user."),
    encoding="application/json"
)
