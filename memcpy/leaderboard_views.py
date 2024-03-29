from __future__ import division
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from memcpy.models import *
from django.db.models import Count
from .forms import *
import random
import json
import operator
from memcpy.forms import *


@login_required
def leader_board(request):
    profiles = Profile.objects.all()
    score_dict = {}
    combo_dict = {}
    accuracy_dict = {}
    for p in profiles:
        score_dict[p] = p.score
        combo_dict[p] = p.max_combo
        if p.attempt == 0:
            accuracy_dict[p] = 0
        else:
            accuracy_dict[p] = p.correct / p.attempt

    sorted_score = sorted(score_dict.items(), key=operator.itemgetter(1), reverse=True)
    sorted_combo = sorted(combo_dict.items(), key=operator.itemgetter(1), reverse=True)
    sorted_accuracy = sorted(accuracy_dict.items(), key=operator.itemgetter(1), reverse=True)

    if len(sorted_score) > 20:
        sorted_score = sorted_score[0:20]
    if len(sorted_combo) > 20:
        sorted_combo = sorted_combo[0:20]
    if len(sorted_accuracy) > 20:
        sorted_accuracy = sorted_accuracy[0:20]

    score_key = []
    combo_key = []
    accuracy_key = []
    accuracy_val = []

    for t in sorted_score:
        score_key.append(t[0])

    for t in sorted_combo:
        combo_key.append(t[0])

    for t in sorted_accuracy:
        accuracy_key.append(t[0])
        accuracy_val.append('%.2f%%' % (t[1] * 100))

    accuracy = zip(accuracy_key, accuracy_val)
    context = {'score': score_key, 'max_combo': combo_key, 'accuracy': accuracy}
    return render(request, 'memcpy/leader-board.html', context)









