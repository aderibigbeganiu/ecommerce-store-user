from django.template.defaultfilters import slugify
from rest_framework import viewsets, serializers
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from rest_framework.parsers import MultiPartParser, FormParser


class UserViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "slug"

    def update(self, request, *arg, **kwargs):
        user_object = self.get_object()
        data = request.data
        if (
            User.objects.filter(phone_number=data["phone_number"]).exists()
            and User.objects.filter(phone_number=data["phone_number"])[0]
            != User.objects.filter(username=data["username"])[0]
        ):
            raise serializers.ValidationError(
                {"detail": "A user with the phone number already exist"}
            )
        if len(data["phone_number"]) > 15:
            raise serializers.ValidationError(
                {"detail": "Phone number can't be longer than 15 characters"}
            )

        user_object.slug = slugify(data["username"])
        # if data["profile_picture"] != "":
        #     user_object.profile_picture = data["profile_picture"]

        fields = user_object._meta.fields
        # exclude = ["profile_picture"]
        for field in fields:
            field = field.name.split(".")[-1]  # to get column name
            # if field in exclude:
            #     continue
            exec("user_object.%s = data.get(field, user_object.%s)" % (field, field))

        serializer_context = {
            "request": request,
        }

        user_object.save()

        serializer = UserSerializer(user_object, context=serializer_context)
        return Response(serializer.data)
