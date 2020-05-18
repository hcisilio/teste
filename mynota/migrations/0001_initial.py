# Generated by Django 3.0.6 on 2020-05-18 03:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=20, null=True, unique=True)),
                ('nome', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Dia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=15, unique=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=45)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modulo', to='mynota.Curso')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('sobrenome', models.CharField(max_length=256)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('comentario', models.TextField(blank=True, max_length=1000, null=True)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('disciplina_padrao', models.CharField(choices=[['Administração', 'Administração'], ['Informática', 'Informática'], ['Inglês', 'Inglês']], max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Professor',
                'verbose_name_plural': 'Professores',
            },
        ),
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=10, unique=True, verbose_name='Código')),
                ('situacao', models.BooleanField(default=True, verbose_name='Situação')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='turma', to='mynota.Curso')),
                ('dia', models.ManyToManyField(to='mynota.Dia')),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='turma', to='mynota.Professor')),
            ],
        ),
        migrations.CreateModel(
            name='PlanoAula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('conteudo', models.TextField(max_length=2048)),
                ('modulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plano_aula', to='mynota.Modulo')),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plano_aula', to='mynota.Professor')),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plano_aula', to='mynota.Turma')),
            ],
            options={
                'verbose_name': 'Plano de aula',
                'verbose_name_plural': 'Planos de aula',
            },
        ),
        migrations.CreateModel(
            name='Aula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('conteudo', models.TextField(max_length=2048)),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aula', to='mynota.Professor')),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aula', to='mynota.Turma')),
            ],
        ),
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('sobrenome', models.CharField(max_length=256)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('comentario', models.TextField(blank=True, max_length=1000, null=True)),
                ('matricula', models.CharField(max_length=10, unique=True)),
                ('turma', models.ManyToManyField(to='mynota.Turma')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Nota',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.FloatField()),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nota', to='mynota.Aluno')),
                ('modulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nota', to='mynota.Modulo')),
            ],
            options={
                'unique_together': {('aluno', 'modulo')},
            },
        ),
    ]
