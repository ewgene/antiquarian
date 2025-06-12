from dj_rest_auth.registration.views import RegisterView, SocialLoginView # type: ignore
from dj_rest_auth.views import LoginView # type: ignore
from django.contrib.auth import get_user_model # type: ignore
from django.utils.translation import gettext as _ # type: ignore
from rest_framework import permissions, status # type: ignore
from rest_framework.generics import ( # type: ignore
    GenericAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.response import Response # type: ignore
from rest_framework.viewsets import ReadOnlyModelViewSet # type: ignore 

from users.models import Address, PhoneNumber, Profile # type: ignore
#from users.permissions import IsUserAddressOwner, IsUserProfileOwner


User = get_user_model()


class SendOrResendSMSAPIView(GenericAPIView):
    """
    Check if submitted phone number is a valid phone number and send OTP.
    """

    #serializer_class = PhoneNumberSerializer

    def post(self, request, *args, **kwargs):
        #serializer = self.get_serializer(data=request.data)

        #if serializer.is_valid():
            # Send OTP
        #    phone_number = str(serializer.validated_data["phone_number"])
            phone_number = str(request.data["phone_number"])
            user = User.objects.filter(phone__phone_number=phone_number).first()

            if not user:
                return Response({"error": _("User not found")}, status=status.HTTP_404_NOT_FOUND)
            
            if user.phone.is_verified:
                return Response({"error": _("Phone number already verified")}, status=status.HTTP_400_BAD_REQUEST)
            
            user.phone.generate_security_code()