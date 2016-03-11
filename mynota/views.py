# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core import serializers
import json
from mynota.models import *
from mynota.forms import *
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    else:
        return HttpResponseRedirect('/entrar/')

def entrar(request):
    next=request.GET.get('next', '/home/')
    if request.method == 'POST':
        next = request.POST.get('next', '/home/')
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = form.logar()
            login(request, usuario)
            return HttpResponseRedirect(next)
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'next': next} )

def sair(request):
    logout(request)
    return HttpResponseRedirect('/')

def home(request):
    return render(request, 'home.html', {'usuario': Professor.objects.get(user=request.user)})

def aluno_detail(request, id):    
    aluno = get_object_or_404(Aluno, pk=id)
    turmas = Turma.objects.filter(aluno = aluno)
    # notas = Nota.objects.filter(aluno=aluno)    
    return render(request, 'aluno_detail.html', {'turmas': turmas, 'aluno': aluno}) 

def aula_add(request):
    if request.method == 'POST':
        form = AulaForm(request.POST)
        if form.is_valid():
            aula = Aula(
                professor = Professor.objects.get(user=request.user),
                turma = form.cleaned_data['turma'],
                data = form.cleaned_data['data'],
                conteudo = form.cleaned_data['conteudo']
            )
            aula.save()
            messages.success(request, 'Aula registrada com sucesso!')
            return HttpResponseRedirect('/aula/add/')
        else:
            messages.error(request, 'Preencha corretamente os campos indicados!')
    else:
        form = AulaForm()
    return render(request, 'aula_add.html', {'form': form})

def aula_delete(request, id):
    aula = get_object_or_404(Aula, pk=id, professor__user = request.user)
    aula.delete()
    messages.success(request, 'Aula removida com sucesso')
    return HttpResponseRedirect('/aula_add/')


def aulas_por_turma(request, turma):
    queryset = Aula.objects.filter(turma__pk=turma).order_by('data')
    list = [] #create list
    for row in queryset: #populate list
        if row.professor.user == request.user:
            list.append({'turma':row.turma.codigo, 'professor': row.professor.user.first_name +" "+ row.professor.user.last_name,'data': row.data.strftime('%d/%m/%Y'), 'conteudo': row.conteudo, 'id': row.id})
        else:
            list.append({'turma':row.turma.codigo, 'professor': row.professor.user.first_name +" "+ row.professor.user.last_name,'data': row.data.strftime('%d/%m/%Y'), 'conteudo': row.conteudo, 'id': False})
    recipe_list_json = json.dumps(list) #dump list as JSON
    return HttpResponse(recipe_list_json, 'application/javascript')

def user_add(request):
    usuario = User.objects.create_user(request.POST['username'].lower(), request.POST['email'], request.POST['senha'])
    usuario.save()
    return usuario

def modulos_por_turma(request, turma):
    turma = Turma.objects.get(pk=turma)
    queryset = Modulo.objects.filter(curso=turma.curso)
    list = [] #create list
    for row in queryset: #populate list
        list.append({'id':row.id, 'nome':row.nome})
    recipe_list_json = json.dumps(list) #dump list as JSON
    return HttpResponse(recipe_list_json, 'application/javascript') 

def plano_aula_add(request):
    if request.method == 'POST':
        form = PlanoAulaForm(request.POST)
        if form.is_valid():
            # data_lista = request.POST['data'].split('/')
            # data = datetime(int(data_lista[2]),int(data_lista[1]),int(data_lista[0]))
            plano_aula = PlanoAula(
                turma = form.cleaned_data['turma'],
                modulo = form.cleaned_data['modulo'],
                professor = Professor.objects.get(user=request.user),
                data = form.cleaned_data['data'],
                conteudo = form.cleaned_data['conteudo'],
            )
            plano_aula.save()
            messages.success(request, 'Plano de aula registrado com sucesso')
            return HttpResponseRedirect('/plano_aula/add/')
    else:
        form = PlanoAulaForm()
    return render(request, 'plano_aula_add.html', {'form': form})

def planos_por_turma(request, turma):
    queryset = PlanoAula.objects.filter(turma__pk=turma).order_by('data')
    list = [] #create list
    for row in queryset: #populate list
        list.append({'turma':row.turma.codigo, 'modulo':row.modulo.nome, 'professor': row.professor.user.first_name +" "+ row.professor.user.last_name,'data': row.data.strftime('%d/%m/%Y'), 'conteudo': row.conteudo, 'id': row.id})
    recipe_list_json = json.dumps(list) #dump list as JSON
    return HttpResponse(recipe_list_json, 'application/javascript')    

def professor_add(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            usuario = user_add(request)
            professor = Professor (
                nome = request.POST['nome'],
                comentario = request.POST['comentario'],
                situacao = request.POST['situacao'],
                user = usuario
            )
            professor.save()
            return HttpResponseRedirect(reverse('professor_add'))
    else:
        form = ProfessorForm()
    return render(request, 'professor_add.html', {'form': form})

def turma_detail(request, id):    
    turma = get_object_or_404(Turma, pk=id)
    aulas = Aula.objects.filter(turma = turma)
    planos = PlanoAula.objects.filter(turma = turma)
    lista = []
    return render(request, 'turma_detail.html', {'turma': turma, 'aulas': aulas, 'planos': planos}) 

def filtro_turmas(request, opcao):
    if opcao == "minhas":
        queryset = Turma.objects.filter(professor__user=request.user, situacao=True)
    elif opcao == "todas":
        queryset = Turma.objects.filter(situacao=True)
    list = [] #create list
    for row in queryset: #populate list
        list.append({'pk': row.pk, 'codigo':row.codigo, 'curso': row.curso.nome})
    recipe_list_json = json.dumps(list) #dump list as JSON
    return HttpResponse(recipe_list_json, 'application/javascript')