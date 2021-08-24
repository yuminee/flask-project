from marshmallow import fields, Schema

class GetUserReponseSchema(Schema):
    user_id = fields.String(
        required=True,
        metadata={
            'description': 'user uuid',
            'example':'0000-1234-2211-3224'
        }
        )