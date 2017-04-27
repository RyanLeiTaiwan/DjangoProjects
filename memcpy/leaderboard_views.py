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
        combo_dict[p] = p.combo
        if p.attempt == 0:
            accuracy_dict[p] = 0
        else:
            accuracy_dict[p] = p.correct / p.attempt

    sorted_score = sorted(score_dict.items(), key=operator.itemgetter(1), reverse=True)
    sorted_combo = sorted(combo_dict.items(), key=operator.itemgetter(1), reverse=True)
    sorted_accuracy = sorted(accuracy_dict.items(), key=operator.itemgetter(1), reverse=True)

    print (sorted_score)
    print (sorted_combo)
    print (sorted_accuracy)
    if len(sorted_score) > 10:
        sorted_score = dict(sorted_score[0:10])
    if len(sorted_combo) > 10:
        sorted_combo = dict(sorted_combo[0:10])
    if len(sorted_accuracy) > 10:
        sorted_accuracy = dict(sorted_accuracy[0:10])

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
        accuracy_val.append(str(t[1] * 100) + "%")

    accuracy = zip(accuracy_key, accuracy_val)
    print(accuracy)
    context = {'score': score_key, 'combo': combo_key, 'accuracy': accuracy,}
    return render(request, 'memcpy/leader-board.html', context)









