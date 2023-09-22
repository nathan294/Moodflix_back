# Moodflix API

# Générer les migrations de base de données

alembic check   _pour check si il y a des modifications sur les modèles par rapport à la bdd_

alembic revision --autogenerate -m "Message"    _pour créer une migration dans alembic/versions_

alembic upgrade head   _pour appliquer les migrations sur la base de données_


# Lancer le docker pour le dev en local

cd .dev/moodflix && docker compose --env-file docker.env up

_you can add --build or --force-recreate to rebuild or force recreate_
