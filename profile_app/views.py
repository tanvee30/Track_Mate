from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status

from .models import Profile, TrustedContact, AadhaarVerification, VehicleDetails, InviteFriend
from .serializers import (
    ProfileSerializer,
    TrustedContactSerializer,
    AadhaarVerificationSerializer,
    VehicleDetailsSerializer,
    FullProfileSerializer,
    InviteFriendSerializer,
)


# --------------------------
# USER PROFILE VIEW
# --------------------------
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


# --------------------------
# TRUSTED CONTACTS CRUD
# --------------------------
class TrustedContactViewSet(viewsets.ModelViewSet):
    serializer_class = TrustedContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TrustedContact.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


# --------------------------
# AADHAAR VERIFY
# --------------------------
class AadhaarVerificationView(generics.RetrieveUpdateAPIView):
    serializer_class = AadhaarVerificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile = self.request.user.profile
        obj, _ = AadhaarVerification.objects.get_or_create(profile=profile)
        return obj


# --------------------------
# VEHICLE DETAILS
# --------------------------
class VehicleDetailsView(generics.RetrieveUpdateAPIView):
    serializer_class = VehicleDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile = self.request.user.profile
        obj, _ = VehicleDetails.objects.get_or_create(profile=profile)
        return obj


# --------------------------
# FULL PROFILE
# --------------------------
class FullProfileView(generics.RetrieveAPIView):
    serializer_class = FullProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


# --------------------------
# INVITE FRIEND VIEWSET
# --------------------------
class InviteFriendViewSet(viewsets.ModelViewSet):
    queryset = InviteFriend.objects.all()
    serializer_class = InviteFriendSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Auto-set profile from logged-in user"""
        serializer.save(profile=self.request.user.profile)
    @action(detail=True, methods=['post'], url_path='accept')
    def accept_invite(self, request, pk=None):
        """
        Accept an invite - the invited friend must be logged in
        """
        try:
            invite = self.get_object()
            
            # Check if the logged-in user's email matches the invited email
            if request.user.email != invite.friend_email:
                return Response(
                    {"error": "You are not authorized to accept this invite"},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Check if already accepted
            if invite.accepted:
                return Response(
                    {"message": "Invite already accepted"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Accept the invite
            invite.accepted = True
            invite.save()
            
            return Response(
                {
                    "message": "Invite accepted successfully!",
                    "invite": InviteFriendSerializer(invite).data
                },
                status=status.HTTP_200_OK
            )
            
        except InviteFriend.DoesNotExist:
            return Response(
                {"error": "Invite not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'], url_path='my-friends')
    def my_friends(self, request):
        """
        Get list of friends for the logged-in user
        Shows accepted invites where user was the inviter OR invitee
        """
        try:
            user_email = request.user.email
            user_profile = request.user.profile
            
            # Friends where I invited them (and they accepted)
            invited_by_me = InviteFriend.objects.filter(
                profile=user_profile,
                accepted=True
            ).values_list('friend_email', flat=True)
            
            # Friends who invited me (and I accepted)
            invited_me = InviteFriend.objects.filter(
                friend_email=user_email,
                accepted=True
            ).select_related('profile__user').values_list('profile__user__email', flat=True)
            
            # Combine both lists and remove duplicates
            all_friends = list(set(list(invited_by_me) + list(invited_me)))
            
            return Response({
                "user": user_email,
                "friends_count": len(all_friends),
                "friends": all_friends
            })
        except Profile.DoesNotExist:
            return Response(
                {"error": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], url_path='my-invites')
    def my_invites(self, request):
        """
        Get all invites sent by the logged-in user (both accepted and pending)
        """
        try:
            invites = InviteFriend.objects.filter(
                profile=request.user.profile
            ).order_by('-created_at')
            
            serializer = self.get_serializer(invites, many=True)
            
            # Add summary statistics
            total = invites.count()
            accepted = invites.filter(accepted=True).count()
            pending = invites.filter(accepted=False).count()
            
            return Response({
                "summary": {
                    "total_invites": total,
                    "accepted": accepted,
                    "pending": pending
                },
                "invites": serializer.data
            })
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], url_path='pending-invites')
    def pending_invites(self, request):
        """
        Get invites received by the logged-in user that are pending acceptance
        """
        try:
            invites = InviteFriend.objects.filter(
                friend_email=request.user.email,
                accepted=False
            ).order_by('-created_at')
            
            serializer = self.get_serializer(invites, many=True)
            
            return Response({
                "pending_count": invites.count(),
                "invites": serializer.data
            })
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], url_path='received-invites')
    def received_invites(self, request):
        """
        Get all invites received by the logged-in user (both accepted and pending)
        """
        try:
            invites = InviteFriend.objects.filter(
                friend_email=request.user.email
            ).order_by('-created_at')
            
            serializer = self.get_serializer(invites, many=True)
            
            # Add summary
            total = invites.count()
            accepted = invites.filter(accepted=True).count()
            pending = invites.filter(accepted=False).count()
            
            return Response({
                "summary": {
                    "total_received": total,
                    "accepted": accepted,
                    "pending": pending
                },
                "invites": serializer.data
            })
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
