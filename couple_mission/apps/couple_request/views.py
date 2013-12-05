# -*- coding: utf-8 -*-

# Django
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

# REST Framework
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, link

# Project
from couple_mission.apps.couple.models import Couple
from couple_mission.apps.couple_request.models import CoupleRequest
from couple_mission.apps.couple_request.serializers import CoupleRequestSerializer


class CoupleRequestViewSet(viewsets.ModelViewSet):
    qeuryset = CoupleRequest.objects.all()
    serializer_class = CoupleRequestSerializer
    model = CoupleRequest

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA)
        user_id = request.DATA['user']
        user = User.objects.get(id=user_id)

        if not Couple.objects.filter(Q(partner_a=user) | Q(partner_b=user)):
            if serializer.is_valid():
                request_sender = request.DATA['request_sender']
                request_receiver = request.DATA['request_receiver']
                requests = CoupleRequest.objects.filter(
                    request_receiver=request_sender, connected=False)

                if requests:
                    for r in requests:
                        if unicode(r.request_sender) == request_receiver:
                            couple, created = Couple.objects.get_or_create(
                                partner_a=user, partner_b=r.user)
                            r.connected = True
                            r.save()

                            return Response({'success': True, 'message': _(u'Congratulation! Couple Connencted.')}, status=status.HTTP_201_CREATED)
                else:
                    CoupleRequest.objects.get_or_create(
                        user=user, request_sender=request_sender, request_receiver=request_receiver)

                    return Response({'success': True, 'message': _(u'Waiting for response from partner.')}, status=status.HTTP_200_OK)

        return Response({'success': False, 'message': _(u'%s' % serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
